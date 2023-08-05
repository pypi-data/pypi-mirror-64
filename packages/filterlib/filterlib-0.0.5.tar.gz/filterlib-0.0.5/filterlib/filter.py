import re
from typing import *
import json


__author__ = "Fabian Becker <fab.becker@outlook.de>"


def __init__():
    return


class Filter:
    replacements = {"__eq__": "=",
                    "__ne__": "!=",
                    "__lt__": "<",
                    "__gt__": ">",
                    "__lte__": "<=",
                    "__gte__":  ">=",
                    "__contains__": " BETWEEN "}

    def __init__(self,
                 operator: str = "AND",
                 allow_missing_attributes: bool = False,
                 **kwargs):
        self.operator = operator
        self.allow_missing_attributes = allow_missing_attributes
        self.ignored_attributes = [x for x in self.__dir__()]
        self.ignored_attributes.append("ignored_attributes")
        # any argument matching the pattern is accepted
        for attr in kwargs:
            if not (re.match(r'\w+__\w+__$', attr) or attr in self.ignored_attributes or type(kwargs[attr]) == Filter):
                raise ValueError(f"{attr} does not match expected attribute format.")
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        # check for all/any non hidden attributes of this class
        # if they are present in another object
        # and equal the corresponding attributes of another object
        patterns = [attr for attr in self.__dir__()
                    if not (attr.startswith("__") or attr in self.ignored_attributes)]
        checks = []
        for pattern in patterns:
            if type(self.__getattribute__(pattern)) != Filter:
                # Check for equality with any object other than filter
                try:
                    attributes = pattern.split("__")[0:-2]
                    magic_method = "__" + pattern.split("__")[-2] + "__"
                    vo = other
                    for attr in attributes:
                        vo = vo.__getattribute__(attr)
                    checks.append(self.__getattribute__(pattern).__getattribute__(magic_method)(vo))
                except AttributeError:
                    if not self.allow_missing_attributes:
                        # when attribute is not present in other object, abort
                        return False
                    else:
                        pass
            else:
                # Check for compatibility with filters
                checks.append(self.__getattribute__(pattern).__eq__(other))
        return False not in checks and len(checks) >= 1

    def __str__(self, logical_condition: Optional[str] = None):
        # Returns a string to be used for sql style databases
        attributes = [a for a in self.__dir__()
                      if not (a.startswith("__") or a in self.ignored_attributes)]
        for attr in range(len(attributes)):
            name = attributes[attr]
            value = self.__getattribute__(name)
            use_brackets = (True if type(value) == Filter and len(value) > 1 else False)
            use_quotes = (True if type(value) == str else False)
            a = (name if type(value) != Filter else "")\
                + ("'" if use_quotes else "")\
                + ("(" if use_brackets else "")\
                + str(value)\
                + (")" if use_brackets else "")\
                + ("'" if use_quotes else "")
            for element in self.replacements:
                a = a.replace(element, self.replacements[element])
            attributes[attr] = a
        return str.join(f" {(logical_condition or self.operator).upper()} ", attributes)

    def __repr__(self):
        # returns a string to be used for storage in text files or sql databases
        d = {x: self.__dict__[x] for x in self.__dict__ if x not in self.ignored_attributes}
        d["operator"] = self.operator
        r = f"<Filter: {json.dumps(d)}>"
        return r

    def __len__(self):
        # returns the number of attributes the filter checks for
        return len([x for x in self.__dir__() if x not in self.ignored_attributes])

    def __bool__(self):
        # returns of the number of attributes the filter checks for is greater than or equal to one
        return bool(self.__len__())


def filter_from_repr(representation: str) -> Filter:
    f = Filter()
    f.__dict__.update(json.loads(representation.lstrip("<Filter: ").rstrip(">")))
    return f


if __name__ == "__main__":
    from tests import tests

    tests.run_tests()
