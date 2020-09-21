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

    def __eq__(self, other):
        return len(self.items) == len(other.items) and all(item in other.items for item in self.items)


class Node:
    def __init__(self, parent, nodeid, x: Xset, level):
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
        self.isactive = True

    def addChild(self, child: Xset):
        if child is None:
            print("child you are trying to add is null")
            raise NameError("child you are trying to add is null")
        elif type(child) is not Xset:
            print("child is not of Xset class")
            raise NameError("child is not of Xset class")
        else:
            self.nofchildren += 1
            childNode = Node(self, self.nofchildren, child, self.level + 1)
            self.children.append(childNode)
            self.updateMaxLevelExtension(self.level + 1)
            return childNode

    def deleteChild(self, child):
        self.children.remove(child)
        if len(
                self.children) == 0:  # when there are no children in the node maxlevel extension should be its level itself
            self.maxLevelExtension = self.level

    def getNumberOfChildren(self):
        return len(self.children)

    def updateMaxLevelExtension(self, maxlevel):
        if self.parent is None:
            self.maxLevelExtension = maxlevel
        else:
            self.maxLevelExtension = maxlevel
            self.parent.updateMaxLevelExtension(maxlevel)

    def increaseSupport(self):
        self.support += 1
        self.set.support += 1

    def __eq__(self, other):
        return self.set == other.set


class CandidateGraph:
    def __init__(self):
        self.root = Node(None, 0, Xset([]), 0)  # root node will have id 0 and empty set as the itemset
        self.levels = dict()
        self.levels[0] = [self.root]

    def getLevel(self, level):  # This should return the all the nodes in the given level
        if level in self.levels:
            return self.levels[level]  # To be implemented
        else:
            return None

    def getMaxLevel(self):
        return self.root.maxLevelExtension

    def addChild(self, parent, node):
        child = parent.addChild(node)
        newLevel = parent.level + 1
        if newLevel in self.levels:
            self.levels[newLevel].append(child)
        else:
            self.levels[newLevel] = [child]

    def deleteNode(self, node, level):
        node.parent.deleteChild(node)
        self.levels[level].remove(node)

    def removeAncestorsIfNecessary(self, node, level):
        if node.parent is not None and node.parent.maxLevelExtension < level:
            node.parent.isactive = False
            self.deleteNode(node.parent, node.parent.level)
            self.removeAncestorsIfNecessary(node.parent, level)


def computesupport(ck, database, k):
    for transaction in database:
        for ksubset in Xset(transaction).ksubset(k):
            tempnode = None
            for node in ck:
                if all(item in node.set.items for item in list(ksubset)):
                    tempnode = node
                    break
            if tempnode is not None:
                node.increaseSupport()


def extendPrefixTree(ck, candidateGraph, level):
    # we need to iterate a copy of Ck since we might remove values from the list
    ckCopy = ck.copy()
    for leaf in ckCopy:
        if leaf.parent.isactive:
            for childLeaf in leaf.parent.children:
                a = leaf.id
                b = childLeaf.id
                if b > a:
                    xabUnion = leaf.set.items + childLeaf.set.items
                    xab = list(set(xabUnion))
                    xabSet = Xset(xab)
                    allXjExists = True
                    for xj in xabSet.ksubset(len(xab) - 1):
                        isXjExists = False
                        for node in ckCopy:
                            if all(item in node.set.items for item in list(xj)):
                                isXjExists = True
                                break
                        if isXjExists is False:
                            allXjExists = False
                            break
                    if allXjExists:
                        candidateGraph.addChild(leaf, xabSet)
            if leaf.getNumberOfChildren() == 0:
                candidateGraph.deleteNode(leaf, leaf.level)
                candidateGraph.removeAncestorsIfNecessary(leaf, leaf.level)


