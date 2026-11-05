"""Exercise the real R launcher; no test framework installation is needed."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
LAUNCHER = PROJECT / "scripts" / "run-r.ps1"


class LauncherTests(unittest.TestCase):
    def run_launcher(self, *arguments, env=None):
        return subprocess.run(
            [shutil.which("pwsh"), "-NoProfile", "-File", str(LAUNCHER), *arguments],
            cwd=tempfile.gettempdir(),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=90,
        )

    def test_default_invocation_reports_the_selected_r_version(self):
        # Catches Rscript rejecting --version when --vanilla is placed first.
        result = self.run_launcher()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("4.5.0", result.stdout + result.stderr)

    def test_explicit_version_and_help_flags_do_not_attempt_a_script(self):
        for flag, expected in [("--version", "4.5.0"), ("--help", "Usage")]:
            with self.subTest(flag=flag):
                result = self.run_launcher("-RArguments", flag)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_launches_clean_r_with_literal_arguments_and_project_working_directory(self):
        # Catches shell interpolation, lost argument boundaries, locale leakage,
        # missing Pandoc, and dependence on the caller's working directory.
        with tempfile.TemporaryDirectory(prefix="ds116 launcher test ") as directory:
            directory = Path(directory)
            probe = directory / "probe with spaces.R"
            result_file = directory / "probe.json"
            probe.write_text(
                'p <- list(arguments = commandArgs(trailingOnly = TRUE), '
                'cwd = normalizePath(getwd(), winslash = "/"), '
                'version = as.character(getRversion()), '
                'pandoc = rmarkdown::pandoc_available(), '
                'locale_override = Sys.getenv("LC_ALL"))\n'
                'writeLines(jsonlite::toJSON(p, auto_unbox = TRUE), '
                'Sys.getenv("SETUP_PROBE_OUTPUT"), useBytes = TRUE)\n'
                'cat("probe stdout visible\\n")\n'
                'message("probe stderr visible")\n',
                encoding="utf-8",
            )
            env = dict(os.environ, SETUP_PROBE_OUTPUT=str(result_file),
                       LANG="C.UTF-8", LC_ALL="C.UTF-8", LC_CTYPE="C.UTF-8")
            literal_arguments = ["argument with spaces", 'a"b', "$(never-run);literal", ""]
            result = self.run_launcher(str(probe), *literal_arguments, env=env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            observed = json.loads(result_file.read_text(encoding="utf-8"))
            self.assertEqual(observed["arguments"], literal_arguments)
            self.assertEqual(Path(observed["cwd"]), PROJECT)
            self.assertEqual(observed["version"], "4.5.0")
            self.assertTrue(observed["pandoc"])
            self.assertEqual(observed["locale_override"], "")
            self.assertNotIn("Setting LC_", result.stderr)
            self.assertIn("probe stdout visible", result.stdout)
            self.assertIn("probe stderr visible", result.stderr)

    def test_propagates_r_failure_exit_code(self):
        # Catches a launcher that reports success after R fails.
        with tempfile.TemporaryDirectory(prefix="ds116 exit test ") as directory:
            script = Path(directory) / "intentional failure.R"
            script.write_text("quit(save = 'no', status = 7)\n", encoding="utf-8")
            result = self.run_launcher(str(script))
            self.assertEqual(result.returncode, 7, result.stdout + result.stderr)

    def test_missing_r_executable_fails_without_starting_analysis(self):
        # Catches silent fallback to a different R installation.
        result = self.run_launcher("-RscriptPath", str(PROJECT / "missing-Rscript.exe"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Rscript executable not found", result.stderr)

    def test_missing_pandoc_fails_with_actionable_diagnostic(self):
        # Catches a silent fallback to an unverified renderer.
        result = self.run_launcher("-PandocDirectory", str(PROJECT / "missing-pandoc"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Pandoc executable not found", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
