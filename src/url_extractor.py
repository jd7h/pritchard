#!/usr/bin/python
"""Module for extracting urls from primary advisories"""

import json
import os.path
import re
import url_marker
import logging

def get_urls(advisory):
    """Given an advisory (dictionary), return a list with contained urls."""
    urls = re.findall(url_marker.URL_REGEX_NO_NAKED, json.dumps(advisory))
    for u in urls:
         if not ("http://" in u or "https://" in u):
             logging.warning("%s does not contains http:// or https://",u)
             logging.warning("adding http:// to %s",u)
             u = "http://" + u
    return urls

def get_all_urls(advisories):
    """Given a list of advisories, return a list with all contained urls."""
    urls = []
    for advisory in advisories:
        urls += get_urls(advisory)

    return urls

def main():
    """
    Load the primary advisories, extract all urls,
    write them to a json-file, and return the list of urls
    """

    advisories = []

    # we open our datafile
    if os.path.isfile("primary_advisories.json"):
        with open("primary_advisories.json", "r") as infile:
            advisories = json.load(infile)
            print("Loaded", len(advisories), "previously scraped advisories.")


    #write all urls to file
    urls = get_all_urls(advisories)

    with open("urls.txt", "w+") as outfile:
        outfile.write("\n".join(urls))
    with open("urls.json", "w+") as outfile:
        json.dump(urls, outfile)

    return urls


if __name__ == "__main__":
    main()
