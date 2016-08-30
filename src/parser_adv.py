#!/usr/bin/python

import json
import os.path
import html

# parses a raw advisory in string format s to a dictionary structure record
def parse_advisory(s):
	# fields from the raw advisories
	fields = ['<pre>','Titel','Advisory ID', 'Versie', 'Kans', 'CVE ID', 'Schade', 'Uitgiftedatum', 'Toepassing', 'Versie(s)', 'Platform(s)','Update', 'Samenvatting', 'Gevolgen', 'Beschrijving', 'Mogelijke oplossingen', 'Hyperlinks', 'Vrijwaringsverklaring','-----BEGIN','restfooter']
	# fields that we want to use in our records
	fields2 = ['header','title','id','version','chance','CVE','damage','date',
		'application','application_version','platform','update','summary','consequences',
		'description','solution','references','footer1','footer2','footer3']
	lhs = ""
	rhs = s
	record = {}
	previousfield = 0 # variable that stores which field we encountered last
	
	for i in range(0,len(fields)-1):
		#print("D: Splitting on",fields[i])
		splitresult = rhs.split(fields[i],1) # split the string with field names as separator
		if len(splitresult)<2: # if we don't find the separator				
			record[fields2[i]] = "" # then the next field is not part of the record
		else:
			lhs,rhs = splitresult	
			#print("D: Left:",lhs)
			lhs = "".join(lhs.split("\r\n      ")) #sanitize the string from unwanted line breaks in urls
			lhs = " ".join("".join(" ".join(lhs.split()).split("\r")).split("\n")) #sanitize the string from whitespace and breaks
			#print("D: Right:",rhs)
			if i>0:
				record[fields2[previousfield]]=html.unescape(lhs)
				previousfield = i

	# sanitize colons from values
	for i in range(1,11):
		record[fields2[i]] = "".join(record[fields2[i]].split(":",1)).strip() #split on first semi-colon, join list, remove all leading and trailing whitespace

	# split "Schade" in rating and description
	splitresult = record['damage'].split(" ",1)
	if len(splitresult)>1:
		record['damage'],record['damage_description'] = splitresult

	return record

# parse a list of raw string advisories to a list of dictionaries
def parse(advisories):
	print("Parsing",len(advisories),"advisories.")
	records = []
	for adv in advisories:
		records.append(parse_advisory(advisories[adv]))
	return records	

def main():
	advisories = {}

	# open data.json
	if os.path.isfile("rawdata_set1.json"):
		with open("rawdata_set1.json","r") as infile:
			advisories.update(json.load(infile))
			print("Loaded",len(advisories),"raw advisories for preprocessing.")

	# parse all advisories from data.json
	records = parse(advisories)

	# write advisories to another JSON-dump
	with open('primary_advisories.json', 'w+') as outfile:
		json.dump(records, outfile)

	return advisories,records

if __name__ == "__main__":
	main()
