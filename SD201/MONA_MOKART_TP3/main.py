# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 09:03:58 2020

@author: mokar
"""
import os
#os.chdir("C:/Users/mokar/Desktop/TELECOM/2A/SD201/LabDecisionTreeSD201")


import math
file1='data.csv'
file2='data2.csv'
import decision_functions as df
from decision_functions import BuildDecisionTree
from decision_functions import printDecisionTree
from decision_functions import generalizationError
from decision_functions import pruneTree
#%%

dclass=0
Nmin =5
decisiontree=BuildDecisionTree(file1,Nmin,dclass)
printDecisionTree(decisiontree)


#%%
print("Generalization error :", generalizationError( decisiontree, 0.5))

#%%
Nmax = len(decisiontree)//2 -1
Nmin =5
pruneddecisiontree=pruneTree(decisiontree,Nmax,Nmin,0.5)
printDecisionTree(pruneddecisiontree)
print("Generalization error :", generalizationError( pruneddecisiontree, 0.5))