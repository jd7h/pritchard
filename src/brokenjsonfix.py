#!/usr/bin/python
import json
import math

class FirstTenDict(dict):
    def __init__(self, pairs):
        super(FirstTenDict, self).__init__(pairs[:10])
    
def fix():
    with open("inter-references.json","r") as infile:
        data = json.load(infile,object_pairs_hook=FirstTenDict)

    return data

def main():
    data = fix()
    slecht = 0
    goed = 0
    complete = []
    incomplete = []
    for d in data:
        if d['status'] == 0:
            slecht += 1
            incomplete.append(d)
        else:
            goed += 1
            complete.append(d)

    # dump data to seperate files to fix memory errors
    data_set_size = 1000
    for i in range(0,floor(len(data)/data_set_size)):
        start = i * data_set_size
        end = (1+i) * data_size_size
        data_sub_set = data[start:finish]
        data_sub_set_nr = str(i)
        data_sub_set_name = "references_" + data_sub_set_nr
        print("Dumping data[" + str(start) + ":" + str(finish) + "] to " + data_sub_set_name)
        with open(data_sub_set_name,"w+") as outfile:
            json.dump(data_sub_set,outfile)

