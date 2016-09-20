import glob
import json

def load(path):
    # open the earlier results                                                   
     data = []                                                                    
     data_set_paths = glob.glob(path)                      
     # open them in order                                                         
     data_set_paths.sort(key=lambda path : int(path.split("_")[1].split(".")[0])) 
     print(data_set_paths)
     for path in data_set_paths:                                                  
         print("Opening",path)                                                    
         try:                                                                     
             with open(path,"r") as infile:                                       
                 data_set = json.load(infile)                                     
         except Exception as e:                                                   
             print(type(e))                                                       
             print(e)
             print("Error in dataset",path)                                       
             continue                                                             
         else:                                                                    
             data.extend(data_set)                                                
     print("Dataset contains",len(data),"records.")             

def dump(data,pathprefix,data_set_size=1000):                                                                  
     # dump data to seperate files to fix memory errors                                                                     
     nr_of_sets = math.floor(len(data)/data_set_size)                             
     print("Will dump to",nr_of_sets,"datasets.")                                 
                                                                                  
     # dump all datasets                                                          
     for i in range(0,nr_of_sets):                                                
         start = i * data_set_size                                                
         end = (1+i) * data_set_size                                              
         data_sub_set = data[start:end]                                           
         data_sub_set_nr = str(i)                                                 
         data_sub_set_name = pathprefix + data_sub_set_nr + ".json"    
         print("Dumping data[" + str(start) + ":" + str(end) + "] to " + data_sub_set_name)
         with open(data_sub_set_name,"w+") as outfile:                            
             json.dump(data_sub_set,outfile)                                      
                                                                                  
     # last dataset with leftovers                                                
     start = nr_of_sets * data_set_size                                           
     end = len(data)                                                              
     data_sub_set_name = pathprefix + str(nr_of_sets) + ".json"        
     data_sub_set = data[start:end]                                               
     print("Dumping data[" + str(start) + ":" + str(end) + "] to " + data_sub_set_name)
     with open(data_sub_set_name,"w+") as outfile:                                
         json.dump(data_sub_set,outfile)
