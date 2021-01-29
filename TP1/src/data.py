""" Read databases """
import pandas as pd

BREAST_CANCER_COIMBRA_DATASET="breast_cancer_coimbra"
GLASS_DATASET="glass"

def read_csv(filepath):
    return pd.read_csv(filepath)
