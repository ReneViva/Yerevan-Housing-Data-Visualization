"""Build the educational Word companion from the final Rmd and executed results.

Run with the bundled Codex Python. The coordinator must run the document
authoring marker before the first invocation that writes a DOCX. This script
does not render or claim to visually validate the document.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Mm, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_chunks(path: Path) -> list[dict]:
    """Extract labelled R fences, preserving local code lines and terminal LF."""
    lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    chunks = []
    cursor = 0
    while cursor < len(lines):
        match = re.match(r"^(`{3,}|~{3,})\s*\{r(?:\s+|,)([^}\n]*)\}\s*$", lines[cursor])
        if not match:
            if re.match(r"^(`{3,}|~{3,})\s*\{r\s*\}", lines[cursor]):
                raise ValueError(f"Unlabelled R chunk at Rmd line {cursor + 1}")
            cursor += 1
            continue
        fence, header = match.groups()
        label = re.split(r"[,\s]", header.strip(), maxsplit=1)[0]
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", label):
            raise ValueError(f"Missing or invalid R chunk label at line {cursor + 1}")
        end = cursor + 1
        while end < len(lines) and not re.fullmatch(rf"{re.escape(fence)}\s*", lines[end]):
            end += 1
        if end == len(lines):
            raise ValueError(f"Unclosed R chunk {label}")
        code = "".join(lines[cursor + 1:end])
        chunks.append({
            "label": label,
            "code": code,
            "lines": code.splitlines(),
            "rmd_first_code_line": cursor + 2,
            "rmd_last_code_line": end,
            "code_sha256": sha256(code),
        })
        cursor = end + 1
    labels = [chunk["label"] for chunk in chunks]
    if not chunks or len(labels) != len(set(labels)):
        raise ValueError("The Rmd must contain nonempty, uniquely labelled R chunks")
    return chunks


def narrative(value, field: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, list) and value and all(isinstance(v, str) for v in value):
        return "\n".join(value).strip()
    raise ValueError(f"Missing or invalid narrative for {field}")


def validate_inputs(chunks: list[dict], guides: list[dict], results: dict):
    if not isinstance(guides, list):
        raise ValueError("chunk-guide.json must be a list in Rmd chunk order")
    if [c["label"] for c in chunks] != [g.get("label") for g in guides]:
        raise ValueError("Guide labels or ordering differ from the actual Rmd")
    actual = results.get("chunks", {})
    for chunk, guide in zip(chunks, guides):
        label = chunk["label"]
        for field in ("title", "objective", "what", "why", "expected", "hypothesis"):
            narrative(guide.get(field), f"{label}.{field}")
        narrative(actual.get(label), f"results.chunks.{label}")
        covered = set()
        previous_end = 0
        for block in guide.get("blocks", []):
            start, end = block.get("start"), block.get("end")
            if not isinstance(start, int) or not isinstance(end, int):
                raise ValueError(f"Noninteger line range in {label}")
            if start < 1 or end < start or end > len(chunk["lines"]):
                raise ValueError(f"Invalid local line range {start}-{end} in {label}")
            if start <= previous_end:
                raise ValueError(f"Overlapping/out-of-order line blocks in {label}")
            narrative(block.get("explanation"), f"{label}.lines.{start}-{end}")
            covered.update(range(start, end + 1))
            previous_end = end
        meaningful = {i for i, line in enumerate(chunk["lines"], 1) if line.strip()}
        if meaningful - covered:
            raise ValueError(f"Unexplained nonblank code lines in {label}: {sorted(meaningful-covered)}")
    for reference in results.get("references", []):
        if not isinstance(reference, dict) or not str(reference.get("url", "")).startswith(("https://", "http://")):
            raise ValueError("Every reference must supply an HTTP(S) URL")


def set_font(style, name: str, size: float):
    style.font.name = name
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor(0, 0, 0)
    fonts = style.element.get_or_add_rPr().get_or_add_rFonts()
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        fonts.set(qn(f"w:{key}"), name)


def bookmark(paragraph, name: str, identity: int):
    start = OxmlElement("w:bookmarkStart")
    start.set(qn("w:id"), str(identity))
    start.set(qn("w:name"), name)
    end = OxmlElement("w:bookmarkEnd")
    end.set(qn("w:id"), str(identity))
    paragraph._p.insert(0, start)
    paragraph._p.append(end)


def link(paragraph, text: str, *, anchor: str | None = None, url: str | None = None):
    element = OxmlElement("w:hyperlink")
    if anchor:
        element.set(qn("w:anchor"), anchor)
    elif url:
        relation = paragraph.part.relate_to(
            url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True
        )
        element.set(qn("r:id"), relation)
    element.set(qn("w:history"), "1")
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "1F3B58")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    properties.extend((color, underline))
    run.append(properties)
    content = OxmlElement("w:t")
    content.text = text
    run.append(content)
    element.append(run)
    paragraph._p.append(element)


def heading_text(text: str) -> str:
    # Document headings are plain subject labels; exact chunk IDs appear below.
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text).replace("_", " ")).strip()


def paragraph(doc, text: str, style: str | None = None):
    p = doc.add_paragraph(style=style)
    p.add_run(text)
    return p


def subsection(doc, title: str, text: str):
    p = doc.add_paragraph(style="Section label")
    p.add_run(title)
    for part in text.split("\n"):
        if part.strip():
            paragraph(doc, part.strip())


def configure(doc):
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = section.bottom_margin = Inches(0.72)
    section.left_margin = section.right_margin = Inches(0.75)
    section.footer_distance = Inches(0.3)
    normal = doc.styles["Normal"]
    set_font(normal, "Calibri", 11)
    normal.paragraph_format.line_spacing = 1.08
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.widow_control = True
    for name, size in (("Title", 27), ("Subtitle", 14), ("Heading 1", 17), ("Heading 2", 13)):
        style = doc.styles[name]
        set_font(style, "Calibri", size)
        style.font.bold = name != "Subtitle"
        style.paragraph_format.space_before = Pt(13 if name.startswith("Heading") else 0)
        style.paragraph_format.space_after = Pt(7)
        style.paragraph_format.keep_with_next = True
        # Avoid theme borders/color rules surviving from Word's default title.
        props = style.element.get_or_add_pPr()
        for child in list(props):
            if child.tag == qn("w:pBdr"):
                props.remove(child)
    label = doc.styles.add_style("Section label", WD_STYLE_TYPE.PARAGRAPH)
    label.base_style = normal
    set_font(label, "Calibri", 11)
    label.font.bold = True
    label.paragraph_format.space_before = Pt(7)
    label.paragraph_format.space_after = Pt(2)
    label.paragraph_format.keep_with_next = True
    code = doc.styles.add_style("Source code", WD_STYLE_TYPE.PARAGRAPH)
    code.base_style = normal
    set_font(code, "Consolas", 8.5)
    code.paragraph_format.line_spacing = 1.0
    code.paragraph_format.space_after = Pt(0)
    code.paragraph_format.space_before = Pt(0)
    code.paragraph_format.left_indent = Inches(0.34)
    code.paragraph_format.first_line_indent = Inches(-0.34)
    code.paragraph_format.tab_stops.add_tab_stop(Inches(0.34))
    code.paragraph_format.widow_control = False
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer.add_run("Page ")
    run.font.size = Pt(9)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)
    doc.core_properties.title = "Yerevan Housing Research Code Companion"
    doc.core_properties.subject = "Educational explanation of the executable DS116 R Markdown research"
    doc.core_properties.author = "DS116 research project"
    doc.core_properties.keywords = "R Markdown, Yerevan, asking rent, commuting, reproducible analysis"


def add_code(doc, chunk: dict):
    for number, line in enumerate(chunk["lines"], 1):
        p = doc.add_paragraph(style="Source code")
        number_run = p.add_run(str(number))
        number_run.font.color.rgb = RGBColor(95, 95, 95)
        p.add_run("\t")
        p.add_run(line)


def verify_saved_code(output_path: Path, chunks: list[dict]):
    """Read the saved OOXML back and compare every numbered source paragraph."""
    saved = Document(output_path)
    observed = [p.text for p in saved.paragraphs if p.style.name == "Source code"]
    expected = [
        f"{number}\t{line}"
        for chunk in chunks
        for number, line in enumerate(chunk["lines"], 1)
    ]
    if observed != expected:
        raise ValueError("Saved Word code paragraphs differ from the final R Markdown")


def methods_source_links(doc, code: str, references: list[dict]):
    p = doc.add_paragraph()
    p.add_run("Dataset and model citations: ")
    link(p, "project references", anchor="references")
    p.add_run(". Source documents explain the evidence behind the imported fields and assumptions.")
    sources = []
    if re.search(r"ggplot|geom_|aes\(|theme_", code):
        sources.append(("ggplot2 function reference", "https://ggplot2.tidyverse.org/reference/"))
    if re.search(r"library\(dplyr|filter\(|mutate\(|summarise\(|group_by\(|arrange\(|left_join\(", code):
        sources.append(("dplyr function reference", "https://dplyr.tidyverse.org/reference/"))
    sources.append(("R language and package manuals", "https://cran.r-project.org/manuals.html"))
    for title, url in sources:
        p = doc.add_paragraph()
        link(p, title, url=url)


def build(rmd_path: Path, guide_path: Path, results_path: Path, output_path: Path):
    chunks = parse_chunks(rmd_path)
    guides = read_json(guide_path)
    results = read_json(results_path)
    validate_inputs(chunks, guides, results)
    doc = Document()
    configure(doc)
    title = paragraph(doc, "Yerevan Housing Research Code Companion", "Title")
    title.paragraph_format.space_before = Pt(75)
    paragraph(doc, "Understanding the R Markdown analysis", "Subtitle")
    paragraph(doc, "DS116 Data Visualization")
    paragraph(doc, "American University of Armenia")
    paragraph(doc, "Research snapshot 5 November 2026")
    paragraph(doc, "This companion explains how the R Markdown reads real rental advertisements, checks their quality, and compares housing and commuting budgets under stated assumptions. It follows the executable code in the same order so that a beginner can explain each result and its limits.")
    paragraph(doc, f"Related analysis source: {rmd_path.name}")
    doc.add_page_break()

    h = doc.add_heading("Contents", level=1)
    bookmark(h, "contents", 1)
    contents = [
        ("Overview and research method", "overview"),
        ("How to read the code", "reading_code"),
    ] + [(f"Chunk {i} {heading_text(g['title'])}", f"chunk_{i:03d}") for i, g in enumerate(guides, 1)] + [
        ("Statistical interpretation", "statistics"),
        ("Reading the visualizations", "visualizations"),
        ("Limitations and responsible use", "limitations"),
        ("References", "references"),
    ]
    for title, anchor in contents:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        link(p, title, anchor=anchor)
    paragraph(doc, "Select a contents entry to jump to its section. Line numbers restart at 1 in every chunk and refer to the code displayed in this companion.")

    h = doc.add_heading("Overview and research method", level=1)
    bookmark(h, "overview", 2)
    paragraph(doc, "The research asks whether advertised rent savings outside Kentron offset extra transport, utilities, heating and optionally valued commuting time. Named Yerevan districts remain separate. This study describes an agency catalogue and modeled budgets, so its comparisons cannot establish what a particular household would save by moving.")
    paragraph(doc, "The source records contain advertised monthly asking rents rather than signed rental contracts. Eligibility checks select comparable room counts and floor areas, native AMD prices, advertised furniture and usable geographic information. Unknown renovation quality and agency selection remain limitations. Source creation dates do not establish when prices last changed.")
    paragraph(doc, "Direct monthly cost adds the selected rent, utility and transportation components. Generalized monthly cost also adds commuting hours multiplied by an assumed value of time. Gas supplies the heating component and is included once. These budgets exclude unmeasured spending and do not represent complete household cost of living.")
    paragraph(doc, "The commuting destination is Republic Square. Cached road-network distances and driving durations describe a routing model. Public-transport speed, access and waiting, car operating costs, congestion, consumption and household inputs are declared scenarios. They are not observed individual journeys or bills.")
    paragraph(doc, "The code produces descriptive medians and listing spreads, then tests how the modeled comparison changes when assumptions change. Repeated scenario rows are different calculations for the same evidence; they do not create additional sampled households.")

    h = doc.add_heading("How to read the code", level=1)
    bookmark(h, "reading_code", 3)
    paragraph(doc, "An object name stores a result for later use. The assignment symbol <- gives that object a value. Parentheses contain a function's inputs, and a comma separates inputs. A data frame is a table; each row is a record and each column is a variable. Text inside quotation marks is a character string.")
    paragraph(doc, "The pipe %>% reads as then: pass a table into the next operation. filter keeps rows, select keeps columns, mutate creates variables, group_by defines groups, and summarise produces one summary per group. A test inside stopifnot must be true or execution stops, helping prevent invalid output.")
    paragraph(doc, "ggplot creates a chart, aes connects variables to visual positions or colors, and geom layers draw marks such as points, bars or lines. labs supplies readable titles and units. Read each code block with its stated question, then compare the expected output type with the actual result calculated by R.")
    paragraph(doc, "The Word code is extracted directly from the final R Markdown. Local line numbers are added beside it for explanation; they are not part of the R code. Visual wrapping of a long line does not create another code line.")

    for index, (chunk, guide) in enumerate(zip(chunks, guides), 1):
        h = doc.add_heading(f"Chunk {index} {heading_text(guide['title'])}", level=1)
        bookmark(h, f"chunk_{index:03d}", 100 + index)
        p = doc.add_paragraph()
        p.add_run("Related R Markdown chunk: ")
        label_run = p.add_run(chunk["label"])
        label_run.font.name = "Consolas"
        subsection(doc, "Research objective", narrative(guide["objective"], "objective"))
        subsection(doc, "What the code does", narrative(guide["what"], "what"))
        p = doc.add_paragraph(style="Section label")
        p.add_run("Exact code with local line numbers")
        add_code(doc, chunk)
        p = doc.add_paragraph(style="Section label")
        p.add_run("Code explanation")
        for block in guide["blocks"]:
            start, end = block["start"], block["end"]
            lead = f"Line {start}" if start == end else f"Lines {start} to {end}"
            p = doc.add_paragraph()
            p.add_run(lead + ". ").bold = True
            p.add_run(narrative(block["explanation"], lead))
        subsection(doc, "Why this method was chosen", narrative(guide["why"], "why"))
        subsection(doc, "Expected result", narrative(guide["expected"], "expected"))
        actual_text = narrative(results["chunks"][chunk["label"]], "actual")
        if guide.get("interpretation"):
            actual_text += "\n" + narrative(guide["interpretation"], "interpretation")
        subsection(doc, "Actual result and interpretation", actual_text)
        subsection(doc, "Connection to the hypothesis", narrative(guide["hypothesis"], "hypothesis"))
        p = doc.add_paragraph(style="Section label")
        p.add_run("Sources and citations")
        methods_source_links(doc, chunk["code"], results.get("references", []))

    h = doc.add_heading("Statistical interpretation", level=1)
    bookmark(h, "statistics", 400)
    paragraph(doc, "A median is the middle observed value after sorting; half the records lie on either side. The interquartile range runs from the 25th to the 75th percentile and describes the middle half of the observed listings. It does not give a confidence interval for all Yerevan renters.")
    paragraph(doc, "A p-value is calculated under a specified null model. It describes how incompatible an observed test statistic is with that model. It is not the probability that the hypothesis is true, the chance that a finding will replicate, or a measure of financial importance.")
    paragraph(doc, "A confidence interval concerns repeated-sampling uncertainty under a defensible sampling and estimation procedure. That interpretation requires assumptions about selection, independence and the model. Convenience advertisements, uncertain dwelling duplication and constructed scenario budgets do not provide the required basis for the intended population tests here. The analysis therefore does not manufacture p-values or population confidence intervals.")
    paragraph(doc, "Sensitivity ranges show how a calculation changes when inputs change. They are useful for comparing assumptions, although they do not carry a 95 percent sampling-coverage interpretation. A break-even value is an algebraic threshold conditional on the other assumptions; it is not proof that every apartment at a particular distance crosses that threshold.")

    h = doc.add_heading("Reading the visualizations", level=1)
    bookmark(h, "visualizations", 401)
    paragraph(doc, "Start with the units and comparison group. AMD per month is a cash budget, while hours describe travel time. A chart that monetizes time includes an assumption about AMD per hour. Check that assumption before comparing it with a chart of direct costs.")
    paragraph(doc, "Rent distributions and area tables describe the selected catalogue. Modeled cost charts combine evidence with assumed components. A larger plotted budget does not establish higher actual household spending. A sensitivity chart is most useful where changing a plausible assumption changes the sign of the comparison.")
    paragraph(doc, "District summary archetypes combine district summary inputs. Such a calculated budget does not necessarily equal the median of all listing-level total costs, and its difference from Kentron is not a matched comparison of otherwise identical homes. Small district sample counts and uncertain source locations should remain visible when interpreting the figures.")

    h = doc.add_heading("Limitations and responsible use", level=1)
    bookmark(h, "limitations", 402)
    paragraph(doc, "The main evidence limits are single-agency selection, asking versus transacted rent, unknown dwelling condition, incomplete building attributes, possible duplicated properties, imperfect geographic labels and modeled travel/consumption. Results apply to the stated sample and scenarios; they do not establish a causal effect of living farther from the center.")
    paragraph(doc, "AI assistance supported research planning, coding and educational explanations. The student should understand and independently explain the code and confirm the instructor's policy before submission. Course teaching examples establish relevant methods, while a project-specific rubric and AI policy remain unconfirmed. The companion does not claim that unrestricted AI use is permitted.")

    h = doc.add_heading("References", level=1)
    bookmark(h, "references", 403)
    references = results.get("references", [])
    for index, reference in enumerate(references, 1):
        title = str(reference.get("title") or reference.get("publisher") or reference["url"])
        publisher = str(reference.get("publisher") or "")
        date = str(reference.get("date") or "Date not stated")
        accessed = str(reference.get("accessed") or "5 November 2026")
        paragraph(doc, f"{index}. {publisher}. {title}. {date}. Accessed {accessed}.")
        p = doc.add_paragraph()
        link(p, reference["url"], url=reference["url"])
    paragraph(doc, "R programming and package documentation")
    for title, url in (
        ("R manuals", "https://cran.r-project.org/manuals.html"),
        ("ggplot2 function reference", "https://ggplot2.tidyverse.org/reference/"),
        ("dplyr function reference", "https://dplyr.tidyverse.org/reference/"),
        ("R Markdown reference", "https://rmarkdown.rstudio.com/docs/"),
        ("knitr documentation", "https://yihui.org/knitr/"),
    ):
        p = doc.add_paragraph()
        link(p, title, url=url)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    verify_saved_code(output_path, chunks)
    manifest = {
        "rmd_source": str(rmd_path.resolve()),
        "rmd_file_sha256": hashlib.sha256(rmd_path.read_bytes()).hexdigest(),
        "guide_file_sha256": hashlib.sha256(guide_path.read_bytes()).hexdigest(),
        "results_file_sha256": hashlib.sha256(results_path.read_bytes()).hexdigest(),
        "code_hash_convention": "UTF-8 text with LF line endings; final LF preserved from Rmd chunk",
        "word_code_style": "Source code",
        "word_line_number_separator": "TAB after local line number",
        "chunks": [
            {key: value for key, value in chunk.items() if key != "lines"}
            | {"line_count": len(chunk["lines"])}
            for chunk in chunks
        ],
    }
    manifest_path = output_path.with_name("companion-code-manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {output_path} with {len(chunks)} exact Rmd chunks.")
    print(f"Created code manifest: {manifest_path}")
    print("Document still requires rendering and visual inspection before delivery.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rmd", type=Path, default=ROOT / "Yerevan_Housing_Research.Rmd")
    parser.add_argument("--guide", type=Path, default=ROOT / "references/chunk-guide.json")
    parser.add_argument("--results", type=Path, default=ROOT / "outputs/results.json")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/Yerevan_Housing_Code_Companion.docx")
    parser.add_argument("--check-only", action="store_true", help="Validate inputs without creating any artifact")
    args = parser.parse_args()
    if args.check_only:
        chunks = parse_chunks(args.rmd)
        validate_inputs(chunks, read_json(args.guide), read_json(args.results))
        print(f"Validated {len(chunks)} source chunks, explanations and actual-result narratives.")
        return
    build(args.rmd, args.guide, args.results, args.output)


if __name__ == "__main__":
    main()
