#!/usr/bin/python

import json
import os.path
import html

def parse_advisory(s):
	fields = ['<pre>','Titel','Advisory ID', 'Versie', 'Kans', 'CVE ID', 'Schade', 'Uitgiftedatum', 'Toepassing', 'Versie(s)', 'Platform(s)','Update', 'Samenvatting', 'Gevolgen', 'Beschrijving', 'Mogelijke oplossingen', 'Hyperlinks', 'Vrijwaringsverklaring','-----BEGIN','restfooter']
	lhs = ""
	rhs = s
	record = {}
	previousfield = 0 # variable that stores which field we encountered last
	
	for i in range(0,len(fields)-1):
		#print("D: Splitting on",fields[i])
		splitresult = rhs.split(fields[i],1) # split the string with field names as separator
		if len(splitresult)<2: # als de sep niet gevonden is				
			record[fields[i]] = "" # then the next field is not part of the record
		else:
			lhs,rhs = splitresult	
			#print("D: Left:",lhs)
			lhs = "".join(lhs.split("\r\n      ")) #sanitize the string from unwanted line breaks in urls
			lhs = " ".join("".join(" ".join(lhs.split()).split("\r")).split("\n")) #sanitize the string from whitespace and breaks
			#print("D: Right:",rhs)
			if i>0:
				#if field[previousfield] in ['Titel','Advisory ID', 'Versie', 'Kans', 'CVE ID', 'Schade', 'Uitgiftedatum', 'Toepassing', 'Versie(s)', 'Platform(s)']:
				#	lhs = "".join(lhs.split(" : ")) # sanitize 
				record[fields[previousfield]]=html.unescape(lhs)
				previousfield = i

	# sanitize colons from values
	for i in range(1,11):
		record[fields[i]] = "".join(record[fields[i]].split(":",1)).strip() #split on first semi-colon, join list, remove all leading and trailing whitespace

	# split "Schade" in rating and description
	splitresult = record['Schade'].split(" ",1)
	if len(splitresult)>1:
		record['Schade'],record['Schade description'] = splitresult

	return record

def parse(advisories):
	print("Parsing",len(advisories),"advisories.")
	records = []
	for adv in advisories:
		records.append(parse_advisory(advisories[adv]))
	return records	

def main():
	advisories = {}

	# we open data.txt
	if os.path.isfile("data.txt"):
		with open("data.txt","r") as infile:
			advisories.update(json.load(infile))
			print("Loaded",len(advisories),"previously scraped advisories.")

	records = parse(advisories)

	# we write advisories to JSON-dump
	with open('primary_advisories.txt', 'w+') as outfile:
		json.dump(records, outfile)

	return advisories,records

if __name__ == "__main__":
	main()
