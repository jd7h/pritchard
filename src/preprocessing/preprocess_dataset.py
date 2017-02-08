#!/usr/bin/python

from pymongo import MongoClient
import re
import scipy.stats

def open_collection(collectionname):
    # open connection with mongodb
    # get advisories and references
    client = MongoClient()
    db = client.reference_test
    coll = db[collectionname]

    data = []
    cursor = coll.find()
    for d in cursor:
        data.append(d)
    client.close()

    return data

def save_collection(dataset,collectionname):
    for d in dataset:
        if '_id' in d.keys():
            d.pop('_id')
    # open connection with mongodb
    client = MongoClient()
    db = client.reference_test
    if collectionname not in db.collection_names():
        coll = db[collectionname]
        for d in dataset:
            print(coll.insert(d))
    else:
        print("Error! collection already exists!")

def create_dataset(adv,ref):

    ''''
    # problem: urls in references in advisories are not the same as in the scraped refs
    # fix: remove all "_id" keys and re-add urls to references
    for a in adv:
        a['_id'] = "" # anders werkt json serialize niet :/
        a['references'] = url_extractor.get_urls(a)
    '''

    # get reference classes from advisory classes

    # merge damage and risk rating into one class
    for a in adv:
        a['class'] = (a['chance'],a['damage'])
    classes = set([a['class'] for a in adv])

    for r in ref:
        r['class'] = []

    ''''
    #problem: previously, advisories had a string instead of list
    for a in adv:
        a['references'] = a['references'].split()
    ''''

    for a in adv:
        for url in a['references']:
            for r in [r for r in ref if r['url'] == url]:
                if a['class'] not in r['class']:
                    r['class'].append(a['class'])
    # check
    print("No class, 1 class, more than 1 class")
    print(
            len([r for r in ref if len(r['class']) < 1]),
            len([r for r in ref if len(r['class']) == 1]),
            len([r for r in ref if len(r['class']) > 1]))
    return adv,ref

# purge faulty records from dataset
def cleanup(ref):
    # load refs from mongodb
    # lose all with a different status than 200
    dataset = [r for r in ref if r['status'] == 200]
    # lose all with more than one class
    dataset = [d for d in dataset if len(d['class']) == 1]

    for inschaling in set([d['class'][0] for d in dataset]):
        print(inschaling,len([d for d in dataset if d['class'][0] == inschaling]))
    '''
        ('high', 'low') 10
        ('medium', 'medium') 4656
        ('low', 'medium') 568
        ('medium', 'low') 70
        ('low', 'high') 471
        ('high', 'high') 446
        ('high', 'medium') 971
        ('medium', 'high') 6547
    '''

# purge faulty words from bag-of-words (bow) of records
def cleanup_bow_refs(dataset):
    # cleanup words in references
    # remove all words with len < 3
    from nltk.corpus import stopwords
    stopwordlist = stopwords.words('english')
    pattern = '[a-zA-Z0-9]'
    minimal_occurence = 15
    
    # make a frequency list of all words over all reviews
    allwords = getallwords(dataset)
    frequencies = {}
    for d in dataset:
        for word in d['bow'].keys():
            if word not in frequencies.keys():
                frequencies[word] = d['bow'][word]
            else:
                frequencies[word] += d['bow'][word]

    for d in dataset:
        for word in list(d['bow'].keys()):
            pop = False
            if frequencies[word] < minimal_occurence:
                pop = True
            elif len(word) < 3:
                pop = True
            elif len(word) == 32 and re.search('[a-fA-F0-9]{32}',word) != None:
                pop = True
            elif len(word) > 32:
                pop = True
            # remove all words from english stopwords list
            elif word in stopwordlist:
                pop = True
            # remove all words that do not contains letters or numbers
            elif re.search(pattern,word) == None:
                pop = True
            if pop:
                print("Removing keyword:",word)
                d['bow'].pop(word)

    # remove references that have no valid words left (empty bag-of-words)
    print("removable references:", len([d for d in dataset if len(d['bow'].keys()) < 1]))
    dataset = [d for d in dataset if len(d['bow']) > 0]
    
def getallwords(dataset):
    return list(set([w for d in dataset for w in d['bow'].keys()]))

def make_frequency_lists(dataset):
    allwords = getallwords(dataset)
    inschalingen = list(set([tuple(d['class']) for d in dataset]))
    
    frequencies_per_bin = {}  #nr of occurences of word w in all reviews in bin b
    frequencies = {} # nr of occurrences of word w in all reviews
    total_words_per_bin = {} # total nr of words per bin
    
    for i in inschalingen:
        frequencies_per_bin[i] = {}
        total_words_per_bin[i] = 0
    
    for word in allwords:
        frequencies[word] = 0
        for i in inschalingen:
            frequencies_per_bin[i][word] = 0

    for r in dataset:
        for word in r['bow'].keys():
            total_words_per_bin[r['class']] += r['bow'][word]
            frequencies[word] += r['bow'][word]
            frequencies_per_bin[r['class']][word] += r['bow'][word]

    totalwords = 0
    for i in inschalingen:
        totalwords += total_words_per_bin[i]
    
    return inschalingen, allwords, totalwords, total_words_per_bin, frequencies_per_bin, frequencies

# calculates p and pmf
# p: chance of encountering a word w (given all reviews)
# pmf: chance that we encounter word w freq_of_w_in_bin times in bin, given p[w]
# if pmf[w] > p[w] and pmf[w] > 0, this word is significantly interesting
def calc_chances(dataset):
    inschalingen, allwords, totalwords, total_words_per_bin, frequencies_per_bin, frequencies = make_frequency_lists(dataset)
    
    pmf = {}

    p = {} # p[w] is chance of encountering w in all reviews
    print("Calculating /p/ values.")
    for w in allwords:
        p[w] = frequencies[w] / float(totalwords)

    for i in inschalingen:
        print("Processing bin",i)
        pmf[i] = {}
        for w in allwords:
            #denotes the chance that we encounter a word as often as we do in this bin
            x = frequencies_per_bin[i][w]
            n = total_words_per_bin[i]
            chance = scipy.stats.binom.pmf(x,n,p[w])
            pmf[i][w] = chance
    return p,pmf

def significant_words_for_inschaling(p,pmf,inschaling):
    siglist = [(word,sig[inschaling][word]) for word in sig[inschaling] if sig[inschaling][word] > p[word] and sig[inschaling][word] > 0.0]
    siglist.sort(key=lambda x:x[1])
    return siglist
