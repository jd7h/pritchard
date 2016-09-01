#!/usr/bin/python
"""Generate reports from the set of scraped references"""

import json
import os.path
import filtered_filetypes

def report_status(references):
    status_classes = set([ref["status"] for ref in references])
    division = {}
    for s in status_classes:
        division[s] = [ref for ref in references if ref["status"] == s]
    return (status_classes,division)

def main():
    
    references = json.load(open("inter-references.json", "r"))
    classes,division = report_status(references)
    for key in division.keys():
        print("{:20}{}".format(str(key),len(division[key])))
    total = len(references)
    scraped = len([x for x in references if x["status"] != 0])
    print("Total items",total)
    print("Checked so far",scraped)

    print("------------------------------\n\Extended report")
    print("------------------------------")
    for key in division.keys():
        if key != 0 and key != 200:
            print(str(key))
            print("---------------------")
            for fout in division[key]:
                print(fout["url"])
            print()
    return classes,division


if __name__ == "__main__":
    main()
