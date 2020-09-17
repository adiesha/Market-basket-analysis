import itertools
from itertools import chain, combinations

import numpy as np
import pandas as pd


class Xset:
    def __init__(self, itemlist):
        self.items = itemlist
        self.support = 0

    def ksubset(self, ksize):
        if ksize is None:
            ksize = len(self.items)
        return list(itertools.combinations(self.items, ksize))

    # return the power set except the empty set
    # https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    def powerset(self):
        s = list(self.items)
        return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))

    def powersetWithEmptySet(self):
        s = list(self.items)
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


class Node:
    def __init__(self, parent, nodeid, x, level):
        self.parent = parent
        self.id = nodeid  # this is the sibling id determined by its parent
        self.nofchildren = 0  # this is the number of children a node has, this value should not be taken as the actual
        # number of children this node has, rather a index that we can use for naming the next child,
        # to get the number of children use the length of the children list
        self.set = x  # this is the itemset that belongs to the node. this should be a list of strings
        self.level = level
        self.children = []
        self.support = 0
        self.maxLevelExtension = level

    def addChild(self, child):
        if child is None:
            print("child you are trying to add is null")
        else:
            self.nofchildren += 1
            self.children.append(Node(self, self.nofchildren, child, self.level + 1))
            self.updateMaxLevelExtension(self.level + 1)

    def getNumberOfChildren(self):
        return len(self.children)

    def updateMaxLevelExtension(self, maxlevel):
        if self.parent is None:
            self.maxLevelExtension = maxlevel
        else:
            self.maxLevelExtension = maxlevel
            self.parent.updateMaxLevelExtension(maxlevel)


class CandidateGraph:
    def __init__(self):
        self.root = Node(None, 0, [], 0)  # root node will have id 0 and empty set as the itemset


    def getLevel(self, level):  # This should return the all the nodes in the given level
        None  # To be implemented

    def getMaxLevel(self):
        return self.root.maxLevelExtension

# def computesupport(X, D, level):
#     for row in D:
#         for x in X.powerset():


# testing method
def test(database):
    for row in database:
        print(row)
    a = ['0023', '0043', '2322', '9890']
    ax = Xset(a)
    print(ax.ksubset(1))
    ff = ax.ksubset(1)
    print(type(ff[0]))

    ff2 = ax.ksubset(3)
    print(ff2)

    ff3 = ax.powerset()
    print(ff3)

    for x in ff3[0]:
        print(x)

    for x in ff3[4]:
        print(x)

    ff4 = ax.powersetWithEmptySet()
    print(ff4)

    # creating the itemset
    dpIddf = pd.read_csv('dept_id_toDeptName.csv', dtype={'DeptId': np.str})
    itemset = dpIddf['DeptId'].tolist()
    print(itemset)
    print(len(itemset))
    # itemset size should be 160 and it is

    n0 = Node(None, 0, [], 0)
    print(n0.id)
    print(n0.level)
    print(n0.maxLevelExtension)
    print(n0.nofchildren)
    print(n0.set)
    print(n0.support)
    print(n0.children)

    n0.addChild(['a'])
    n0.addChild(['b'])

    print(n0.id)
    print(n0.level)
    print(n0.maxLevelExtension)
    print(n0.nofchildren)
    print(n0.set)
    print(n0.support)
    print(n0.children)

    print("-----------------------")

    for child in n0.children:
        print(child.id)
        print(child.level)
        print(child.maxLevelExtension)
        print(child.nofchildren)
        print(child.set)
        print(child.support)
        print(child.children)
        print("-----------------------")


def apriori():
    return None  # To be implemented


def main():
    df = pd.read_csv('txn_wih_dpt_ids.csv', dtype={'Dept': np.str})  # read the department ids as strings
    print(df.describe())
    print("Loaded txns with dpt ids")
    # following will contain the list of list that contains the dept ids of each transaction
    database = df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist()
    test(database)

    # print(database)

    # print(df.groupby(['POS Txn'])['POS Txn'].apply(list).values.tolist())
    # a = df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist()
    # b = df.groupby(['POS Txn'])['POS Txn'].apply(list).values.tolist()


if __name__ == "__main__":
    main()