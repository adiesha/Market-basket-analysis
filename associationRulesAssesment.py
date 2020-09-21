import itertools
import sys
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
        result = list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))
        result2 = []
        for i in result:
            temp = list(i)
            temp.sort()
            result2.append(temp)
        return result2

    def powersetWithEmptySet(self):
        s = list(self.items)
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

    def __eq__(self, other):
        return len(self.items) == len(other.items) and all(item in other.items for item in self.items)

    def print(self, dptIdToDptName):
        self.deptNames = []
        for item in self.items:
            self.deptNames.append(dptIdToDptName[item])
        return str(self.deptNames)


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


class Rules:
    def __init__(self, X, Y, Z, dtxn, max_conf_w):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.dtxn = dtxn
        self.support = Z.support
        self.rsup = self.support / dtxn
        self.conf = self.support / X.support
        self.lift = self.conf * self.dtxn / Y.support
        self.leverage = (Z.support / dtxn - (X.support * Y.support) / dtxn ** 2)
        self.interest = abs(1 - self.lift)
        self.improvement = self.conf - max_conf_w
        # self.rank = 0.5 * self.conf + 0.5 * abs(1 - self.lift)

    def print(self, dptNames):
        print(self.X.print(dptNames) + " -> " + self.Y.print(dptNames) + "\t" + str(self.conf) + "\t" + str(
            self.support) + "\t" + str(
            self.rsup) + "\t" + str(self.lift) + "\t" + str(self.leverage) + "\t" + str(self.interest) + "\t" + str(
            self.improvement))


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


def loadDptNames():
    dataframe = pd.read_csv('dept_id_toDeptName.csv', dtype={'DeptId': np.str})
    dptIdToName = dict()
    for index in dataframe.index:
        dptIdToName[dataframe['DeptId'][index]] = dataframe['DeptName'][index]
    return dptIdToName


def apriori(database, itemset, minsup):
    F = []
    candidateGraph = CandidateGraph()

    for item in itemset:
        candidateGraph.addChild(candidateGraph.root, Xset([item]))

    k = 1
    while ((candidateGraph.getLevel(k) is not None) and (
            len(candidateGraph.getLevel(k)) != 0)):
        computesupport(candidateGraph.getLevel(k), database, k)

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


def max_conf_W_subset(X, Y, Z, f, dtxn):
    W_SET = Xset(X.items).powerset()
    W_SET.pop()
    max = 0
    for i in range(len(W_SET)):
        a = f.index(Xset(W_SET[i]))
        W = f[a]
        YUW_SET = W.items + Y.items
        b = f.index(Xset(YUW_SET))
        YUW = f[b]
        confWtoY = YUW.support / W.support
        if confWtoY > max:
            max = confWtoY
    return max


def AssociationRules(f, minconf, dtxn):
    ruleset = []
    Z_set = filter(lambda x: len(x.items) >= 2, f)
    for Z in Z_set:

        A = Z.powerset()
        A.remove(A[-1])

        while len(A) != 0:
            A_max = A[-1]

            XsetTemp = Xset(list(A_max))

            a = f.index(XsetTemp)

            X = f[a]
            X.items.sort()

            A.remove(X.items)

            conf = Z.support / X.support

            if conf >= minconf:
                Y_set = Z.items.copy()

                for i in range(len(X.items)):
                    if X.items[i] in Y_set:
                        Y_set.remove(X.items[i])

                YsetTemp = Xset(list(Y_set))
                b = f.index(YsetTemp)
                Y = f[b]

                max_conf_W = max_conf_W_subset(X, Y, Z, f, dtxn)
                # print(X.items, '->', Y.items, 'Support', Z.support, 'Confidence:', conf)
                newRule = Rules(X, Y, Z, dtxn, max_conf_W)
                ruleset.append(newRule)
            else:

                W = Xset(X.items).powerset()

                for i in range(len(W)):
                    if W[i] in A:
                        A.remove(W[i])

    return ruleset


def main(argv):
    print("Please input <minsupp(int)> <minconf(float)> <krules(int)>")
    minsup = int(sys.argv[1])
    minconf = float(sys.argv[2])
    k = int(sys.argv[3])
    print('minconf:', minconf, ' minsup:', minsup, ' krules:', k)

    df = pd.read_csv('txn_wih_dpt_ids.csv', dtype={'Dept': np.str})  # read the department ids as strings

    print("Loaded txns with dpt ids")
    # following will contain the list of list that contains the dept ids of each transaction
    database = df.groupby(['POS Txn'])['Dept'].apply(list).values.tolist()
    # test(database)

    # creating the itemset
    dpIddf = pd.read_csv('dept_id_toDeptName.csv', dtype={'DeptId': np.str})
    itemset = dpIddf['DeptId'].tolist()

    F = apriori(database, itemset, minsup)

    rulesset = AssociationRules(F, minconf, len(database))
    dptNames = loadDptNames()
    print("Rule\tConf\tSupport\trSup\tlift\tLeverage\tInterest*\tImprovement")

    sortedlist = sorted(rulesset, key=lambda x: (x.interest, x.improvement, x.conf), reverse=True)
    if k > len(sortedlist):
        k = len(sortedlist)

    for i in range(0, k):
        print("Rank:", i + 1)
        sortedlist[i].print(dptNames)


if __name__ == "__main__":
    main(sys.argv[1:])
