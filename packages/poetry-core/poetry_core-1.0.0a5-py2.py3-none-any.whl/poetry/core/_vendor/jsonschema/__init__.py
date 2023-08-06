"""
An implementation of JSON Schema for Python

The main functionality is provided by the validator classes for each of the
supported JSON Schema versions.

Most commonly, `validate` is the quickest way to simply validate a given
instance under a schema, and will create a validator for you.
"""

from poetry.core._vendor.jsonschema.exceptions import (
    ErrorTree, FormatError, RefResolutionError, SchemaError, ValidationError
)
from poetry.core._vendor.jsonschema._format import (
    FormatChecker,
    draft3_format_checker,
    draft4_format_checker,
    draft6_format_checker,
    draft7_format_checker,
)
from poetry.core._vendor.jsonschema._types import TypeChecker
from poetry.core._vendor.jsonschema.validators import (
    Draft3Validator,
    Draft4Validator,
    Draft6Validator,
    Draft7Validator,
    RefResolver,
    validate,
)

__version__ = "3.2.0"
