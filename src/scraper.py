#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup
import json
import os.path

def make_page_url(sourceurl,pagenumber):
	return sourceurl + "page=" + str(pagenumber)

def get_urls_from_page(sourceurl,pagenumber,baseurl):
	filename = make_page_url(sourceurl,pagenumber)

	# open url
	webpage = urllib.request.urlopen(filename)
	#D pagecontents = webpage.read()
	#D print(pagecontents)
	soup = BeautifulSoup(webpage, "html.parser")

	# find links and make list
	urllist = []
	#D to find: li.advisory-item > a
	for item in soup.find_all(class_ = 'advisoryitem'):
		url = item.a['href']
		if not url in urllist:
			urllist.append(baseurl + url)
			#D print("advisory url added to parse list")
		#D print(baseurl + url)
	return urllist

def get_adv_from_links(urllist,titlestring):
	# open link and find advisory
	advisories = {}
	for url in urllist:
		#D print("Opening url: ",url)
		soup = BeautifulSoup(urllib.request.urlopen(url),"html.parser")
		advisory = soup.find(class_="advisoryitem")

		
		advisoryid = ""
		for s in advisory.find("h2").strings:
			if titlestring in s:
				advisoryid = s.rstrip().lstrip()
				print("ID:",advisoryid)
		if advisoryid == "":
			print("Error: no advisory ID found")
		advisorytext = advisory.find("pre")
		advisories[advisoryid] = advisorytext.prettify()
		#D print(advisorytext)
	print(len(advisories),"advisories parsed from source.")
	print("done.")
	return advisories

def main():
	filename = ""
	baseurl = ""
	titlestring = ""

	# get parameters from file
	sourcefile = open('source',encoding='utf-8')
	starturl = sourcefile.readline().rstrip()
	baseurl = sourcefile.readline().rstrip()
	titlestring = sourcefile.readline().rstrip()
	sourcefile.close()

	advisories = {}
	if os.path.isfile("data.txt"):
		with open("data.txt","r") as infile:
			advisories.update(json.load(infile))
			print("Loaded previously scraped advisories.")

	new_adv = 0;

	for i in range(1,10):
		linklist = get_urls_from_page(starturl,i,baseurl)
		#D print("linklist:",linklist);
		new_advisories = (get_adv_from_links(linklist,titlestring))
		for key in new_advisories.keys():
			if key not in advisories:
				advisories[key]=new_advisories[key]
				new_adv+=1
	
	#for a in advisories:
	#	print(a,advisories[a][0:100])

	print(len(advisories), "advisories in database.")
	print(new_adv, "advisories added.")

	with open('data.txt', 'w+') as outfile:
		json.dump(advisories, outfile)

if __name__ == "__main__":
	main()
