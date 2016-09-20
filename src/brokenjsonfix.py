#!/usr/bin/python
import json

class FirstTenDict(dict):
    def __init__(self, pairs):
        super(FirstTenDict, self).__init__(pairs[:10])
    
    #aanroepen met
    #data = json.load(json_string, object_pairs_hook=FirstTenDict)


