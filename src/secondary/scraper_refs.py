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
import logging
import datetime

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
            logging.warning("%s contains %s",u["url"],ext)
            return u

    logging.info("Scraping %s ...", u["url"])
    try:
        conn = urllib.request.urlopen(
            urllib.request.Request(u["url"], headers={
                'User-Agent': 'Pritchard/1.0 (data mining on security \
                advisories, http://github.com/jd7h/pritchard)'}),timeout=60)
    except urllib.error.HTTPError as error:
        # Return code error (e.g. 404, 501, ...)
        logging.debug("HTTP-code %s",error.code)
        u["status"] = error.code
    except Exception as e:
        logging.error("%s error for %s",type(e),u["url"])
        logging.debug("repr(e) = %s",repr(e))
        u["status"] = str(type(e))
    else:
        u["status"] = conn.getcode()
        logging.debug("HTTP-code %s",conn.getcode())
        try:
            logging.debug("Reading contents of %s",u["url"])
            if not conn.headers.get_content_charset() is None:
                u["content"] = conn.read().decode(conn.headers.get_content_charset())
            else:
                u["content"] = conn.read().decode()
        except Exception as e:
            logging.error("Read error for %s: %s",u["url"],type(e))
            logging.debug("repr(e) = %s",repr(e))
            u["status"] = str(u["status"]) + ", " + type(e)
    finally:
        return u

def scrape_references(references):
    """Take a set of references and scrape the urls of not-yet-scraped references"""
    logging.info("Scraping references...")
    already_visited = 0
    scraped = 0
    backup_interval = 10
    save_interval = 1000
    data_set_size = 1000
    for idx,ref in enumerate(references):
        # incrementing intervals for debugging
        if idx == 201:
            backup_interval = 50
            logging.info("Changing backup interval to %d",backup_interval)
        if idx == 751:
            backup_interval = 100
            logging.info("Changing backup interval to %d",backup_interval)
        if idx == 1501:
            backup_interval = 200
            logging.info("Changing backup interval to %d",backup_interval)
        # write intermediary results to backup file
        if scraped % backup_interval == 0 and scraped != 0:
            logging.info("Dumping %d new results to backup.",scraped)
            data_set.dump(references,"../data/temp/temp_",data_set_size)
        if idx % save_interval == 0 and idx != 0:
            logging.info("Dumping %d processed results to data set.",idx)
            data_set.dump(references,"../data/references_",data_set_size)
        # scrape unvisited urls
        if ref["status"] == 0:
            open_url(ref)
            scraped += 1
            time.sleep(1)
        else:
            already_visited += 1
    #print stats
    logging.info("Done scraping.")
    logging.info("Scraped: %d", scraped)
    logging.info("Already visited: %d", already_visited)
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
            logging.info("Loaded %d previously scraped advisories", len(advisories))

    # open earlier scraped references and urls
    old_references = []
    old_urls = []

    old_references = data_set.load(data_set_path)
    logging.info("Loaded %d previously scraped references", len(old_references))
    old_urls = [u["url"] for u in old_references]

    # make set of new urls and 
    # check for http-prefix to avoid duplicates with and without http://
    new_urls = [url for url in set(url_extractor.get_all_urls(advisories))]
    for u in new_urls:
        if not ("http://" in u or "https://" in u):
            logging.warning("%s does not contains http:// or https://",u)
            logging.warning("adding http:// to %s",u)
            u = "http://" + u
    new_urls = [url for url in new_urls if url not in old_urls]
    
    new_references = [{'url':u, 'status':0, 'content':''} for u in new_urls]

    logging.info("%d old urls from datasets in %s",len(old_urls),data_set_path)
    logging.info("%d new urls from advisories in %s",len(new_urls),advisory_path)

    all_references = old_references + new_references
    
    return all_references

def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',filename='scraper_refs.log',level=logging.DEBUG)
    logging.info("------------ SCRAPER REFS -----------------")
    logging.info("Building data set.")
    data = build_url_set("primary_advisories.json","../data/references_*.json")
    logging.info("Start scraping phase.")
    scrape_references(data)
    return data

if __name__ == "__main__":
    main()
