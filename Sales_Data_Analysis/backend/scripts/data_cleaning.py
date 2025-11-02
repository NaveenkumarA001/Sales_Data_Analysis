import pandas as pd

def clean_data(df):
    # Remove missing values and duplicates
    df = df.dropna()
    df = df.drop_duplicates()
    return df
