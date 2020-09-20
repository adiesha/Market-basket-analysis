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


def AssociationRules(F, minconf):
    Z = np.asarray(F[2:5]) # Modify according to frequency set
    print('Z values')
    print(Z)
    z_r = len(Z)
    print(z_r)
    for r in range(z_r):
        z_c = len(Z[r])
        for c in range(z_c):
            print('Element in Z') 
            print(Z[r][c])
            A = list(chain.from_iterable(combinations(Z[r][c],i) for i in range(1,len(Z[r][c]))))
            print("A set")
            print(A)

            while len(A) !=0:
                X = A[-1]
                print("X value")
                print(X)

                A.remove(X)
                print("A after removing X")
                print(A)

                #c = sup(Z[r][c])/sup(X)
                conf = 0.9    
                if conf >= minconf:
                    ZZ = list(Z[r][c])
                    print('ZZ')
                    print(ZZ)

                    print(list(X))
                    for i in range(len(X)):
                        if X[i] in ZZ :
                            Y = ZZ
                            Y.remove(X[i])
                    print('Y set')
                    print(Y)

                    print(X,'->',Y,'Support','Confidence:',conf)
                else:
                    W = list(chain.from_iterable(combinations(X,i) for i in range(1,len(X))))
                    print('W set')
                    print(W)
                    for i in range(len(W)):
                        if W[i] in A:
                            A.remove(W[i])
                    print('A after removing W set')
                    print(A)










def main():
    minconf = 0.8
    #F = candidategraph()
    F = np.asarray(list(combinations([1, 2, 3, 4, 5],r) for r in range(5)))
    for i in range(5):
        F[i] = list(combinations(['A', 'B', 'C', 'D', 'E'],i))
    # print(F)

    """ a = ['A', 'B', 'C', 'D', 'E']

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
    print(ff4) """
    

    

    #F = ([6 , 'B'], [5 ,'E', 'B''E' ])
    AssociationRules(F, minconf)

if __name__ == "__main__":
    main()