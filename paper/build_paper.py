"""Build the FRB periodicity preprint PDF from the markdown source.

Inputs:
    paper/frb_periodicity_investigation.md (markdown source)
    paper/figures/*.png (referenced from the markdown)

Outputs:
    paper/frb_periodicity_investigation.pdf

Pipeline role:
    Produces the citable PDF artifact for Zenodo deposit. Locates pandoc
    and xelatex on the host system (checking common Windows install
    locations if PATH does not include them), then invokes pandoc with
    xelatex as the PDF engine. xelatex is required for Unicode characters
    used throughout the paper (alpha, sigma, perp, approx, etc.).

    The script is idempotent: re-running it overwrites the output PDF.

Code license: MIT -- see LICENSE for details.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PAPER_DIR = Path(__file__).resolve().parent
REPO_ROOT = PAPER_DIR.parent
SOURCE_MD = PAPER_DIR / "frb_periodicity_investigation.md"
OUTPUT_PDF = PAPER_DIR / "frb_periodicity_investigation.pdf"


def locate(executable_name: str, extra_dirs: list[Path]) -> str:
    """Find an executable: prefer PATH, fall back to listed install dirs."""
    on_path = shutil.which(executable_name)
    if on_path:
        return on_path
    for directory in extra_dirs:
        candidate = directory / f"{executable_name}.exe"
        if candidate.exists():
            return str(candidate)
        candidate_no_ext = directory / executable_name
        if candidate_no_ext.exists():
            return str(candidate_no_ext)
    return ""


def main() -> int:
    local_app_data = Path(os.environ.get("LOCALAPPDATA", ""))
    pandoc_path = locate(
        "pandoc",
        [
            local_app_data / "Pandoc",
            Path(r"C:\Program Files\Pandoc"),
        ],
    )
    if not pandoc_path:
        print("error: pandoc not found on PATH or in known install locations.", file=sys.stderr)
        return 1

    xelatex_path = locate(
        "xelatex",
        [
            local_app_data / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
            Path(r"C:\Program Files\MiKTeX\miktex\bin\x64"),
        ],
    )
    if not xelatex_path:
        print("error: xelatex not found on PATH or in known MiKTeX install locations.", file=sys.stderr)
        return 1

    # Augment PATH so pandoc can find xelatex when it shells out.
    env = os.environ.copy()
    xelatex_dir = str(Path(xelatex_path).parent)
    env["PATH"] = xelatex_dir + os.pathsep + env.get("PATH", "")

    # Build command. xelatex is required for the unicode characters used in
    # the paper (alpha, sigma, perp, approx, Greek letters, etc.). The
    # geometry margins follow typical preprint conventions; colorlinks keeps
    # arxiv URLs in the references readable.
    cmd = [
        pandoc_path,
        str(SOURCE_MD),
        "--output", str(OUTPUT_PDF),
        "--pdf-engine", xelatex_path,
        # Disable pandoc's "implicit figures" extension. Without this, an image
        # on its own line gets wrapped in a LaTeX figure environment with the
        # alt-text as caption (which then collides with our explicit body
        # caption "**Figure 1.** ..." below the image). With the extension
        # off, the image renders inline and the body caption is the only
        # visible caption.
        "--from", "markdown-implicit_figures",
        "--variable", "geometry:margin=1in",
        "--variable", "fontsize=11pt",
        "--variable", "colorlinks=true",
        "--variable", "linkcolor=blue",
        "--variable", "urlcolor=blue",
        "--variable", "documentclass=article",
        "--resource-path", str(PAPER_DIR),
        # Allow MiKTeX to auto-install packages on first build.
        "--pdf-engine-opt=-interaction=nonstopmode",
    ]

    print(f"pandoc:  {pandoc_path}")
    print(f"xelatex: {xelatex_path}")
    print(f"source:  {SOURCE_MD}")
    print(f"output:  {OUTPUT_PDF}")
    print()

    # encoding=utf-8 + errors=replace: pandoc emits UTF-8 to its streams, but
    # Windows Python defaults the subprocess text decoder to cp1252 which
    # chokes on em-dashes etc. Force UTF-8 with a safe fallback.
    result = subprocess.run(
        cmd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        print("--- pandoc stdout ---")
        print(result.stdout)
        print("--- pandoc stderr ---")
        print(result.stderr)
        return result.returncode

    if OUTPUT_PDF.exists():
        size_kb = OUTPUT_PDF.stat().st_size / 1024
        print(f"OK: wrote {OUTPUT_PDF} ({size_kb:.1f} KB)")
        return 0

    print("error: pandoc exited 0 but no PDF was produced.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
