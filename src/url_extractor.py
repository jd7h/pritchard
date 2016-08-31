#!/usr/bin/python

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import json
import os.path
import re
import pprint
import url_marker

def get_urls(advisory):
	return re.findall(url_marker.URL_REGEX_NO_NAKED, json.dumps(advisory))

def get_all_urls(advisories):
	urls = []
	for a in advisories:
		urls += get_urls(a)

	return urls

def main():
	advisories = []

	# we open our datafile
	if os.path.isfile("primary_advisories.json"):
		with open("primary_advisories.json","r") as infile:
			advisories = json.load(infile)
			print("Loaded",len(advisories),"previously scraped advisories.")

	
	#write all urls to file
	urls = get_all_urls(advisories)
		
	with open("urls.txt","w+") as outfile:
		outfile.write("\n".join(urls))
	with open("urls.json","w+") as outfile:
		json.dump(urls,outfile)
	
	return urls


if __name__ == "__main__":
	main()
