import pandas as pd
from flask import jsonify

def set_file(file_):
    global file
    global matrix
    
    df = pd.read_csv(file_, header=None, delimiter = ', ', engine='python')
    matrix = df.to_numpy()
    matrix = matrix.tolist()
    file = matrix

def get_file():
    global file
    return file