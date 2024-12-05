import pandas as pd
import models.cargo

def set_file(file_):
    global file
    global matrix
    
    list = []
    df = pd.read_csv(file_, header=None, delimiter = ', ', engine='python')
    matrix = df.to_numpy()
    file = df.to_string()
    
    for i in matrix:
        position = i[0]
        weight = i[1]
        container_name = i[2]
        obj = models.cargo.Cargo(container_name, position)
        list.append(obj)
        models.cargo.Cargo.set_weight(obj,weight)
        
            
def set_name(name):
    global file_name
    file_name = name

def get_file():
    global file
    return file

def get_name():
    global file_name
    return file_name