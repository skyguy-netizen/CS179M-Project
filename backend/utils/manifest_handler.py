import pandas as pd

def retrieval(file):
    df = pd.read_csv(file, delimiter = ', ')
    matrix = df.to_numpy()
    print(matrix)