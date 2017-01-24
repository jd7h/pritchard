#!/usr/bin/python
"""Scraper for primary advisories"""

import urllib.request
import json
import os.path
from bs4 import BeautifulSoup
import logging

def make_page_url(sourceurl, pagenumber):
    """Combine source-url and page-number to form a valid url"""
    return sourceurl + "page=" + str(pagenumber)

def get_urls_from_page(sourceurl, pagenumber, baseurl):
    """
    Get all links to a primary advisory
    from a html-page that contains a list of advisory-links
    """
    filename = make_page_url(sourceurl, pagenumber)

    # open url
    try:
        logging.debug("opening %s", filename)
        webpage = urllib.request.urlopen(
            urllib.request.Request(filename, headers={
                'User-Agent': 'Pritchard/1.0 (data mining on security \
                advisories, http://github.com/jd7h/pritchard)'}),timeout=60)
    except Exception as e:
        logging.error("%s error for %s",type(e),filename)
        logging.error("repr(e) = %s",repr(e))
    try:
        logging.debug("parsing %s", filename)
        soup = BeautifulSoup(webpage, "html.parser")
    except:
        logging.error("can't parse %s", filename)

    # find links and make list
    urllist = []
    for item in soup.find_all(class_='advisoryitem'):
        url = item.a['href']
        if not url in urllist:
            urllist.append(baseurl + url)
    return urllist

def get_adv_from_links(urllist, titlestring):
    """
    Obtains all advisories from a list of advisory links

    urllist -- a list with links to primary advisories
    titlestring -- a string that indicates the advisory
    """
    # open link and find advisory
    advisories = {}
    for url in urllist:
        try:
            logging.debug("opening %s", url)
            webpage = urllib.request.urlopen(
                urllib.request.Request(url, headers={
                    'User-Agent': 'Pritchard/1.0 (data mining on security \
                    advisories, http://github.com/jd7h/pritchard)'}),timeout=60)
        except Exception as e:
            logging.error("%s error for %s",type(e),url)
            logging.error("repr(e) = %s",repr(e))

        try:
            soup = BeautifulSoup(webpage, "html.parser")
            logging.debug("parsing %s", url)
        except:
            logging.error("Error: can't parse %s", url)
            break

        advisory = soup.find(class_="advisoryitem")

        advisoryid = ""
        for s in advisory.find("h2").strings:
            if titlestring in s:
                advisoryid = s.rstrip().lstrip()
                logging.debug("ID: %s", advisoryid)
        if advisoryid == "":
            logging.error("Error: no advisory ID found in advisory")
        advisorytext = advisory.find("pre")
        advisories[advisoryid] = advisorytext.get_text()
    logging.debug("%d advisories parsed from source", len(advisories))
    logging.debug("done obtaining advisories from urllist")
    return advisories

def main():
    """
    Load previously scraped advisories,
    and scrape all new advisories given a range of pagenumbers.
    Finally, write old and new advisories to a json-file.
    """
    # logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: scraper_adv %(message)s',filename='../pritchard.log',level=logging.DEBUG)

    # get parameters from file
    baseurl = ""
    titlestring = ""
    sourcefile = open('scraper_adv.config', encoding='utf-8')
    starturl = sourcefile.readline().rstrip()
    baseurl = sourcefile.readline().rstrip()
    titlestring = sourcefile.readline().rstrip()
    sourcefile.close()

    advisories = {}
    archive_filename = "../../data/primary.json"

    # load advisories we already scraped
    if os.path.isfile(archive_filename):
        with open(archive_filename, "r") as archive:
            advisories.update(json.load(archive))
            logging.info("Loaded %d previously scraped advisories from %s", len(advisories), archive_filename)

    new_adv = 0

    # scrape advisory links from list page
    # then scrape new advisories from advisory links
    minpage = 1
    maxpage = 5
    logging.debug("Scraping raw primary advisories, pages %d to %d", minpage, maxpage)
    for i in range(minpage,maxpage):
        linklist = get_urls_from_page(starturl, i, baseurl)
        new_advisories = (get_adv_from_links(linklist, titlestring))
        for key in new_advisories.keys():
            if key not in advisories:
                advisories[key] = new_advisories[key]
                new_adv += 1

    logging.info("%d new raw primary advisories found", new_adv)

    # we write advisories to JSON-dump
    with open(archive_filename, 'w+') as archive:
        json.dump(advisories, archive)
    logging.info("%d new advisories added", new_adv)
    logging.info("%d raw primary advisories in %s", len(advisories), archive_filename)

    return advisories


if __name__ == "__main__":
    main()