# testing method
def test(database):
    for row in database:
        print(row)
    a = ['0023', '0043', '2322', '9890']
    ax = Xset(a)
    print(ax.ksubset(2))
    ff = ax.ksubset(1)
    print(type(ff[0]))

    tupletolist = list(ff[0])
    print(all(item in a for item in tupletolist))

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

    n0 = Node(None, 0, Xset([]), 0)
    print(n0.id)
    print(n0.level)
    print(n0.maxLevelExtension)
    print(n0.nofchildren)
    print(n0.set.items)
    print(n0.support)
    print(n0.children)

    a1 = n0.addChild(Xset(['a']))
    b1 = n0.addChild(Xset(['b']))

    print(n0.id)
    print(n0.level)
    print(n0.maxLevelExtension)
    print(n0.nofchildren)
    print(n0.set.items)
    print(n0.support)
    print(n0.children)

    print("-----------------------")

    for child in n0.children:
        print(child.id)
        print(child.level)
        print(child.maxLevelExtension)
        print(child.nofchildren)
        print(child.set.items)
        print(child.support)
        print(child.children)
        print("-----------------------")

    n0.deleteChild(a1)
    print(n0.maxLevelExtension)

    for child in n0.children:
        print(child.id)
        print(child.level)
        print(child.maxLevelExtension)
        print(child.nofchildren)
        print(child.set.items)
        print(child.support)
        print(child.children)
        print("-----------------------")

    n0.deleteChild(b1)
    print(n0.maxLevelExtension)

    candidateGraph = CandidateGraph()
    candidateGraph.addChild(candidateGraph.root, Xset(['a']))
    candidateGraph.addChild(candidateGraph.root, Xset(['b']))
    print(candidateGraph.getLevel(1))
    for n in candidateGraph.getLevel(1):
        print(n.id)

    testNode = candidateGraph.getLevel(1)[1]
    candidateGraph.deleteNode(testNode, testNode.level)

    print("+++++++++++++++++++++")
    for n in candidateGraph.getLevel(1):
        print(n.id)
    candidateGraph.addChild(candidateGraph.root, Xset(['c']))
    candidateGraph.addChild(candidateGraph.root, Xset(['b']))
    print("+++++++++++++++++++++")
    for n in candidateGraph.getLevel(1):
        print(n.id)
    print("--------------------------")
    dbtest = [['a', 'b'], ['a'], ['c']]
    computesupport(candidateGraph.getLevel(1), dbtest, 1)

    for n in candidateGraph.getLevel(1):
        print(n.support)

    candidateGraph.addChild(candidateGraph.getLevel(1)[0], Xset(['a', 'b']))
    candidateGraph.addChild(candidateGraph.getLevel(1)[0], Xset(['a', 'c']))

    for n in candidateGraph.getLevel(2):
        print(n.id)

    candidateGraph.addChild(candidateGraph.getLevel(2)[0], Xset(['a', 'b', 'c']))

    candidateGraph.removeAncestorsIfNecessary(candidateGraph.getLevel(2)[1], 3)


def apriori(database, itemset, minsup):
    F = []
    candidateGraph = CandidateGraph()

    for item in itemset:
        candidateGraph.addChild(candidateGraph.root, Xset([item]))

    k = 1
    while ((candidateGraph.getLevel(k) is not None) and (
            len(candidateGraph.getLevel(k)) != 0)):
        computesupport(candidateGraph.getLevel(k), database, k)
        # for n in candidateGraph.getLevel(1):
        #     print("Items: " + n.set.items + " support: " + str(n.support))
        for node in candidateGraph.getLevel(k).copy():
            if node.support >= minsup:
                F.append(node.set)
            else:
                candidateGraph.deleteNode(node, k)

        extendPrefixTree(candidateGraph.getLevel(k), candidateGraph, k)
        k = k + 1
        print("calculated candidate graph for level: ", k)

    print("Finished")
    return F  # To be implemented


def main():
    df = pd.read_csv('txn_wih_dpt_ids.csv', dtype={'Dept': np.str})  # read the department ids as strings

    print("Loaded txns with dpt ids")
    # following will contain the list of list that contains the dept ids of each transaction
    database = df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist()
    # test(database)

    # creating the itemset
    dpIddf = pd.read_csv('dept_id_toDeptName.csv', dtype={'DeptId': np.str})
    itemset = dpIddf['DeptId'].tolist()

    f = apriori(database, itemset, 20)
    for frequent in f:
        frequent.items.sort()
        print(frequent.items)

    f1 = filter(lambda x : len(x.items) >= 2, f)

    print("===========================")
    for frequent in f1:
        frequent.items.sort()
        print(frequent.items)

    # test2()


def test2():
    a1 = Xset(['a', 'b'])
    a2 = Xset(['a', 'b'])

    if a1 == a2:
        print("a1 wqual e2")

    n1 = Node(None, 0, a1, 0)
    n2 = Node(None, 0, a2, 0)

    if n1 == n2:
        print("n1 and n2 equal")


if __name__ == "__main__":
    main()