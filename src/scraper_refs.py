#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup
import json
import os.path

def main():
	if not os.path.isfile("data.txt"):
		print("Error: data.txt not found.")
		return 0
	with open ("data.txt","r") as infile:
	advisories = json.load(infile)
	print("Loaded",len(advisories),"advisories.")

if __name__ == "__main__":
	main()
