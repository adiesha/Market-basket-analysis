import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib import rcParams

def BinaryMatrixSetup(df):
    [n_entries, n_columns] =df.shape
    temp = df.nunique()
    print('Number of unique elements in each column')
    print(temp)

    
    n_unique_Txn = temp.array[0]
    n_unique_ID =temp.array[2]
    
    print('Number of Unique transactions')
    print(n_unique_Txn)
    print('Number of Unique IDs')
    print(n_unique_ID)

    by_Txn = df.groupby('POS Txn')['ID']
    by_ID = df.groupby('ID')['POS Txn']
    
    # by_Dept = df.groupby('Dept')

    # print('First entries in all the Txn groups')
    # # print(by_Txn.first())
    # print('All the entries in a Txn groups')
    # #print(by_Txn.get_group(16120100160021008774))

    # print('First entries in all the ID groups')
    # print(by_ID.first())
    # print('All the entries in a ID groups')
    # print(by_ID.get_group(1))

    # print('All the entries in kth ID groups')
    # a = by_ID.groups[1]
    # print(a[0])

    # print('Accessing a entry in a group')
    # print(by_ID(1))

    binaryM = pd.DataFrame(0,index= range(n_unique_Txn),columns=range(n_unique_ID))
    
    # print(binaryM.head())
    
    
    t =0
    L = ['']
    for T, group in by_Txn:
        # print(T)
        L.append(str( T))
        t= t+1
        
    # print(L)
    
    i= 0
    H=['']
    for I, group in by_ID:
        H.append(str(I))
        g = group.array

        for T in range(g.size) :
            J = L.index(str(g[T]))      
            binaryM.iloc[J-1,i] =1
        i=i+1 
    
    binaryM.columns = H[1:161]
    binaryM.index =L[1:2065]
   
    print(binaryM.head(5))
    
    # print(binaryM.iloc[1500:1510,159])
    return binaryM

def main():
    print("hello world!")
    df = pd.read_csv('txn_by_dept.csv')
    print(df.head())

    binaryM = BinaryMatrixSetup(df)
    #print(df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist())
    #print(df.groupby(['POS Txn'])['POS Txn'].apply(list).values.tolist())
    #a = df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist()
    #b = df.groupby(['POS Txn'])['POS Txn'].apply(list).values.tolist()

    # print(df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist())
    # print(df.groupby(['POS Txn']).head())
    # print(df.groupby(['POS Txn'])['Dept'].head())
    # print(df.count())
    # print(df.groupby(['POS Txn']).count())
    # print(df.columns)
    # print(df.groupby(['POS Txn'])['POS Txn'].head())

if __name__ == "__main__":
    main()
