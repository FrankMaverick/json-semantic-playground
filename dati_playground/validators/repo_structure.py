from pathlib import Path
from typing import List
import logging

log = logging.getLogger(__name__)
required_subdirs = ["assets/controlled-vocabularies", "assets/ontologies", "assets/schemas"]


def validate(root_dir: Path):
    """
    Validate directory structure to ensure required directories exist.
    Check that the structure of the assets directories 
    complies with required_subdirs.
    
    Args:
        root_dir (Path): The root directory path to be checked.

    """

    if not root_dir.is_dir():
        log.warning(f"{root_dir} is not a directory.")
        return exit(1)

    subdirs = []
    for subdir in root_dir.iterdir():

        if subdir.is_dir():
            subdirs.append(str("/".join(subdir.parts)))


    # Check if all direct subdirectories are present in required_subdirs
    if set(subdirs) <= set(required_subdirs):
        return exit(0)
    else:
        # Find missing subdirectories
        missing_dirs = set(subdirs) - set(required_subdirs)
        
        if missing_dirs:
            log.error(f"One or more Directories do not conform to the expected structure in {root_dir} dir: {missing_dirs}")

        return exit(1)