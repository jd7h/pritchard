import glob
import math
import json
import logging

def load(path):
    logging.info('Opening %s',path)
    data = []
    data_set_paths = glob.glob(path)
    # open them in order
    data_set_paths.sort(key=lambda path : int(path.split("_")[1].split(".")[0]))
    logging.debug('Found files in %s: %s',path, str(data_set_paths))
    for p in data_set_paths:
        logging.info('Opening %s',p)
        try:
            with open(p,"r") as infile:
                data_set = json.load(infile)
        except Exception as e:
            logging.error("%s",repr(e))
            logging.error("Error with dataset %s",p)
            continue
        else:
            data.extend(data_set)
            logging.info("Dataset contains %d records",len(data))
    return data

def dump(data,pathprefix,data_set_size=1000):
    logging.info("Dumping data of length %d",len(data))
    logging.info("Target path is %s with max size %d",pathprefix,data_set_size)
    nr_of_sets = math.floor(len(data)/data_set_size)

    # dump all datasets
    for i in range(0,nr_of_sets):
        start = i * data_set_size
        end = (1+i) * data_set_size
        data_sub_set = data[start:end]
        data_sub_set_nr = str(i)
        data_sub_set_name = pathprefix + data_sub_set_nr + ".json"
        logging.info("Dumping data[%d:%d] to %s",start,end,data_sub_set_name)
        with open(data_sub_set_name,"w+") as outfile:
           json.dump(data_sub_set,outfile)

    # last dataset with leftovers
    start = nr_of_sets * data_set_size
    end = len(data)
    data_sub_set_name = pathprefix + str(nr_of_sets) + ".json"
    data_sub_set = data[start:end]
    logging.info("Dumping data[%d:%d] to %s",start,end,data_sub_set_name)
    with open(data_sub_set_name,"w+") as outfile:
        json.dump(data_sub_set,outfile)
    logging.info("Dumped data to %d files",nr_of_sets)
