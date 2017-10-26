#!/usr/bin/env python3


def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def mysql_number(x, typeconv=lambda x: x, factor=1, replace=",%"):
    if not x:
        return "NULL"
    x = x.strip()
    for char in replace:
        x = x.replace(char, "")
    if factor != 1:
        return str(typeconv(x) * factor)
    else:
        return str(typeconv(x))


def mysql_int(x, factor=1, replace=",%"):
    return mysql_number(x, typeconv=int, factor=factor, replace=replace)


def mysql_float(x, factor=1, replace=",%"):
    return mysql_number(x, typeconv=float, factor=factor, replace=replace)


def mysql_string_date(x):
    """
    Return x as a string of the form "YYYYMMDD". This allows for representing a
    wider range of dates than is supported in MySQL's date type ('1000-01-01'
    to '9999-12-31'). Just the year can be stored as "YYYY0000", and just the
    year and month can be stored as "YYYYMM00". The input x should be an
    integer representing the year or a string of the form "YYYY", "YYYY-MM", or
    "YYYY-MM-DD".
    """
    x = str(x)
    if "-" not in x:
        assert len(x) <= 4, x
        return mysql_quote(("0" * (4 - len(x))) + x + "0000")
    if len(x) == len("YYYY-MM"):
        lst = x.split("-")
        return mysql_quote(lst[0] + lst[1] + "00")
    if len(x) == len("YYYY-MM-DD"):
        return mysql_quote("".join(x.split("-")))
