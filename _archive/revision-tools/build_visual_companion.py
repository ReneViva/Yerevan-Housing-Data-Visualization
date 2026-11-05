"""Build the chart-led Word teaching companion from the editable master Rmd.

This is an archived authoring utility, not a dependency of the student's Rmd.
Run with Codex's bundled Python. The coordinator owns the document-authoring
marker and final Word/PDF rendering. This builder does not claim visual QA.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Mm, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
CODE_STYLE = "Exact R code"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def chunks_from_rmd(path: Path) -> list[dict]:
    """Keep every code line, normalizing only platform line endings to LF."""
    lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    chunks = []
    position = 0
    while position < len(lines):
        match = re.match(r"^(`{3,}|~{3,})\s*\{r\s+([^}\n]+)\}\s*$", lines[position])
        if not match:
            if re.match(r"^(`{3,}|~{3,})\s*\{r\s*\}", lines[position]):
                raise ValueError(f"Rmd line {position + 1} has an unlabeled chunk")
            position += 1
            continue
        fence, header = match.groups()
        label = re.split(r"[,\s]", header.strip(), maxsplit=1)[0]
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", label):
            raise ValueError(f"Invalid chunk label: {label!r}")
        end = position + 1
        while end < len(lines) and not re.fullmatch(rf"{re.escape(fence)}\s*", lines[end]):
            end += 1
        if end == len(lines):
            raise ValueError(f"Unclosed chunk: {label}")
        code = "".join(lines[position + 1:end])
        chunks.append({"label": label, "code": code, "lines": code.splitlines(),
                       "code_sha256": digest(code.encode("utf-8")),
                       "rmd_first_line": position + 2, "rmd_last_line": end})
        position = end + 1
    labels = [c["label"] for c in chunks]
    if not chunks or len(labels) != len(set(labels)):
        raise ValueError("Rmd must contain uniquely labeled chunks")
    return chunks


def required_text(value, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing explanatory text: {name}")
    return value.strip()


def validate(chunks: list[dict], guide: list[dict], results: dict, root: Path):
    if [c["label"] for c in chunks] != [g.get("label") for g in guide]:
        raise ValueError("Guide labels/order must match every actual Rmd chunk")
    actuals = results.get("chunks", {})
    figures = []
    for chunk, entry in zip(chunks, guide):
        label = chunk["label"]
        for field in ("title", "purpose", "expected", "interpretation", "hypothesis"):
            required_text(entry.get(field), f"{label}.{field}")
        required_text(actuals.get(label), f"results.chunks.{label}")
        covered = set()
        previous = 0
        for block in entry.get("blocks", []):
            start, end = block.get("start"), block.get("end")
            if not isinstance(start, int) or not isinstance(end, int):
                raise ValueError(f"Noninteger code-line range in {label}")
            if start <= previous or end < start or end > len(chunk["lines"]):
                raise ValueError(f"Invalid/overlapping range {start}-{end} in {label}")
            required_text(block.get("explanation"), f"{label}.lines.{start}-{end}")
            covered.update(range(start, end + 1))
            previous = end
        nonblank = {n for n, line in enumerate(chunk["lines"], 1) if line.strip()}
        if nonblank - covered:
            raise ValueError(f"Unexplained lines in {label}: {sorted(nonblank-covered)}")
        if entry.get("figure"):
            image = (root / entry["figure"]).resolve()
            if not image.is_relative_to(root.resolve()) or not image.is_file():
                raise ValueError(f"Missing or outside-project figure for {label}")
            figures.append(str(image))
    if len(figures) != 6 or len(set(figures)) != 6:
        raise ValueError("The companion must display exactly six distinct final chart files")


def font(style, name: str, size: float, bold: bool = False):
    style.font.name = name
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.color.rgb = RGBColor(0, 0, 0)
    rfonts = style.element.get_or_add_rPr().get_or_add_rFonts()
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn(f"w:{key}"), name)


def plain_heading(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text).replace("_", " ")).strip()


def mark(paragraph, name: str, identity: int):
    start = OxmlElement("w:bookmarkStart")
    start.set(qn("w:name"), name)
    start.set(qn("w:id"), str(identity))
    end = OxmlElement("w:bookmarkEnd")
    end.set(qn("w:id"), str(identity))
    paragraph._p.insert(0, start)
    paragraph._p.append(end)


def hyperlink(paragraph, title: str, *, anchor=None, url=None):
    link = OxmlElement("w:hyperlink")
    if anchor:
        link.set(qn("w:anchor"), anchor)
    else:
        relation = paragraph.part.relate_to(
            url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
        link.set(qn("r:id"), relation)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "21576B")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    properties.extend((color, underline))
    run.append(properties)
    text = OxmlElement("w:t")
    text.text = title
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def para(doc, text: str = "", style=None, keep_next=False):
    paragraph = doc.add_paragraph(text, style=style)
    paragraph.paragraph_format.keep_with_next = keep_next
    return paragraph


def labeled(doc, label: str, text: str):
    paragraph = doc.add_paragraph()
    paragraph.add_run(label + " ").bold = True
    paragraph.add_run(text)
    return paragraph


def configure(doc):
    section = doc.sections[0]
    section.page_width, section.page_height = Mm(210), Mm(297)
    section.top_margin = section.bottom_margin = Inches(0.65)
    section.left_margin = section.right_margin = Inches(0.65)
    section.footer_distance = Inches(0.25)
    normal = doc.styles["Normal"]
    font(normal, "Calibri", 11)
    normal.paragraph_format.line_spacing = 1.05
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.widow_control = True
    for name, size in [("Title", 27), ("Subtitle", 14), ("Heading 1", 17), ("Heading 2", 12)]:
        style = doc.styles[name]
        font(style, "Calibri", size, bold=name != "Subtitle")
        style.paragraph_format.space_before = Pt(12 if name.startswith("Heading") else 0)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.keep_with_next = True
        props = style.element.get_or_add_pPr()
        for element in list(props):
            if element.tag == qn("w:pBdr"):
                props.remove(element)
    code = doc.styles.add_style(CODE_STYLE, WD_STYLE_TYPE.PARAGRAPH)
    code.base_style = normal
    font(code, "Consolas", 10)
    code.paragraph_format.line_spacing = 1.0
    code.paragraph_format.space_before = code.paragraph_format.space_after = Pt(0)
    code.paragraph_format.left_indent = Inches(0.32)
    code.paragraph_format.first_line_indent = Inches(-0.32)
    code.paragraph_format.tab_stops.add_tab_stop(Inches(0.32))
    code.paragraph_format.widow_control = False
    code.paragraph_format.keep_together = True
    caption = doc.styles["Caption"]
    font(caption, "Calibri", 10)
    caption.paragraph_format.space_after = Pt(7)
    caption.paragraph_format.keep_with_next = False
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run("Page ").font.size = Pt(9)
    number = OxmlElement("w:fldSimple")
    number.set(qn("w:instr"), "PAGE")
    footer._p.append(number)
    doc.core_properties.title = "Yerevan Housing Code and Chart Guide"
    doc.core_properties.subject = "Beginner explanation of the six-chart R Markdown study"
    doc.core_properties.author = "DS116 research project"


def add_glossary(doc):
    terms = [
        ("read.csv", "Read a CSV file into an R table."),
        ("<- and %>%", "Store a result; then pass it into another operation."),
        ("group_by and summarise", "Group records and calculate a summary such as a median."),
        ("mutate and filter", "Create a column; keep rows matching a condition."),
        ("ggplot and aes", "Start a chart and connect variables to positions or colors."),
        ("geom_col and facet_wrap", "Draw bars; make separate panels for the modes."),
        ("ggsave", "Save the same chart to the figures folder."),
        ("stopifnot", "Stop if a required data or arithmetic check is false."),
    ]
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(2.1)
    table.columns[1].width = Inches(4.65)
    props = table._tbl.tblPr
    table_width = props.find(qn("w:tblW"))
    if table_width is None:
        table_width = OxmlElement("w:tblW")
        props.append(table_width)
    table_width.set(qn("w:type"), "dxa")
    table_width.set(qn("w:w"), str(round(6.75 * 1440)))
    table_indent = props.find(qn("w:tblInd"))
    if table_indent is None:
        table_indent = OxmlElement("w:tblInd")
        props.append(table_indent)
    table_indent.set(qn("w:type"), "dxa")
    table_indent.set(qn("w:w"), "0")
    table.rows[0].cells[0].text = "R expression"
    table.rows[0].cells[1].text = "Meaning"
    for term, meaning in terms:
        cells = table.add_row().cells
        cells[0].text, cells[1].text = term, meaning
    for row_index, row in enumerate(table.rows):
        for column_index, cell in enumerate(row.cells):
            # Word honors each cell's preferred width as well as the grid.
            cell.width = Inches(2.1 if column_index == 0 else 4.65)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            props = cell._tc.get_or_add_tcPr()
            borders = OxmlElement("w:tcBorders")
            for edge in ("top", "left", "bottom", "right"):
                border = OxmlElement(f"w:{edge}")
                border.set(qn("w:val"), "single")
                border.set(qn("w:sz"), "4")
                border.set(qn("w:color"), "D9D9D9")
                borders.append(border)
            props.append(borders)
            fill = OxmlElement("w:shd")
            fill.set(qn("w:fill"), "DDE8EC" if row_index == 0 else ("F5F7F8" if row_index % 2 == 0 else "FFFFFF"))
            props.append(fill)
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.space_before = Pt(4)
                for run in p.runs:
                    run.font.size = Pt(10.5)
                    if row_index == 0:
                        run.bold = True


def add_exact_code(doc, chunk):
    for number, line in enumerate(chunk["lines"], 1):
        p = doc.add_paragraph(style=CODE_STYLE)
        run = p.add_run(str(number))
        run.font.color.rgb = RGBColor(90, 90, 90)
        p.add_run("\t")
        p.add_run(line)


def verify_saved(docx_path: Path, chunks: list[dict]):
    reopened = Document(docx_path)
    actual = [p.text for p in reopened.paragraphs if p.style.name == CODE_STYLE]
    expected = [f"{i}\t{line}" for chunk in chunks for i, line in enumerate(chunk["lines"], 1)]
    if actual != expected:
        raise ValueError("Actual saved Word code does not match the current Rmd")
    if len(reopened.inline_shapes) != 6:
        raise ValueError("Saved companion does not contain all six chart images")
    return len(actual)


def build(args):
    root = args.root.resolve()
    chunks = chunks_from_rmd(args.rmd)
    guide = load_json(args.guide)
    results = load_json(args.results)
    validate(chunks, guide, results, root)
    if args.check_only:
        print(f"PASS: {len(chunks)} chunks, explained lines, executed narratives and six chart files.")
        return
    references = list(csv.DictReader((root / "data/sources.csv").open(encoding="utf-8-sig")))
    doc = Document()
    configure(doc)
    title = para(doc, "Yerevan Housing Code and Chart Guide", "Title")
    title.paragraph_format.space_before = Pt(60)
    para(doc, "Understanding the six chart research story", "Subtitle")
    para(doc, "DS116 Data Visualization\nAmerican University of Armenia\nResearch snapshot 5 November 2026")
    para(doc, "Read a question, look at its chart, then use the short code explanation to understand how the result was made. This guide follows the exact R Markdown code in order and keeps the same charts beside the relevant steps.")
    para(doc, "Related source: Yerevan_Housing_Research.Rmd")
    para(doc, "The study compares one agency's advertised monthly rents with modeled commuting and winter utility costs. Its conclusions apply to the stated sample and assumptions, not every household in Yerevan.")
    doc.add_page_break()

    h = doc.add_heading("How to use this guide", 1)
    mark(h, "guide_start", 1)
    para(doc, "The Rmd is the editable analysis. It reads the four CSV inputs in data, calculates the results, and saves six charts in figures. The HTML report starts with the visual story; this companion explains the code behind it.")
    para(doc, "Line numbers restart at 1 for each chunk. They are added only in Word and are not part of executable R. A wrapped display line is still the same numbered code line. Read each logical block together; the glossary explains recurring verbs once.")
    add_glossary(doc)
    para(doc, "Observed asking rents and sample counts come from the cleaned agency dataset. Road inputs are network-model outputs. Consumption, transit speed/waiting, car costs and the value of time are assumptions. A modeled budget is not an observed household bill.")
    p = doc.add_paragraph()
    p.add_run("Jump to a code step: ").bold = True
    for i, entry in enumerate(guide, 1):
        if i > 1:
            p.add_run("  ·  ")
        hyperlink(p, str(i), anchor=f"chunk_{i:02d}")

    for i, (chunk, entry) in enumerate(zip(chunks, guide), 1):
        h = doc.add_heading(f"{i} {plain_heading(entry['title'])}", 1)
        # A visual question should open together with its chart rather than
        # appearing as a heading at the foot of the previous code explanation.
        if entry.get("figure"):
            h.paragraph_format.page_break_before = True
        mark(h, f"chunk_{i:02d}", 100 + i)
        para(doc, f"R Markdown chunk: {chunk['label']}", keep_next=True)
        para(doc, entry["purpose"], keep_next=True)
        if entry.get("figure"):
            p = doc.add_paragraph()
            p.paragraph_format.keep_with_next = False
            p.add_run().add_picture(str(root / entry["figure"]), width=Inches(6.85))
        doc.add_heading("Exact code", 2)
        add_exact_code(doc, chunk)
        doc.add_heading("Read the code in blocks", 2)
        for block in entry["blocks"]:
            start, end = block["start"], block["end"]
            label = f"Line {start}." if start == end else f"Lines {start}–{end}."
            labeled(doc, label, block["explanation"])
        labeled(doc, "Expected output:", entry["expected"])
        labeled(doc, "Actual result:", results["chunks"][chunk["label"]])
        labeled(doc, "What it means:", entry["interpretation"])
        labeled(doc, "Research connection:", entry["hypothesis"])
        p = doc.add_paragraph()
        p.add_run("Sources: ")
        hyperlink(p, "references", anchor="references")
        p.add_run(".")

    doc.add_heading("Statistics and responsible interpretation", 1)
    para(doc, "The median is the middle observed rent. Quartiles show the middle half of the selected advertisements; they are not confidence intervals for all Yerevan rentals. Differences shown by the charts are not proof that otherwise identical homes would cost the same amount after a move.")
    para(doc, "A p-value requires a justified sampling and statistical model. It is not the probability that a hypothesis is true. This single-agency convenience dataset and its repeated cost scenarios do not support the intended population inference, so the analysis does not manufacture p-values or confidence intervals.")
    para(doc, "Sensitivity charts change declared assumptions. Their cells are scenarios, not probabilities. A break-even value holds the other model inputs fixed; it does not identify a universal distance where savings vanish. Advertised furnishing, missing condition and approximate district geography remain important limits.")
    para(doc, "AI assistance was used for planning, code and explanations. The student should understand and independently explain the work and confirm the instructor's project and AI-assistance rules before submission.")
    h = doc.add_heading("References", 1)
    mark(h, "references", 500)
    for row in references:
        publisher = row.get("publisher", "")
        date = row.get("date", "Date not stated")
        title = row.get("title", row.get("url", "Source"))
        p = doc.add_paragraph()
        p.add_run(f"{publisher}. {date}. ")
        hyperlink(p, title, url=row["url"])
        p.add_run(f". Accessed {row.get('accessed', '2026-11-05')}.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output)
    count = verify_saved(args.output, chunks)
    manifest = {
        "rmd_sha256": digest(args.rmd.read_bytes()),
        "guide_sha256": digest(args.guide.read_bytes()),
        "results_sha256": digest(args.results.read_bytes()),
        "docx_sha256": digest(args.output.read_bytes()),
        "code_style": CODE_STYLE, "number_separator": "TAB", "code_line_paragraphs": count,
        "code_hash_convention": "UTF-8 with normalized LF; chunk terminal LF retained",
        "chunks": [{k: v for k, v in c.items() if k != "lines"} | {"line_count": len(c["lines"])} for c in chunks],
        "figures": [{"path": e["figure"], "sha256": digest((root / e["figure"]).read_bytes())}
                    for e in guide if e.get("figure")],
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created {args.output}; {len(chunks)} exact chunks, {count} code paragraphs, six charts.")
    print("Render and inspect every page before delivery; no visual-validation claim is made here.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--rmd", type=Path, default=ROOT / "Yerevan_Housing_Research.Rmd")
    parser.add_argument("--guide", type=Path, default=ROOT / "_archive/revision-tools/companion-guide.json")
    parser.add_argument("--results", type=Path, default=ROOT / "_archive/revision-checks/results.json")
    parser.add_argument("--output", type=Path, default=ROOT / "Yerevan_Housing_Code_Companion.docx")
    parser.add_argument("--manifest", type=Path, default=ROOT / "_archive/revision-checks/companion-manifest.json")
    parser.add_argument("--check-only", action="store_true")
    build(parser.parse_args())


if __name__ == "__main__":
    main()
