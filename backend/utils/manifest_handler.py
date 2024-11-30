import pandas as pd

def retrieval(file):
    df = pd.read_csv(file, header=None, delimiter = ', ', engine='python')
    matrix = df.to_numpy()
    print(matrix)