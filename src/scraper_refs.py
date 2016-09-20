#!/usr/bin/python
"""Parse referenced htmlpages from advisories"""
import urllib.request
import urllib.error
import json
import os.path
import time
import url_extractor
import filtered_filetypes
import glob
import math
import data_set

# betere aanpak
# verzamel alle links die moeten worden gescrapet: url en referencing advisories
# bepaal alle domeinen
# scrape om en om, wissel tussen domeinen en doe 3 seconden tussen elk request 

def open_url(u):
    """
    Given an url, open the url
    and register status code and contents
    """
    # filter on certain filetypes
    exclude = filtered_filetypes.FILTERED_FILETYPES
    for ext in exclude:
        if ext in u["url"]:
            u["status"] = ext
            print(u["url"],"contains",ext,"\tskipping...")
            return u

    if not ("http://" in u["url"] or "https://" in u["url"]):
        u["url"] = "http://" + u["url"]

    print("Scraping", u["url"], "...")
    try:
        conn = urllib.request.urlopen(
            urllib.request.Request(u["url"], headers={
                'User-Agent': 'Pritchard/1.0 (data mining on security \
                advisories, http://github.com/jd7h/pritchard)'}))
    except urllib.error.HTTPError as error:
        # Return code error (e.g. 404, 501, ...)
        u["status"] = error.code
    except urllib.error.URLError as error:
        # Not an HTTP-specific error (e.g. connection refused)
        u["status"] = "URLError"
    except:
        u["status"] = "Unknown error"
    else:
        u["status"] = conn.getcode()
        try:
            u["content"] = conn.read().decode('utf-8')
        except:
            print("Read error for", u["url"])
            u["status"] = str(u["status"]) + ", read error"
    finally:
        return u

def scrape_references(references):
    """Take a set of references and scrape the urls of not-yet-scraped references"""
    print("Scraping references...")
    already_visited = 0
    scraped = 0
    backup_interval = 100
    save_interval = 1000
    data_set_size = 1000
    for idx,ref in enumerate(references):
        # write intermediary results to backup file
        if scraped % backup_interval == 0 and scraped != 0:
            print("Dumping",scraped,"new results to backup.")
            data_set.dump(references,"../data/temp/temp_",data_set_size)
        if idx % save_interval == 0 and idx != 0:
            print("Dumping",idx,"processed results to data set.")
            data_set.dump(references,"../data/references_",data_set_size)
        # scrape unvisited urls
        if ref["status"] == 0:
            open_url(ref)
            scraped += 1
            time.sleep(3)
        else:
            already_visited += 1
    #print stats
    print("Done scraping.")
    print("Scraped:", scraped)
    print("Already visited:", already_visited)
    return references

def first_time():
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
    #if len(old_urls) != 0:
    #    print(old_urls[0])
    print("new urls", len(new_urls))
    #if len(new_urls) != 0:
    #    print(new_urls[0])

    all_references = old_references + new_references
    
    scrape_references(all_references)

    # write the references to JSON-dump
    with open('references.json', 'w+') as outfile:
        json.dump(all_references, outfile)

    return 0

def continue_scraping():
    # we want to continue scraping after an earlier version crashed
    # we have inbetween results in ../data/

    # open the earlier results
    data = data_set.load("../data/references*.json")
    # and continue
    #data = scrape_references(data)

def main():
    continue_scraping()

if __name__ == "__main__":
    main()
