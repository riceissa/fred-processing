#!/usr/bin/env python3

import requests


with open("apikey.txt", "r") as f:
    API_KEY = next(f).strip()


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
    series_names = []
    count = 1  # This just has to be greater than 0

    while len(series_names) < count:
        r = requests.get(tags_series_endpoint, params={
            "api_key": API_KEY,
            "file_type": "json",
            "tag_names": tag,
        })
        j = r.json()
        series_names.extend([x["id"] for x in j["seriess"]])

    return series_names

def get_series(tags):
    all_series = []

    for tag in tags[:1]:
        ss = get_series_names_for_tag(tag)
        for s in ss:
            if s not in all_series:
                all_series.append(s)


if __name__ == "__main__":
    get_tags()
