""" Read databases """
import pandas as pd
from sklearn import preprocessing

BREAST_CANCER_COIMBRA_DATASET="breast_cancer_coimbra"
GLASS_DATASET="glass"

def read_csv(filepath):
    return pd.read_csv(filepath)

def normalize_data(df):
    x = df.values
    x_transformed = preprocessing.MinMaxScaler().fit_transform(x)
    return pd.DataFrame(x_transformed, columns=df.columns, index=df.index)
