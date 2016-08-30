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

def get_url_contents(advisory):
	urls = get_urls(advisory)
	if len(urls) > 0:
		links = []
		for u in urls:
			if ".pdf" in u:
				print("Skipping:",u,"\t(pdf)")
				break
			linkeditem = {}
			linkeditem['url'] = u
			try:
				print("Opening",u)
				webpagestr = urllib.request.urlopen(u).read().decode('utf-8') #webpage to string
				print("Success: opened",u)
				webpagestr = webpagestr.replace("<br>","</br>")
				print("Parsing",u)
				c = str(BeautifulSoup(webpagestr,"html.parser"))
				print("Success: parsed",u)
				linkeditem['content'] = c
				links.append(linkeditem)
			except urllib.error.URLError:
				print("Failed:",u,"\t(URLError)")
			except:
				print("Failed:",u,"\t(Unknown error") #fix this later
		advisory['related'] = links
	return advisory

def main():
	advisories = []

	# we open our datafile
	if os.path.isfile("primary_advisories_set1.json"):
		with open("primary_advisories_set1.json","r") as infile:
			advisories = json.load(infile)
			print("Loaded",len(advisories),"previously scraped advisories.")

	'''
	#write all urls to file
	urls = get_all_urls(advisories)
		
	with open("urls.txt","w+") as outfile:
		outfile.write("\n".join(urls))
	'''


	# add all related content to advisory
	for advisory in advisories:
		get_url_contents(advisory)

	# we write advisories to JSON-dump
	with open('secondary_advisories_set1.json', 'w+') as outfile:
		json.dump(advisories, outfile)

	return advisories


if __name__ == "__main__":
	main()
