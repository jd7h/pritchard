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
    except Exception as e:
        print("Error for", u["url"],repr(e))
        u["status"] = repr(e)
    else:
        u["status"] = conn.getcode()
        try:
            u["content"] = conn.read()
        except Exception as e:
            print("Error for", u["url"],repr(e))
            u["status"] = str(u["status"]) + ", " + repr(e)
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
    data_set.dump(references,"../data/references_",data_set_size)
    return references

def build_url_set(advisory_path,data_set_path):
    """Open primary advisories, obtain all urls and scrape all those webpages."""
    advisories = []

    # we open our datafile with advisories
    # the advisories provide the urls for scraping
    if os.path.isfile(advisory_path):
        with open(advisory_path, "r") as infile:
            advisories = json.load(infile)
            print("Loaded", len(advisories), "previously scraped advisories.")

    # open earlier scraped references and urls
    old_references = []
    old_urls = []

    old_references = data_set.load(data_set_path)
    print("Loaded", len(old_references), "previously scraped references.")
    old_urls = [u["url"] for u in old_references]

    #make set of new urls
    new_urls = [url for url in set(url_extractor.get_all_urls(advisories)) if url not in old_urls]
    new_references = [{'url':u, 'status':0, 'content':''} for u in new_urls]

    print("old urls", len(old_urls))
    print("new urls", len(new_urls))

    all_references = old_references + new_references
    
    return all_references

def main():
    print("Building data set.")
    data = build_url_set("primary_advisories.json","../data/references_*.json")
    print("Start scraping phase.")
    scrape_references(data)
    return data

if __name__ == "__main__":
    main()
