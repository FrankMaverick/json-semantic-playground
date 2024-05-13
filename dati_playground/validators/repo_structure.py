from pathlib import Path
from typing import List
import logging

log = logging.getLogger(__name__)
required_subdirs = ["assets/controlled-vocabularies", "assets/ontologies", "assets/schemas"]


def validate(root_dir: Path) -> bool:
    """
    Validate directory structure to ensure required directories exist.
    
    Args:
        root_dir (Path): The root directory path to be checked.
        required_subdirs (list): A list of required subdirectories to be checked.

    Returns:
        bool: True if the required directories exist, False otherwise.
    """

    if not root_dir.is_dir():
        log.warning(f"{root_dir} is not a directory.")
        return False

    subdirs = []
    for subdir in root_dir.iterdir():

        if subdir.is_dir():
            subdirs.append(str("/".join(subdir.parts)))


    # Verifica se tutte le sotto-directory dirette sono presenti in required_subdirs
    if set(subdirs) <= set(required_subdirs):
        return
    else:
        # Trova le sotto-directory mancanti
        missing_dirs = set(subdirs) - set(required_subdirs)
        
        # Logga gli errori
        if missing_dirs:
            log.error(f"One or more Directories do not conform to the expected structure in {root_dir} dir: {missing_dirs}")

        return False