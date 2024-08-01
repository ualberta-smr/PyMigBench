from enum import Enum


class ProgramElement(Enum):
    F_CALL = "function call"
    ATTR = "attribute"
    DEC = "decorator"
    F_REF = "function reference"
    TYPE = "type"
    EXC = "exception"
    IMP = "import"
    NO_PE = "none"


class Cardinality(Enum):
    ZERO_TO_ONE = "zero-to-one"
    ONE_TO_ZERO = "one-to-zero"
    ONE_TO_ONE = "one-to-one"
    ONE_TO_MANY = "one-to-many"
    MANY_TO_ONE = "many-to-one"
    MANY_TO_MANY = "many-to-many"


class Property(Enum):
    ENC = "element name change"
    ARG_ADD = "argument addition"
    ARG_DEL = "argument deletion"
    ARG_NC = "argument name change"
    ARG_TRANS = "argument transformation"
    ASYNC_TRANS = "async transformation"
    OUT_TRANS = "output transformation"
    PARAM_ADD_TO_DECORATE = "parameter addition to decorated function"
    NO_PROP = "no properties"
    Not_Applicable = "not applicable"


_short_name_map = {
    ProgramElement.F_CALL: "fCall",
    ProgramElement.ATTR: "attr",
    ProgramElement.DEC: "dec",
    ProgramElement.F_REF: "fRef",
    ProgramElement.TYPE: "type",
    ProgramElement.EXC: "exc",
    ProgramElement.IMP: "imp",

    Property.NO_PROP: "noProps",
    Property.ENC: "elemNC",
    Property.ARG_ADD: "argAdd",
    Property.ARG_DEL: "argDel",
    Property.ARG_NC: "argNC",
    Property.ARG_TRANS: "argTrans",
    Property.ASYNC_TRANS: "asyncTrans",
    Property.OUT_TRANS: "outTrans",
    Property.PARAM_ADD_TO_DECORATE: "paramAdd",

    Cardinality.ONE_TO_ONE: "OO",
    Cardinality.ONE_TO_MANY: "OM",
    Cardinality.MANY_TO_ONE: "MO",
    Cardinality.MANY_TO_MANY: "MM",
    Cardinality.ZERO_TO_ONE: "ZO",
    Cardinality.ONE_TO_ZERO: "OZ",
}


def short_name(long_name: str):
    return _short_name_map.get(long_name, long_name)
