from enum import Enum


class RuleTypes(Enum):
    bool = "bool"
    choice = "choice"
    string = "string"
    integer = "integer"
    float = "float"


class Actions(Enum):
    include = "include"
    cmd = "cmd"


BooleanStrValues = {
    "positive": ["true", "yes", "1", "y", "t"],
    "negative": ["false", "no", "0", "n", "f"],
}
