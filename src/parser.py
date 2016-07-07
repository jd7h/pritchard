#!/usr/bin/python

def parse_advisory(a):
	fields = ['Titel','Advisory ID', 'Versie', 'Kans', 'CVE ID', 'Schade', 'Uitgiftedatum', 'Toepassing', 'Versie(s)', 'Platform(s)', 'Samenvatting', 'Update', 'Gevolgen', 'Beschrijving', 'Mogelijke oplossingen', 'Hyperlinks', 'Vrijwaringsverklaring']
	values = []
	lhs = ""
	rhs = a
	for f in fields:
		splitresult = rhs.split(f,1)
		if len(splitresult)>1:
			print("Old:",splitresult[0])
			strippedstring = " ".join("".join(" ".join(splitresult[0].split()).split("\r")).split("\n"))
			print("New:",strippedstring)
			values.append(strippedstring)
			rhs = splitresult[1]
		else:
			print("Field",f,"not found in string.")
			values.append("")
			rhs = splitresult[0]
	for i in range(0,9):
		result = values[i].split(":",1)
		if len(result)>1:
			values[i] = result[1].strip()
	return values
