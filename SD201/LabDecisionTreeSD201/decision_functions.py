
import math


def filetolist(file): #to transform file in list
    list=[]
    newlist=[]
    f=open(file, "r")
    for l in f:
        datas = [chiffres for chiffres in l.split(',')]
        list.append(datas)
    del list[0]
    for val in list:
        datas = [int(data) for data in val]
        newlist.append(datas)
    return newlist

#%%
def BuildDecisionTree(file, Nmin,dclass):
    tree=[]
    newlist =filetolist(file)
    A=[[[1,2],[2,3]],[[0,1],[1,2]]]    #list of constraints
    newlist1=[]
    newlist2=[]
    survivors=0                        #choose a root : Sex
    for val in newlist:
        if val[-1]==1:
            survivors+=1
    deads = len(newlist)-survivors
    gini = 1 -(survivors/len(newlist))**2 -(deads/len(newlist))**2
    
    for val in newlist:
                if val[0] ==0:
                    newlist1.append(val)
                else:
                    newlist2.append(val)
    tree.append(['node',1,0,0,[0],survivors,deads,gini]) #tree= list of list of type :
                                                        #[{node/leaf},{number of the node/leaf},{level},
                                                        #{ level of the constraint(only for node, 0 for Pclass, 1 for Embarked)},
                                                        #{Class(for leaf)/constraints(for node)}
                                                        #{nb of survivors}, {nb of deads},{gini}]

    
    BuildTree(newlist1,A,Nmin,2,dclass,tree)   #directed to the recursive function BuilTree
    BuildTree(newlist2,A,Nmin,3,dclass,tree)
    return tree
 


def BuildTree(list,A, Nmin, v, dclass,tree): 
    newlist1=[]
    newlist2=[]
    datalist=[]
    same=1
    level=int(math.floor(math.log(v)/math.log(2)))
    survivors=0
    for val in list:
        if val[-1]==1:
            survivors+=1
        if val[0:3]!=list[0][0:3]:
            same = 0
    deads = len(list)-survivors
    gini = 1 -(survivors/len(list))**2 -(deads/len(list))**2
    if v==6 or v==7:
        print(v, list)
    
    #leaf
    if survivors==0:
        tree.append(['leaf',v,level,0,survivors,deads,0])
        print(v,'Aucun survivant')
    elif survivors ==len(list):
        tree.append(['leaf',v,level,1,survivors,deads,0])
        print(v,'Que des survivants')
    elif same:
        if survivors>deads:
            tree.append(['leaf',v,level,1,survivors,deads,gini])
        else:
            tree.append(['leaf',v,level,0,survivors,deads,gini])
        print(v,'mêmes attributs')
    
    elif len(list)<Nmin:
        tree.append(['leaf',v,level,dclass,survivors,deads,gini])
        print(v,'Nmin atteint')
    


    #node
    else:
        
        for i, attribute in enumerate(A):
            for constraint in attribute:
                newlist1=[]
                newlist2=[]
                for val in list:
                    if val[i+1] in constraint:
                        newlist1.append(val)
                    else:
                        newlist2.append(val)
                if len(newlist1) > 0 and len(newlist2) > 0:
                    ginisplit =GINI(newlist1,newlist2)
                    datalist.append([ginisplit,newlist1,newlist2,i+1,constraint])
       
        datalist.sort()
        tree.append(['node',v,level,datalist[0][3],datalist[0][4],survivors,deads,gini])
        print(v,'Noeud')
                    
        newlist1,newlist2=datalist[0][1],datalist[0][2]
        BuildTree(newlist1,A,Nmin,2*v,dclass,tree)
        BuildTree(newlist2,A,Nmin,2*v+1,dclass,tree)



def GINI(datalist1,datalist2): #returns the gini split of a node correponding to the two new list
    n1=len(datalist1)
    n2=len(datalist2)
    n=n1+n2
    nclass01=0
    nclass02=0
    for val in datalist1:
        if val[3]==0:
            nclass01+=1
    gini1= 1 -(nclass01/n1)**2 -((n1-nclass01)/n1)**2
        
    for val in datalist2:
        if val[3]==0:
            nclass02+=1
    gini2= 1 -(nclass02/n2)**2 -((n2-nclass02)/n2)**2
    gini= (n1/n)*gini1 + (n2/n)*gini2
    return  gini


#%%

def takeSecond(val):
    return val[1]

def printDecisionTree(tree):
    tree.sort(key=takeSecond)
    features=['Sex','Pclass','Embarked']
    level=0
    for val in tree:
        if level != val[2]:
            level=val[2]
            print("\n")
        elif level !=0:
            print("**************")
            
            
            
        if val[1]==1:
            print("Root"+"\nLevel : ", val[2],"\nFeature : "+features[val[3]]+" ",val[4][0],"\nGini : ",val[-1])
        elif val[0]=='node':
            print("Intermediate"+"\nLevel : ", val[2],"\nFeature : "+features[val[3]]+" ",val[4][0],val[4][1],"\nGini : ",val[-1])
        else:
            print("leaf"+"\nLevel : ", val[2],"\nClass : ",val[3],"\nGini : ",val[-1])

def generalizationError(tree, alpha):
    n=0
    nbleaf=0    
    trainerror=0
    
    for val in tree:
        
        if val[0]=="leaf":
            nbleaf+=1
            n+=val[4]+val[5]
            if val[3]==0:
                trainerror+=val[4]
            else:
                trainerror+=val[5]
    generror = (trainerror + alpha*nbleaf)/n
    return generror
            
#%%
def pruneTree(tree,Nmax,Nmin, alpha):
    newtree=list([list(val) for val in tree]) #creates a new tree in order to modify it and compare the error with the original tree
    final=1
    n=len(tree)
    print('Nouvelle recursivité n:',n)
    if Nmax==0:
        return newtree

    for i in reversed(range(0,n-1)):
        if newtree[i][0]=='leaf' and newtree[i+1][0]=='leaf' and newtree[i][1]//2 == newtree[i+1][1]//2: #two leaves from the same father
            father = newtree[i][1]//2 #nb of the node of the father
            for val in newtree:
                if val[1] == father:
                    val[0]='leaf'
                    del val[3]
                    totalsurvivors=newtree[i][4]+newtree[i+1][4]
                    totaldeads=newtree[i][5]+newtree[i+1][5]
                    total = totaldeads+totalsurvivors
                    if totaldeads >= totalsurvivors or total<Nmin: #the class
                        val[3]=0
                    else:
                        val[3]=1
            newtree[i]='Null'
            newtree[i+1]='Null'
            
            newtree.remove('Null') #deletes the leaves under the father 
            newtree.remove('Null')
            if generalizationError(newtree, alpha)< generalizationError( tree, alpha):
                final =0
                print('recursivité')
                return(pruneTree(newtree,Nmax-1,Nmin, alpha))
                break
            else:
                final=1
                newtree=list([list(val) for val in tree])
                print('pas de recursivité')
             
    if final==1:
        return newtree
                
                
                
    
                
            
    