import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib import rcParams


def main():
    print("hello world!")
    df = pd.read_csv('txn_by_dept.csv')
    # print(df.head())
    print(df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist())
    print(df.groupby(['POS Txn'])['POS Txn'].apply(list).values.tolist())
    a = df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist()
    b = df.groupby(['POS Txn'])['POS Txn'].apply(list).values.tolist()


if __name__ == "__main__":
    main()
