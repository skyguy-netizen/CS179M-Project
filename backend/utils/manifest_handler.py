import pandas as pd

def set_file(file_):
    global file
    global matrix
    
    df = pd.read_csv(file_, header=None, delimiter = ', ', engine='python')
    matrix = df.to_numpy()
    file = df.to_string()

def get_file():
    global file
    return file