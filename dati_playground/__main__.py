"""
Validation script for semantic assets.
"""
import logging
from multiprocessing import Pool
from pathlib import Path

import click

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)



from dati_playground.csv import is_csv
from dati_playground.schema import build_schema
from dati_playground.tools import (
    build_semantic_asset,
    build_vocabularies,
    build_yaml_asset,
)
from dati_playground.validators import (
    json_schema,
    openapi,
    is_turtle,
    list_files,
    validate_file,
    shacl,
    versioned_directory,
    repo_structure,
    filename_format,
    filename_match_uri,
    filename_match_directory,
    directory_versioning_pattern,
    mandatory_files_presence,
    utf8_file_encoding
)


@click.command()
@click.argument("command", type=(click.Choice(["validate", "build"])))
@click.argument("files", type=click.Path(exists=True), nargs=(-1))
@click.option("--validate", default=False)
@click.option("--build-semantic", default=False)
@click.option("--build-json", default=False)
@click.option("--build-schema-index", default=False)
@click.option("--build-csv", default=False)
@click.option("--validate-shacl", default=False)
@click.option("--validate-oas3", default=False)
@click.option("--validate-jsonschema", default=False)
@click.option("--validate-versioned-directory", default=False)
@click.option("--validate-turtle", default=False)
@click.option("--validate-csv", default=False)
@click.option("--validate-repo-structure", default=False)
@click.option("--validate-filename-format", default=False)
@click.option("--validate-filename-match-uri", default=False)
@click.option("--validate-filename-match-directory", default=False)
@click.option("--validate-directory-versioning-pattern", default=False)
@click.option("--validate-mandatory-files-presence", default=False)
@click.option("--validate-utf8-file-encoding", default=False)
@click.option("--pattern", default="")
@click.option("--exclude", default=["NoneString"], type=str, multiple=True)
@click.option("--debug", default=False, type=bool)
def main(
    command,
    files,
    validate,
    build_semantic,
    build_json,
    build_csv,
    validate_shacl,
    validate_oas3,
    validate_jsonschema,
    validate_versioned_directory,
    validate_turtle,
    validate_csv,
    validate_repo_structure,
    validate_filename_format,
    validate_filename_match_uri,
    validate_filename_match_directory,
    validate_directory_versioning_pattern,
    validate_mandatory_files_presence,
    validate_utf8_file_encoding,
    pattern,
    exclude,
    build_schema_index,
    debug,
):  
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    if command == "build":
        basepath = Path("assets") if not files else Path(files[0])
        buildpath = Path("_build") if len(files) < 2 else Path(files[1])
        buildpath.mkdir(exist_ok=True, parents=True)

        file_list = [
            x
            for x in list(list_files(basepath))
            if pattern in x.name
            if all((exclude_item not in x.name for exclude_item in exclude))
        ]
        
        log.warning(f"Examining {file_list} with {exclude}")
        workers = Pool(processes=4)
        if validate:
            workers.map(validate_file, file_list)
        if build_semantic:
            workers.starmap(
                build_semantic_asset,
                ((f, buildpath) for f in file_list if f.suffix == ".ttl"),
            )
        if build_csv:
            workers.starmap(
                build_vocabularies,
                ((f, buildpath) for f in file_list if f.suffix == ".ttl"),
            )
        if build_json:
            workers.starmap(
                build_yaml_asset,
                ((f, buildpath) for f in file_list if f.suffix == ".yaml"),
            )
        if build_schema_index:
            workers.starmap(
                build_schema,
                ((f, buildpath) for f in file_list if f.name.endswith((".oas3.yaml",))),
            )
            workers.starmap(
                build_schema,
                ((f, Path(".")) for f in file_list if f.name.endswith((".oas3.yaml",))),
            )

        workers.close()
        exit(0)
    else:
        log.debug(files)
        errors = []
        if command == "validate":
            for f in files:
                f = Path(f)
                if validate_shacl:
                    shacl.validate(f, errors) #ok
                if validate_oas3:
                    openapi.validate(f, errors)
                if validate_jsonschema:
                    json_schema.validate(f, errors)
                if validate_versioned_directory:
                    versioned_directory.validate(f, errors)
                if validate_turtle:
                    is_turtle(f.read_text())
                if validate_csv:
                    is_csv(f, errors)
                if validate_repo_structure:
                    repo_structure.validate(f)
                if validate_filename_format:
                    if not filename_format.validate(f):
                        errors_found = True
                if validate_filename_match_uri:
                    filename_match_uri.validate(f, errors)
                if validate_filename_match_directory:
                    filename_match_directory.validate(f, errors)
                if validate_directory_versioning_pattern:
                    directory_versioning_pattern.validate(f, errors)
                if validate_mandatory_files_presence: 
                    mandatory_files_presence.validate(f, errors)
                if validate_utf8_file_encoding:
                    utf8_file_encoding.validate(f, errors)

            if errors:
                errors = list(set(errors))
                #raise RuntimeError("Errors found: " + "\n".join(errors))
                print("Errors found:")
                for error in errors:
                    print(" - ",error,"\n")
                exit(1)
            else:
                pass
                print("No errors found")


if __name__ == "__main__":
    main()
