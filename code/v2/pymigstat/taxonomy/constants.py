# program elements
F_CALL = "function call"
ATTR = "attribute"
DEC = "decorator"
F_REF = "function reference"
TYPE = "type"
EXE = "exception"
IMP = "import"
NO_PE = "none"
NON_FUNC_OR_IMP_PES = [ATTR, DEC, F_REF, TYPE, EXE]
ALL_PES = [F_CALL, ATTR, DEC, F_REF, TYPE, EXE, IMP]
NON_IMPORT_PES = [F_CALL, ATTR, DEC, F_REF, TYPE, EXE, NO_PE]
ALL_PES_WITH_NO_PE = ALL_PES + [NO_PE]
TOTAL = "total"
ALL_PE_DIMS = ALL_PES + [NO_PE, TOTAL]

# cardinalities
ZERO_TO_ONE = "zero-to-one"
ONE_TO_ZERO = "one-to-zero"
ONE_TO_ONE = "one-to-one"
ONE_TO_MANY = "one-to-many"
MANY_TO_ONE = "many-to-one"
MANY_TO_MANY = "many-to-many"
ALL_CARDINALITIES = [ZERO_TO_ONE, ONE_TO_ZERO, ONE_TO_ONE, ONE_TO_MANY, MANY_TO_ONE, MANY_TO_MANY]

# properties
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
ALL_PROPS = [ENC, ARG_ADD, ARG_DEL, ARG_NC, ARG_TRANS, ASYNC_TRANS, OUT_TRANS, PARAM_ADD_TO_DECORATE]
ALL_PROPS_WITH_NO_PROPS = ALL_PROPS + [NO_PROP]
ARGUMENT_PROPERTIES = [ARG_ADD, ARG_DEL, ARG_NC, ARG_TRANS]

_short_name_map = {
    ENC: "elemNC",
    ARG_ADD: "argAdd",
    ARG_DEL: "argDel",
    ARG_NC: "argNC",
    ARG_TRANS: "argTrans",
    ASYNC_TRANS: "asyncTrans",
    OUT_TRANS: "outTrans",
    PARAM_ADD_TO_DECORATE: "paramAdd",
    "input transformation": "inTrans"
}


def short_name(long_name: str):
    return _short_name_map.get(long_name, long_name)
