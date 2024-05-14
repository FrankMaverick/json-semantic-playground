import difflib
import logging
from distutils.version import LooseVersion
from functools import lru_cache
from pathlib import Path
from typing import List

from pyshacl import validate
from rdflib import Graph

log = logging.getLogger(__name__)

MAX_DEPTH = 5
basedir = Path(__file__).parent

def validate(fpath: Path, errors: List):
    if fpath.parent.name != "latest":
        return
    folders = [
        x.name
        for x in fpath.parent.parent.glob("*/")
        if x.name != "latest" and x.is_dir() and x.name[:2] != "v."
    ]
    log.debug("Identified folders: %r", (folders,))
    if not folders:
        log.info(f"No versioned directories found for {fpath}")
        return
    last_version_dirname = sorted(LooseVersion(x) for x in folders)[-1]
    log.debug("Version: %r", (last_version_dirname,))
    cpath = fpath.parent.parent / last_version_dirname.vstring / fpath.name

    with open(cpath) as f_latest, open(fpath) as f_version:
        diffs = []
        diff = difflib.unified_diff(
            f_latest.readlines(),
            f_version.readlines(),
            fromfile=cpath.as_posix(),
            tofile=fpath.as_posix(),
        )
        diffs = "".join(diff)
        if diffs:
            errstr = f"ERROR: files are different: {cpath} {fpath}"
            errors.append(errstr)
            log.error(diffs)
        else:
            log.info(f"File {cpath} is up to date with {fpath}")