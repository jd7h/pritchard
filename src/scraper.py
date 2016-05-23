#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup

filename = ""
baseurl = ""
titlestring = ""

# get filename from file
sourcefile = open('source',encoding='utf-8')
filename = sourcefile.readline()
baseurl = sourcefile.readline().rstrip()
titlestring = sourcefile.readline().rstrip()
sourcefile.close()

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
