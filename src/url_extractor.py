#!/usr/bin/python

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import json
import os.path
import re
import pprint

def get_urls(advisory):
	return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', json.dumps(advisory))

def get_all_urls(advisories):
	urls = []
	for a in advisories:
		urls += get_urls(a)

	return urls

def main():
	advisories = []

	# we open our datafile
	if os.path.isfile("primary_advisories_set100.json"):
		with open("primary_advisories_set100.json","r") as infile:
			advisories = json.load(infile)
			print("Loaded",len(advisories),"previously scraped advisories.")

	
	#write all urls to file
	urls = get_all_urls(advisories)
		
	with open("urls.txt","w+") as outfile:
		outfile.write("\n".join(urls))
	
	return urls


if __name__ == "__main__":
	main()
