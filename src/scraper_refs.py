#!/usr/bin/python

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import json
import os.path
import re
import pprint
import url_extractor

# betere aanpak
# verzamel alle links die moeten worden gescrapet: url en referencing advisories
# bepaal alle domeinen
# scrape om en om, wissel tussen domeinen en doe 3 seconden tussen elk request. 

# based on: http://stackoverflow.com/questions/1726402/in-python-how-do-i-use-urllib-to-see-if-a-website-is-404-or-200
def open_url(u):
	try:
		conn = urllib.request.urlopen(urllib.request.Request(u["url"],headers={'User-Agent': 'Pritchard/1.0 (data mining on security advisories, http://github.com/jd7h/pritchard)'}))
	except urllib.error.HTTPError as e:
		# Return code error (e.g. 404, 501, ...)
		u["status"] = e.code
		return u	
	except urllib.error.URLError as e:
		# Not an HTTP-specific error (e.g. connection refused)
		u["status"] = "URLError"
		return u
	else:
		u["status"] = conn.getcode()
		u["content"] = conn.read().decode('utf-8')
		return u


def main():
	advisories = []

	# we open our datafile
	if os.path.isfile("primary_advisories_set100.json"):
		with open("primary_advisories_set100.json","r") as infile:
			advisories = json.load(infile)
			print("Loaded",len(advisories),"previously scraped advisories.")

	#make set of urls
	urls = set(url_extractor.get_all_urls(advisories))
	urls = [{'url':u,'status':0,'content':''} for u in urls]
	
	for u in urls[10:20]:
		open_url(u)

	for u in urls[10:20]:
		print(u["url"],u["status"],u["content"][:100])
	
	'''
	# we write advisories to JSON-dump
	with open('secondary_advisories_set100.json', 'w+') as outfile:
		json.dump(advisories, outfile)
	'''

	return 0


if __name__ == "__main__":
	main()
