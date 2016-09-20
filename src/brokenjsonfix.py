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

def score(data):
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
    print("current score")
    print("goed:",goed)
    print("slecht:",slecht)
    return goed,slecht,complete,incomplete

def dump(data):
    # dump data to seperate files to fix memory errors
    data_set_size = 1000
    nr_of_sets = math.floor(len(data)/data_set_size)
    print("Will dump to",nr_of_sets,"datasets.")
    
    # dump all datasets
    for i in range(0,nr_of_sets):
        start = i * data_set_size
        end = (1+i) * data_set_size
        data_sub_set = data[start:end]
        data_sub_set_nr = str(i)
        data_sub_set_name = "../data/references_" + data_sub_set_nr + ".json"
        print("Dumping data[" + str(start) + ":" + str(end) + "] to " + data_sub_set_name)
        with open(data_sub_set_name,"w+") as outfile:
            json.dump(data_sub_set,outfile)
    
    # last dataset with leftovers
    start = nr_of_sets * data_set_size
    end = len(data)
    data_sub_set_name = "../data/references_" + str(nr_of_sets) + ".json"
    data_sub_set = data[start:end]
    print("Dumping data[" + str(start) + ":" + str(end) + "] to " + data_sub_set_name)
    with open(data_sub_set_name,"w+") as outfile:
        json.dump(data_sub_set,outfile)

'''
def main():
    data = fix()
    score(data)
    dump(data)
'''
