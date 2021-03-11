import os
#os.chdir("C:/Users/mokar/Desktop/TELECOM/2A/SD201/LabDecisionTreeSD201")
file1='data.csv'
file2='data2.csv'
try:
	from decision_functions import BuildDecisionTree
	BuildDecisionTree(file1,5,0)
	print('BuildDecisionTree loaded!')
	print('----')
except Exception as e:
	raise e

try:
	from decision_functions import printDecisionTree
	printDecisionTree(BuildDecisionTree(file1,5,0))
	print('printDecisionTree loaded!')
	print('----')
except Exception as e:
	raise e

try:
	from decision_functions import generalizationError
	generalizationError(BuildDecisionTree(file1,5,0),0.5)
	print('generalizationError loaded!')
	print('----')
except Exception as e:
	raise e

try:
	from decision_functions import pruneTree
	pruneTree(BuildDecisionTree(file1,5,0),len(BuildDecisionTree(file1,5,0))//2 -1,5,0.5)
	print('pruneTree loaded!')
	print('----')
except Exception as e:
	raise e