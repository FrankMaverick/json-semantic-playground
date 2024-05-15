import re
from pathlib import Path

import logging

log = logging.getLogger(__name__)

# List of filenames to be excluded
EXCLUDED_FILENAMES = ["index.ttl", "datapackage.json", "context-short.ld.yaml", "rules.shacl"]

# List of extensions to be excluded
EXCLUDED_EXTENSIONS = [".md", ".shacl", ".frame.yamlld", ".ld.yaml", ".schema.yaml", ".example.yaml", ".example.ttl"]

def validate(fpath: Path):

    suffixes = fpath.suffixes
    extension = ''.join(suffixes)
    filename = re.sub(extension, '', fpath.name)

    if fpath.name in EXCLUDED_FILENAMES or extension in EXCLUDED_EXTENSIONS:
        log.info(f"The file '{fpath.name}' in path '{fpath}' is not checked")
        exit(0)

    # Check the name of the file and parent directories
    path_dirs = fpath.parent 

    if filename not in path_dirs.parts:
        log.error(f"Filename '{fpath.name}' in path '{fpath}' does not match its containing directory name")
        exit(1)

    exit(0)