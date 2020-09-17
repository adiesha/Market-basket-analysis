import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib import rcParams


def edit(value):
    value.split(":")


def removeDeptName():
    df = pd.read_csv('txn_by_dept.csv')

    # removing department names from the Dept column
    df['Dept'] = df['Dept'].apply(lambda x: x.split(":")[0])
    print(df.head())
    df.to_csv('txn_wih_dpt_ids')


def createDeptIDToDeptmentNameCSV():
    df = pd.read_csv('txn_by_dept.csv')
    # print(df['Dept'].unique())
    # print(df['Dept'].nunique())

    # print(df.groupby('Dept').nunique())

    df3 = pd.DataFrame(df.Dept.unique(), columns=['Dept'])
    print(df3.head())
    print(df3.count())
    df4 = pd.DataFrame(df3.Dept.str.split(":", 1).tolist(), columns=['DeptId', 'DeptName'])
    print(df4.head())
    df4.to_csv('dept_id_toDeptName')


def main():
    print("hello world!")
    removeDeptName()
    createDeptIDToDeptmentNameCSV()


if __name__ == "__main__":
    main()
