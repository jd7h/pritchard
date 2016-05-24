#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup

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

	linklist = get_urls_from_page(starturl,1,baseurl)
	advisories = get_adv_from_links(linklist,titlestring)
	
	for a in advisories:
		print(a,advisories[a][0:100])

if __name__ == "__main__":
	main()
