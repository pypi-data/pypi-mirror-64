"""Command line interface for sorting YAML files."""


import pathlib
from typing import Any, Iterable, List, Optional, Sequence, Tuple

import fastjsonschema
import yaml
from yamltable.typing import Row, Schema


__author__ = "Macklan Weinstein"
__version__ = "0.0.8"


def dependencies(unsorted: Sequence[Row], depends: str, name: str) -> List[Row]:
    """Sort rows based on the dependencies found in key.

    Args:
        unsorted: Rows to sort.
        depends: Dictionary key whose values are other dictionary dependencies.
        name: Foreign key for dependencies.

    Raises:
        ValueError: If rows contain circular requirements.

    Returns:
        Rows sorted by requirements.
    """

    sorted_: List[Row] = []
    while unsorted:
        # Find rows containing only dependencies in sorted_.
        names = [pkg[name] for pkg in sorted_]
        rows = [
            (idx, pkg)
            for idx, pkg in enumerate(unsorted)
            if set(pkg[depends]).issubset(names)
        ]

        if rows:
            idxs, pkgs = zip(*rows)
            # Append found rows to sorted_ and remove them from unsorted.
            sorted_ += pkgs
            unsorted = [
                elem for idx, elem in enumerate(unsorted) if idx not in idxs
            ]
        else:
            # If no rows are found then there exist circular dependencies.
            raise ValueError("encountered circular dependencies.")

    return sorted_


def read(file_path: pathlib.Path) -> Tuple[List[Row], Optional[Schema]]:
    """Read data from YAML file.

    Args:
        file_path: YAML file path.

    Raises:
        FileNotFoundError: If unable to find file path.
        TypeError: If file is not organized as a list.

    Returns:
        YAML data.
    """

    try:
        with open(file_path, "r") as handle:
            data = yaml.safe_load(handle)
    except (yaml.scanner.ScannerError, yaml.parser.ParserError) as xcpt:
        raise TypeError(f"invalid YAML file: {xcpt}")

    if isinstance(data, list):
        return data, None
    elif isinstance(data, dict):
        try:
            return data["rows"], data["schema"]
        except KeyError:
            raise TypeError(
                "YAML file does not have a schema and rows organization"
            )
    else:
        raise TypeError("YAML file is not organized in a tabular format")


def search(key: str, val: Any, rows: Iterable[Row]) -> List[Row]:
    """Search dictionaries by key and value.

    Args:
        key: Search key.
        val: Key comparison value.
        rows: Dictionaries to search.

    Returns:
        Matching dictionaries.
    """

    return [row for row in rows if key in row and row[key] == val]


def sort(key: str, rows: Iterable[Row]) -> List[Row]:
    """Sort dictionaries based on value for supplied key name.

    Args:
        key: Search key.
        rows: Dictionaries to sort.

    Returns:
        List of sorted dictionaries.
    """

    return sorted(rows, key=lambda row: row[key])


def validate(
    rows: Iterable[Row], schema: Optional[Schema]
) -> Tuple[bool, int, str]:
    """Check that each row satisfies the schema.

    Args:
        rows: Dictionaries to validate.
        schema: JSON schema for validation.

    Returns:
        Whether all rows are valid, invalid row index or -1,
            invalid error message.
    """

    try:
        validator = fastjsonschema.compile(schema)
    except (fastjsonschema.JsonSchemaDefinitionException, TypeError) as xcpt:
        return False, -1, f"invalid schema: {xcpt}"

    for idx, row in enumerate(rows):
        try:
            validator(row)
        except fastjsonschema.JsonSchemaException as xcpt:
            return False, idx, xcpt.message

    return True, -1, ""


def write(
    file_path: pathlib.Path,
    rows: List[Row],
    schema: Optional[Schema] = None,
    sort_keys: bool = False,
) -> None:
    """Write data to YAML file.

    Args:
        file_path: YAML file path.
        rows: List of dictionaries to write.
        schema: JSON schema dictionary.
        sort_keys: Whether to sort row keys.
    """

    if schema is None:
        with open(file_path, "w") as handle:
            yaml.dump(rows, handle, sort_keys=sort_keys)
    else:
        data = {"schema": schema, "rows": rows}
        with open(file_path, "w") as handle:
            yaml.dump(data, handle, sort_keys=sort_keys)
