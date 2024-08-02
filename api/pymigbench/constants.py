from enum import Enum


class ProgramElement(Enum):
    FUNCTION_CALL = "function call"
    ATTRIBUTE = "attribute"
    DECORATOR = "decorator"
    FUNCTION_REFERENCE = "function reference"
    TYPE = "type"
    EXCEPTION = "exception"
    IMPORT = "import"


class Cardinality(Enum):
    ZERO_TO_ONE = "zero-to-one"
    ONE_TO_ZERO = "one-to-zero"
    ONE_TO_ONE = "one-to-one"
    ONE_TO_MANY = "one-to-many"
    MANY_TO_ONE = "many-to-one"
    MANY_TO_MANY = "many-to-many"
    NOT_APPLICABLE = "not applicable"


class Property(Enum):
    ELEMENT_NAME_CHANGE = "element name change"
    ARGUMENT_ADDITION = "argument addition"
    ARGUMENT_DELETION = "argument deletion"
    ARGUMENT_NAME_CHANGE = "argument name change"
    ARGUMENT_TRANSFORMATION = "argument transformation"
    ASYNC_TRANSFORMATION = "async transformation"
    OUTPUT_TRANSFORMATION = "output transformation"
    PARAM_ADD_TO_DECORATED = "parameter addition to decorated function"


_short_name_map = {
    ProgramElement.FUNCTION_CALL: "fCall",
    ProgramElement.ATTRIBUTE: "attr",
    ProgramElement.DECORATOR: "dec",
    ProgramElement.FUNCTION_REFERENCE: "fRef",
    ProgramElement.TYPE: "type",
    ProgramElement.EXCEPTION: "exc",
    ProgramElement.IMPORT: "imp",

    Property.ELEMENT_NAME_CHANGE: "elemNC",
    Property.ARGUMENT_ADDITION: "argAdd",
    Property.ARGUMENT_DELETION: "argDel",
    Property.ARGUMENT_NAME_CHANGE: "argNC",
    Property.ARGUMENT_TRANSFORMATION: "argTrans",
    Property.ASYNC_TRANSFORMATION: "asyncTrans",
    Property.OUTPUT_TRANSFORMATION: "outTrans",
    Property.PARAM_ADD_TO_DECORATED: "paramAdd",

    Cardinality.ONE_TO_ONE: "OO",
    Cardinality.ONE_TO_MANY: "OM",
    Cardinality.MANY_TO_ONE: "MO",
    Cardinality.MANY_TO_MANY: "MM",
    Cardinality.ZERO_TO_ONE: "ZO",
    Cardinality.ONE_TO_ZERO: "OZ",
}


def short_name(long_name: str):
    return _short_name_map.get(long_name, long_name)
