# precednce.py
class Precedence:
    LOWEST = 0
    ASSIGNMENT = 1     # =
    OR = 2             # or
    AND = 3            # and
    EQUALITY = 4       # ==, !=
    TERM = 5           # + -
    FACTOR = 6         # * /
    PREFIX = 7         # -X, !X
    CALL = 8           # myFunc(X)
    PRIMARY = 9
