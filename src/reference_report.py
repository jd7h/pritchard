#!/usr/bin/python
"""Generate reports from the set of scraped references"""

import json
import os.path
import filtered_filetypes
import data_set
import logging

def report_status(references):
    logging.info("Generating report for reference dataset of size %d",len(references))
    status_classes = set([ref["status"] for ref in references])
    
    division = {}
    for s in status_classes:
        division[s] = [ref for ref in references if ref["status"] == s]
    logging.info("Printing overview of results to stdout")
    for key in division.keys():
        print("{:40}{}".format(str(key)[:35],len(division[key])))
    total = len(references)
    scraped = len([x for x in references if x["status"] != 0])
    print("Total items",total)
    print("Checked so far",scraped)

    logging.info("Printing complete report to stdout")
    print("------------------------------")
    print("        Extended report")
    print("------------------------------")
    for key in division.keys():
        if key != 0 and key != 200:
            print(str(key)[:35])
            print("------------------------------")
            for fout in division[key]:
                print(fout["url"])
            print()
    return (status_classes,division)



def main():
    data = data_set.load("../data/references*.json")
    classes,division = report_status(data)
    return classes,division


if __name__ == "__main__":
    main()
