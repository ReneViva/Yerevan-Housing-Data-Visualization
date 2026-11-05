"""Check that the student-facing Rmd runs with only its four CSV inputs."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
R = r"D:\Softwares\Applications\R\R-4.5.0\bin\Rscript.exe"
env = {k: v for k, v in os.environ.items() if k not in {"LANG", "LANGUAGE"} and not k.startswith("LC_")}
env["RSTUDIO_PANDOC"] = r"D:\Softwares\Applications\RStudio\resources\app\bin\quarto\bin\tools"
env["PATH"] = r"C:\Users\Raven\AppData\Roaming\TinyTeX\bin\windows;" + env["PATH"]
with tempfile.TemporaryDirectory(prefix="yerevan clean report ") as temp:
    folder = Path(temp)
    shutil.copy2(ROOT / "Yerevan_Housing_Research.Rmd", folder)
    shutil.copytree(ROOT / "data", folder / "data")
    result = subprocess.run(
        [R, "--vanilla", "-e", 'file <- "Yerevan_Housing_Research.Rmd"; knit <- eval(parse(text=rmarkdown::yaml_front_matter(file)$knit)); knit(file)'],
        cwd=folder, env=env, capture_output=True, text=True, encoding="utf-8", timeout=180,
    )
    log = ROOT / "_archive/revision-checks/clean-render.log"
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode:
        print(result.stdout + result.stderr)
        raise SystemExit(result.returncode)
    assert (folder / "outputs/Yerevan_Housing_Research.html").exists()
    assert (folder / "outputs/Yerevan_Housing_Research.pdf").exists()
    assert len(list((folder / "figures").glob("*.png"))) == 6
    assert set(p.name for p in (folder / "data").iterdir()) == {"rentals.csv", "tariffs.csv", "wages.csv", "sources.csv"}
    print("PASS: isolated Knit function produced HTML, PDF and six figures from only the Rmd and four data CSVs.")
