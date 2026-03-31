import pandas as pd

def extract():
    df = pd.read_csv('data/vendas.csv')
    return df