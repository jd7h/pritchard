#!/usr/bin/python
"""Parses raw string advisories to dictionary structure"""
import json
import os.path
import html
import logging

def parse_advisory(s):
    """Parse a raw string advisory to a dictionary"""
    # fields from the raw advisories
    fields = ['<pre>', 'Titel', 'Advisory ID', 'Versie', 'Kans',
              'CVE ID', 'Schade', 'Uitgiftedatum', 'Toepassing',
              'Versie(s)', 'Platform(s)', 'Update', 'Samenvatting',
              'Gevolgen', 'Beschrijving', 'Mogelijke oplossingen',
              'Hyperlinks', 'Vrijwaringsverklaring']
    # fields that we want to use in our records
    fields2 = ['header', 'title', 'id', 'version', 'chance', 'CVE',
               'damage', 'date', 'application', 'application_version',
               'platform', 'update', 'summary', 'consequences',
               'description', 'solution', 'references', 'footer1']
    lhs = ""
    rhs = s
    record = {}
    previousfield = 0 # variable that stores which field we encountered last

    #Ugly but handy: because we use len(fields), the last field is not saved
    #(we save the last encountered field, which is at most i-1).
    #This is okay because the last field (Vrijwaringsverklaring and beyond)
    #does not contain data

    for i in range(0, len(fields)):
        logging.debug("splitting on %s", fields[i])
        splitresult = rhs.split(fields[i], 1) # split the string with field names as separator
        if len(splitresult) < 2: # if we don't find the separator
            record[fields2[i]] = "" # then the next field is not part of the record
        else:
            lhs, rhs = splitresult
            lhs = "".join(lhs.split("\r\n      ")) #sanitize the string from line breaks in urls
            lhs = " ".join("".join(" ".join(lhs.split()).split("\r")).split("\n")) #sanitize the string from whitespace and breaks
            if i > 0:
                record[fields2[previousfield]] = html.unescape(lhs)
                previousfield = i

    # sanitize colons from values
    for i in range(1, 11):
        record[fields2[i]] = "".join(record[fields2[i]].split(":", 1)).strip() #split on first semi-colon, join list, remove all leading and trailing whitespace

    # split "Schade" in rating and description
    splitresult = record['damage'].split(" ", 1)
    if len(splitresult) > 1:
        record['damage'], record['damage_description'] = splitresult

    # set date to int
    date = int(record['date'])
    if date > 20100000 and date < 20200000:
        record['date'] = int(record['date'])
    else:
        logging.error("invalid date in record %s: %s", record['id'], record['date'])

    # set version to int
    record['version'] = int(record['version'].split('.',1)[1])

    return record

def parse(advisories):
    """parse a list of raw string advisories to a list of dictionaries"""
    logging.info("parsing %d raw advisories", len(advisories))
    records = []
    for adv in advisories:
        records.append(parse_advisory(advisories[adv]))
    return records

def main():
    """
    Open raw data, parse all string advisories to dictionary
    and write the result to a JSON-file.
    """
    # logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: parser_adv %(message)s',filename='../pritchard.log',level=logging.INFO)

    advisories = {}
    raw_filename = "../../data/primary.json"
    parsed_filename = "../../data/primary_parsed.json"

    # open data.json
    if os.path.isfile(raw_filename):
        with open(raw_filename, "r") as infile:
            advisories.update(json.load(infile))
            logging.info("Loaded %d raw advisories for parsing from %s", len(advisories), raw_filename)

    # parse all advisories from data.json
    records = parse(advisories)

    # write advisories to another JSON-dump
    logging.info("Writing %d parsed advisories to %s", len(records), parsed_filename)
    with open(parsed_filename, 'w+') as outfile:
        json.dump(records, outfile)

    return advisories, records

if __name__ == "__main__":
    main()
