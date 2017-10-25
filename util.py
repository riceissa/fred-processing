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


def mysql_number(x, typeconv=lambda x: x, factor=1):
    if not x:
        return "NULL"
    x = x.strip()
    x = x.replace(",", "")
    x = x.replace("%", "")
    if factor != 1:
        return str(typeconv(x) * factor)
    else:
        return str(typeconv(x))


def mysql_int(x, factor=1):
    return mysql_number(x, typeconv=int, factor=factor)


def mysql_float(x, factor=1):
    return mysql_number(x, typeconv=float, factor=factor)
