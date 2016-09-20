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

def fix_data_set(data,pathprefix,i):
    # this should become pathprefix_i.json, but there's a problem
    errorfile = open("../data/error/temp.json","w+")
    new_data = []
    weird_data = []
    for d in data:
        logging.debug("Trying to dump %s to json",d["url"])
        try:
            s = json.dump(d,errorfile)
        except Exception as e:
            logging.error("%s",repr(e))
            #logging.debug("------ contents of data point -----")
            #logging.debug("%s",str(d))
            #logging.debug("------ end of data point -----")
            weird_data.append(d)
        else:
            new_data.append(d)

    # log weird_data
    logging.info("------- Error inducing urls --------")
    for w in weird_data:
        logging.info("%s",w["url"])
    logging.info("------------------------------------")

    # dump new_data 
    data_sub_set_name = pathprefix + str(i) + ".json"
    logging.info("Dumping sanitized data set to %s",data_sub_set_name)
    outfile = open(data_sub_set_name,"w+")
    try:
        json.dump(new_data,outfile)
    except Exception as e:
        logging.error("%s during sanitation of dataset",repr(e))
        logging.warning("I give up, skipping this dataset")
        return

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
        outfile = open(data_sub_set_name,"w+")
        try:
            json.dump(data_sub_set,outfile)
        except TypeError as t:    
            logging.error("%s",repr(t))
            logging.warning("TypeError encountered, trying to fix the problem...")
            fix_data_set(data[start:end],pathprefix,i)
            continue
        except Exception as e:
            logging.error("%s",repr(e))
            logging.warning("Skipping this dataset")
            continue            

    # last dataset with leftovers
    start = nr_of_sets * data_set_size
    end = len(data)
    data_sub_set_name = pathprefix + str(nr_of_sets) + ".json"
    data_sub_set = data[start:end]
    logging.info("Dumping data[%d:%d] to %s",start,end,data_sub_set_name)

    outfile = open(data_sub_set_name,"w+")
    try:
        json.dump(data_sub_set,outfile)
    except TypeError as t:    
        logging.error("%s",repr(t))
        logging.warning("TypeError encountered, trying to fix the problem...")
        fix_data_set(data[start:end],pathprefix,i)
    except Exception as e:
        logging.error("%s",repr(e))
        logging.warning("Skipping this dataset")

    logging.info("Dumped data to %d files",nr_of_sets)
