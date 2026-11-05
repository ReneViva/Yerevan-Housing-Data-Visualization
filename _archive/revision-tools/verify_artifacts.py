"""Verify preserved originals and the synchronization of final artifacts."""
import hashlib
import importlib.util
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


manifest = json.loads((ROOT / "_archive/snapshot-manifest.json").read_text(encoding="utf-8-sig"))
previous = ROOT / "_archive/previous-version"
for name, expected in manifest.items():
    assert sha((previous / name).read_bytes()) == expected, name
with zipfile.ZipFile(ROOT / "_archive/Before_simplification_2026-11-05.zip") as snapshot:
    for name, expected in manifest.items():
        assert sha(snapshot.read(name)) == expected, name
for name in ["Yerevan_Housing_Research.Rmd", "outputs/Yerevan_Housing_Research.html",
             "outputs/Yerevan_Housing_Code_Companion.docx"]:
    blob = subprocess.run(["git", "show", "before-visual-simplification:" + name],
                          cwd=ROOT, capture_output=True, check=True).stdout
    assert sha(blob) == sha((previous / name).read_bytes()), name

spec = importlib.util.spec_from_file_location("companion", Path(__file__).with_name("build_visual_companion.py"))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
chunks = builder.chunks_from_rmd(ROOT / "Yerevan_Housing_Research.Rmd")
docx = ROOT / "Yerevan_Housing_Code_Companion.docx"
lines = builder.verify_saved(docx, chunks)
current = json.loads((ROOT / "_archive/revision-checks/companion-manifest.json").read_text(encoding="utf-8"))
for key, path in [("rmd_sha256", ROOT / "Yerevan_Housing_Research.Rmd"),
                  ("guide_sha256", Path(__file__).with_name("companion-guide.json")),
                  ("results_sha256", ROOT / "_archive/revision-checks/results.json"),
                  ("docx_sha256", docx)]:
    assert sha(path.read_bytes()) == current[key], key
with zipfile.ZipFile(docx) as document:
    embedded = [sha(document.read(name)) for name in document.namelist() if name.startswith("word/media/")]
final_figures = [sha(path.read_bytes()) for path in sorted((ROOT / "figures").glob("*.png"))]
assert len(embedded) == len(final_figures) == 6
assert sorted(embedded) == sorted(final_figures), "Word must contain the current chart files"
assert sorted(p.name for p in (ROOT / "data").iterdir()) == ["rentals.csv", "sources.csv", "tariffs.csv", "wages.csv"]
assert sorted(p.name for p in (ROOT / "outputs").iterdir()) == ["Yerevan_Housing_Research.html", "Yerevan_Housing_Research.pdf"]
print(f"PASS: {len(manifest)} originals and ZIP contents unchanged; previous Git tag verified; "
      f"Word matches {len(chunks)} chunks, {lines} code lines and six current PNGs.")
