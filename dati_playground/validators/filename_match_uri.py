import re
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, SKOS, Namespace

import logging

log = logging.getLogger(__name__)

def extract_main_uri(ttl_file: Path):
    """
    Extracts the main URI relative to the specified TTL file.

    Args:
        ttl_file (Path): The path of the TTL file.

    Returns:
        str: The main relative URI if found, otherwise None.
    """
    g = Graph()
    g.parse(str(ttl_file), format="ttl")

    # Define namespace prefixes
    dcatapit = Namespace("http://dati.gov.it/onto/dcatapit#")

    main_uri = None

    for s, p, o in g:
        if (s, RDF.type, OWL.Ontology) in g and "onto" in str(ttl_file.parents[1]).lower():
            main_uri = s
            break
        elif p == RDF.type and o == dcatapit.Dataset:
            main_uri = s
            break
        # elif (s, RDF.type, RDFS.Class) in g:
        #     main_uri = s
        #     break        
        elif (s, RDF.type, SKOS.ConceptScheme) in g:
            main_uri = s
            break        

    return main_uri

def validate(fpath: Path):

    filename = fpath.stem

    # Extract uri from file path
    uri = extract_main_uri(fpath)
    
    if uri:
        # Extract the final part of the URI
        uri_parts = str(uri).split("/")
        last_uri_part = uri_parts[-1]
        if last_uri_part == '':
            last_uri_part = uri_parts[-2]

        # Check if the parent of the fpath contain "schema"
        if "schema" in fpath.parts[1].lower():
            # Check if the file with .oas3.yaml extension exists
            yaml_file = Path(fpath.parent, f"{last_uri_part}")

            if not yaml_file.exists():
                log.error(f"The file '{yaml_file}' does not match their relative URI '{uri}'")
                exit(1)
        else:
            if fpath.stem != last_uri_part:
                log.error(f"The file '{fpath}' does not match their relative URI '{uri}'")
                exit(1)
    exit(0)