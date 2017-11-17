#!/usr/bin/env python3

import sys

from util import *

FIELD_NAMES = ["region", "odate", "database_url", "database_version",
        "data_retrieval_method", "metric", "units", "value", "notes"]


def process_line(line):
    if line.startswith("#") or line.startswith("insert") or line.startswith(";"):
        return line[:-1]
    assert line.startswith("    ")
    if line.startswith("    ,"):
        result = "    ,"
    else:
        result = "    "
    fields = parse_line(line)
    assert len(FIELD_NAMES) == len(fields)
    lst = []
    for i in range(len(FIELD_NAMES)):
        if FIELD_NAMES[i] == "value" or fields[i] == "NULL":
            lst.append(fields[i])
        else:
            lst.append(mysql_quote(fields[i]))
    result += "(" + ",".join(lst) + ")"
    return result


def parse_line(line):
    fields = {}
    i = 0
    fields[i] = ""
    # 0 for not in a SQL string, 1 for in a SQL string not on a single quote
    # character, 2 for in a SQL string on a single quote character
    in_str = 0
    in_paren = False
    for c in line:
        if not in_paren and c != "(":
            continue
        elif not in_paren and c == "(":
            in_paren = True
        elif in_str == 0 and c == "'":
            in_str = 1
        elif in_str == 1 and c == "'":
            in_str = 2
        elif in_str == 2 and c == "'":
            fields[i] += "'"
            in_str = 1
        elif in_str == 2 and c == ",":
            in_str = 0
            i += 1
            fields[i] = ""
        elif in_str == 1 and c != "'":
            fields[i] += c
        elif in_str == 0 and c == ",":
            i += 1
            fields[i] = ""
        elif (in_str == 0 or in_str == 2) and c == ")":
            in_paren = False
            in_str = 0
            break
        elif in_str == 0:
            assert c not in [",", "'", ")"]
            fields[i] += c
        else:
            print("DEBUG: ", c, file=sys.stderr)
    assert in_str == 0
    assert not in_paren
    return fields


if __name__ == "__main__":
    for line in sys.stdin:
        print(process_line(line))
