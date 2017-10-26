#!/usr/bin/env python3

import requests
import os
import sys
from util import *


with open("apikey.txt", "r") as f:
    API_KEY = next(f).strip()


def get_tags_from_file():
    try:
        with open("fred_tags", "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []


def get_tags():
    tags_endpoint = "https://api.stlouisfed.org/fred/tags"
    tags = []
    count = 1  # This just has to be greater than 0

    # The API limits to 1000 tags per query, so keep bumping up the offset
    # until we get them all
    while len(tags) < count:
        r = requests.get(tags_endpoint, params={
            "api_key": API_KEY,
            "file_type": "json",
            "offset": len(tags),
        })
        j = r.json()
        tags.extend([x["name"] for x in j["tags"]])
        count = j["count"]

    with open("fred_tags", "w") as f:
        for tag in tags:
            f.write(tag + "\n")

    return tags


def get_series_names_for_tag(tag):
    tags_series_endpoint = "https://api.stlouisfed.org/fred/tags/series"
    result = []
    count = 1  # This just has to be greater than 0

    while len(result) < count:
        r = requests.get(tags_series_endpoint, params={
            "api_key": API_KEY,
            "file_type": "json",
            "tag_names": tag,
            "offset": len(result),
        })
        j = r.json()
        result.extend([x["id"] for x in j["seriess"]])
        count = j["count"]
        print(len(result), file=sys.stderr)

    return result


def get_all_series_names_from_file():
    try:
        with open("fred_series_names", "r") as f:
            return [(line.strip()[0], line.strip()[1]) for line in f]
    except FileNotFoundError:
        return []


def get_all_series_names(tags):
    result = []
    seen = set()

    with open("fred_series_names", "w") as f:
        for tag in tags:
            print("DOING", tag, file=sys.stderr)
            for s in get_series_names_for_tag(tag):
                if s not in seen:
                    result.append((tag, s))
                    f.write("{}\t{}\n".format(tag, s))
                    seen.add(s)
            f.flush()
            os.fsync(f.fileno())

    return result


def get_series_observations(series_name):
    r = requests.get("https://api.stlouisfed.org/fred/series", params={
        "api_key": API_KEY,
        "file_type": "json",
        "series_id": series_name,
    })
    j = r.json()
    title = j["seriess"][0]["title"]
    units = j["seriess"][0]["units"]

    endpoint = "https://api.stlouisfed.org/fred/series/observations"
    n = 0  # Track how many observations we have gotten
    count = 1  # This just has to be greater than 0

    while n < count:
        r = requests.get(endpoint, params={
            "api_key": API_KEY,
            "file_type": "json",
            "series_id": series_name,
            "offset": n,
        })
        j = r.json()
        for x in j["observations"]:
            n += 1
            yield {"date": x["date"],
                   "value": x["value"],
                   "database_version": x["realtime_start"],
                   "units": units,
                   "title": title}
        count = j["count"]


def print_sql_rows(series_name):
    insert_line = "insert into data(region, odate, database_url, database_version, data_retrieval_method, metric, units, value, notes) values"
    count = 0
    first = True
    for ob in get_series_observations(series_name):
        if first:
            print(insert_line)
        print("    " + ("" if first else ",") + "(" + ",".join([
            mysql_quote("United States?"),  # region
            mysql_string_date(ob["date"]),  # odate
            mysql_quote("https://research.stlouisfed.org/docs/api/fred/"),  # database_url
            mysql_quote(ob["database_version"]),  # database_version
            mysql_quote(""),  # data_retrieval_method
            mysql_quote(ob["title"]),  # metric
            mysql_quote(ob["units"]),  # units
            mysql_float(ob["value"]),  # value
            mysql_quote(""),  # notes
        ]) + ")")
        first = False
        count += 1
        if count > 5000:
            count = 0
            first = True
            print(";")
    if not first:
        print(";")


if __name__ == "__main__":
    # tags = get_tags_from_file()
    # if not tags:
    #     tags = get_tags()
    # series_names = get_all_series_names_from_file()
    # if not series_names:
    #     series_names = get_all_series_names(tags)
    print_sql_rows("GNPCA")
