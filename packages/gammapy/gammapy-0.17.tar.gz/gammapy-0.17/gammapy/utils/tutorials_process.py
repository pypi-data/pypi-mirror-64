# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Process tutorials notebooks for publication in documentation."""
import argparse
import logging
import os
import shutil
import subprocess
import sys
from distutils.util import strtobool
from pathlib import Path
from gammapy.scripts.jupyter import notebook_test

log = logging.getLogger(__name__)


def ignorefiles(d, files):
    return [
        f
        for f in files
        if os.path.isfile(os.path.join(d, f))
        and f[-6:] != ".ipynb"
        and f[-4:] != ".png"
    ]


def setup_sphinx_params(args):
    flagnotebooks = "True"
    setupfilename = "setup.cfg"
    if not args.nbs:
        flagnotebooks = "False"
    build_notebooks_line = f"build_notebooks = {flagnotebooks}\n"

    file_str = ""
    with open(setupfilename) as f:
        for line in f:
            if line.startswith("build_notebooks ="):
                line = build_notebooks_line
            file_str += line

    with open(setupfilename, "w") as f:
        f.write(file_str)


def build_notebooks(args):
    if "GAMMAPY_DATA" not in os.environ:
        log.info("GAMMAPY_DATA environment variable not set.")
        log.info("Running notebook tests requires this environment variable.")
        log.info("Exiting now.")
        sys.exit()

    # prepare folder structure
    pathsrc = Path(args.src)
    path_temp = Path("temp")
    path_empty_nbs = Path("tutorials")
    path_filled_nbs = Path("docs") / "notebooks"
    path_static_nbs = Path("docs") / "_static" / "notebooks"

    shutil.rmtree(path_temp, ignore_errors=True)
    path_temp.mkdir(parents=True, exist_ok=True)
    path_filled_nbs.mkdir(parents=True, exist_ok=True)
    path_static_nbs.mkdir(parents=True, exist_ok=True)

    if pathsrc == path_empty_nbs:
        shutil.rmtree(path_temp, ignore_errors=True)
        shutil.rmtree(path_static_nbs, ignore_errors=True)
        shutil.rmtree(path_filled_nbs, ignore_errors=True)
        shutil.copytree(path_empty_nbs, path_temp, ignore=ignorefiles)
    elif pathsrc.exists():
        notebookname = pathsrc.name
        pathdest = path_temp / notebookname
        shutil.copyfile(pathsrc, pathdest)
    else:
        log.info("Notebook file does not exist.")
        sys.exit()

    if args.fmt:
        subprocess.run(
            [sys.executable, "-m", "gammapy", "jupyter", "--src", "temp", "black"]
        )
    subprocess.run(
        [sys.executable, "-m", "gammapy", "jupyter", "--src", "temp", "strip"]
    )

    # test /run
    for path in path_temp.glob("*.ipynb"):
        notebook_test(path)

    # convert into scripts
    # copy generated filled notebooks to doc
    if pathsrc == path_empty_nbs:
        # copytree is needed to copy subfolder images
        shutil.copytree(path_empty_nbs, path_static_nbs, ignore=ignorefiles)
        for path in path_static_nbs.glob("*.ipynb"):
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jupyter",
                    "nbconvert",
                    "--to",
                    "script",
                    str(path),
                ]
            )
        shutil.copytree(path_temp, path_filled_nbs, ignore=ignorefiles)
    else:
        pathsrc = path_temp / notebookname
        pathdest = path_static_nbs / notebookname
        shutil.copyfile(pathsrc, pathdest)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "script",
                str(pathdest),
            ]
        )
        pathdest = path_filled_nbs / notebookname
        shutil.copyfile(pathsrc, pathdest)

    # tear down
    shutil.rmtree(path_temp, ignore_errors=True)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="Tutorial notebook or folder to process")
    parser.add_argument("--nbs", help="Notebooks are considered in Sphinx")
    parser.add_argument("--fmt", help="Black format notebooks")
    args = parser.parse_args()

    if not args.src:
        args.src = "tutorials"
    if not args.nbs:
        args.nbs = "True"
    if not args.fmt:
        args.fmt = "True"

    try:
        args.nbs = strtobool(args.nbs)
        args.fmt = strtobool(args.fmt)
    except Exception as ex:
        log.error(ex)
        sys.exit()

    setup_sphinx_params(args)

    if args.nbs:
        build_notebooks(args)


if __name__ == "__main__":
    main()
