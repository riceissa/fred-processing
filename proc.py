#!/usr/bin/env python3

import requests
import os


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
        for tag in tags[:1]:
            for s in get_series_names_for_tag(tag):
                if s not in seen:
                    result.append((tag, s))
                    f.write("{}\t{}\n".format(tag, s))
                    seen.add(s)
            f.flush()
            os.fsync(f.fileno())

    return result


if __name__ == "__main__":
    tags = get_tags_from_file()
    if not tags:
        tags = get_tags()
    series_names = get_all_series_names_from_file()
    if not series_names:
        series_names = get_all_series_names(tags)
