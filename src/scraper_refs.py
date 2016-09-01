#!/usr/bin/python
"""Parse referenced htmlpages from advisories"""
import urllib.request
import urllib.error
import json
import os.path
import time
import url_extractor

# betere aanpak
# verzamel alle links die moeten worden gescrapet: url en referencing advisories
# bepaal alle domeinen
# scrape om en om, wissel tussen domeinen en doe 3 seconden tussen elk request 

def open_url(u):
    """
    Given an url, open the url
    and register status code and contents
    """
    if u["status"] == 0:
        try:
            conn = urllib.request.urlopen(
                urllib.request.Request(u["url"], headers={
                    'User-Agent': 'Pritchard/1.0 (data mining on security \
                    advisories, http://github.com/jd7h/pritchard)'}))
        except urllib.error.HTTPError as error:
            # Return code error (e.g. 404, 501, ...)
            u["status"] = error.code
            return u
        except urllib.error.URLError as error:
            # Not an HTTP-specific error (e.g. connection refused)
            u["status"] = "URLError"
            return u
        else:
            u["status"] = conn.getcode()
            u["content"] = conn.read().decode('utf-8')
            return u
    else:
        return u #todo: register some kind of error

def scrape_references(references):
    """Take a set of references and scrape the urls of not-yet-scraped references"""
    already_visited = 0
    scraped = 0
    for ref in references:
        if ref["status"] == 0:
            open_url(ref)
            scraped += 1
            time.sleep(3)
        else:
            already_visited += 1
    print("Done scraping.")
    print("Scraped:", scraped)
    print("Already visited:", already_visited)
    return references

def main():
    """Open primary advisories, obtain all urls and scrape all those webpages."""
    advisories = []

    # we open our datafile
    if os.path.isfile("primary_advisories.json"):
        with open("primary_advisories.json", "r") as infile:
            advisories = json.load(infile)
            print("Loaded", len(advisories), "previously scraped advisories.")

    old_urls = []
    old_references = []

    # open earlier scraped urls
    if os.path.isfile("references.json"):
        with open("references.json", "r") as infile:
            old_references = json.load(infile)
            print("Loaded", len(old_references), "previously scraped references.")
            old_urls = [u["url"] for u in old_references]

    #make set of new urls
    new_urls = [url for url in set(url_extractor.get_all_urls(advisories)) if url not in old_urls]
    new_references = [{'url':u, 'status':0, 'content':''} for u in new_urls]

    print("old urls", len(old_urls))
    if len(old_urls) != 0:
        print(old_urls[0])
    print("new urls", len(new_urls))
    if len(new_urls) != 0:
        print(new_urls[0])

    all_references = old_references + new_references

    scrape_references(all_references[:20])

    # write the references to JSON-dump
    with open('references.json', 'w+') as outfile:
        json.dump(all_references, outfile)

    return 0


if __name__ == "__main__":
    main()
