# Databricks notebook source
1+1

# COMMAND ----------

X=map( lambda a : 2*a , [ 1 , 2 , 3 , 4 ] )

# COMMAND ----------

lines = sc.textFile("/FileStore/tables/steve.txt")

# COMMAND ----------

text_file = sc.textFile("/FileStore/tables/steve.txt")
print( lines.take(5) )

# COMMAND ----------

words = text_file.flatMap(lambda line : line.split(" "))
for a in words.take(5):
  print(a)

# COMMAND ----------

pairs = words.map( lambda s : ( s , 2) )
print(pairs.take(5))

# COMMAND ----------

# DBTITLE 1,On voit que cela affiche les double des occurrences pour chaque mot du texte steve.txt
counts = pairs.reduceByKey(lambda a, b : a + b)
for (count, word ) in counts.take(10):
  print ("%s : %i " % (count,word))

# COMMAND ----------
#%% The code which is expected
# DBTITLE 1,Question 1
text_file = sc.textFile("/FileStore/tables/steve.txt")
words = text_file.flatMap(lambda line : line.split(" "))
pairs = words.map(lambda s :(s, 1))
occurences = pairs.reduceByKey(lambda a, b : a + b)
for (word,occurence ) in occurences.collect():
  print ("%s : %i " % (word, occurence))


# COMMAND ----------
#%%
# DBTITLE 1,Question 2
text_file = sc.textFile("/FileStore/tables/steve.txt")
words = text_file.flatMap(lambda line : line.split(" "))
pairs = words.map(lambda s :(s, 1))
occurences = pairs.reduceByKey(lambda a, b : a + b)
newoccurences = occurences.map(lambda s : (s[1],s[0])).sortByKey(False).map(lambda s : (s[1],s[0])) #changes the tuples so that the occurence becomes the key, and then sorts the data
for (word, occurence) in newoccurences.take(5):
  print ("%s : %i " % (word, occurence))

# COMMAND ----------
#%%
# DBTITLE 1,Question 3
text_file = sc.textFile("/FileStore/tables/steve.txt")
words = text_file.flatMap(lambda line : line.split(" "))
newwords = words.filter(lambda word : len(word)>=5)

newpairs = newwords.map(lambda s :(s, 1))
occurences = newpairs.reduceByKey(lambda a, b : a + b)
occurences5 = occurences.map(lambda s : (s[1],s[0])).sortByKey(False).map(lambda s : (s[1],s[0]))
for (word, occurence) in occurences5.take(5):
  print ("%s : %i " % (word, occurence))



# COMMAND ----------
#%%
# DBTITLE 1,Question 4
def fonction(phrase): #function which permits to return the tuple (id,name) from each line of the data idslabels.txt
  id=""
  name=""
  i=0
  while phrase[i] !=  " " :
    id = id + phrase[i]
    i+=1

  name = phrase[i+1:]
  return (id,name)

    

# COMMAND ----------

# DBTITLE 0,Question 4
labels = sc.textFile("/FileStore/tables/idslabels.txt")
datalabels = labels.flatMap(lambda line : line.split("\n"))
datalabels = datalabels.map(fonction)


edges = sc.textFile("/FileStore/tables/edgelist.txt")
dataedges = edges.flatMap(lambda line : line.split("\n")) #splits the lines
dataedges = dataedges.map(lambda line : line[2:])   #deletes the two first lines
dataedges = dataedges.flatMap(lambda line : line.split(" "))  #splits into words

pairs = dataedges.map(lambda s :(s, 1))
occurences = pairs.reduceByKey(lambda a, b : a + b)
data = datalabels.join(occurences)


newdata=data.map(lambda s : (s[1][1],(s[0],s[1][0]))).sortByKey(False) #changes the tuples so that the occurence becomes the key, and then sorts the data
for (occurence,(id,name)) in newdata.take(10):
  print("%s : %i " % (name, occurence))




# COMMAND ----------


