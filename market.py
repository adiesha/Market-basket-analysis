import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib import rcParams
from itertools import permutations 
from itertools import combinations 

def BinaryMatrixSetup(df):
    #[n_entries, n_columns] =df.shape
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

def ComputeSupport_Kaveen(C_k, BinDB):
    D = BinDB.to_numpy()
    print(D)
    (n_t,n_i) = D.shape 
    print('Numberof transactions')
    print(n_t)
    print('Number of items')
    print(n_i)
    
    (n_X,k) = C_k.shape
    print('Number of k subsets')
    print(n_X)
    print('kth level')
    print(k)
  
    sup_X =  np.zeros(n_X) 
    for  i in range(n_t):
        # print('Transaction number')
        # print(i)
        i_t = np.where(D[i,:]==1)[0]
        print('Transcaction values')
        print(i_t)
        
        i_K = np.asarray(list(combinations(i_t,k)))
        print('item combinations per txn')
        print(i_K)
        
        print('number of permutations')
        n_i_K = len(i_K)
        print(n_i_K)
        for j in range(n_i_K):
            print(i_K[j])
            a =  C_k == i_K[j]
            print(a)
            if a.any:
                idx = np.where(a == True)[1]
                print(idx)
                sup_X[idx] = sup_X[idx] +1
            
            
    
    print(sup_X)
    return sup_X
    


def main():
    print("hello world!")
    df = pd.read_csv('txn_by_dept.csv')
    print(df.head())

    
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
    binaryM = BinaryMatrixSetup(df)
    
    k =2
    C_k = np.asarray(list(combinations(range(160),k)))
    print(C_k)
    sup_X = ComputeSupport_Kaveen(C_k,binaryM)
    
    return binaryM
if __name__ == "__main__":
    main()
