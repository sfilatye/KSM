# pd.read_sql is extremely slow on my computer when 'ORDER BY Random()' is used
# The method below is much faster
# Generates 5 million randomly chosen lines from the database and saves them in a pickle file
# as a pandas data frame
import sqlite3 as sql
import pandas as pd
import numpy as np

sql_conn = sql.connect('./database.sqlite')
c=sql_conn.cursor()
c.execute("SELECT Count(*) FROM May2015 ")
N=c.fetchone()[0]
print N
## N=10
numbers=np.random.choice(N,5000000,replace=False)
numbers.sort()
##print numbers
k_max=len(numbers)
print 'max number=',max(numbers)
Data=list()
i=0
k=0
for row in c.execute("SELECT subreddit, body,score,controversiality, distinguished FROM May2015 "):
  if not i%100000: print 'i=',i
#  print 'i=',i
  if i==numbers[k]:
    k+=1
    Data.append(row)
#    print 'k=',k
    if k>=k_max: break
    if not k%10000: print 'k=',k
  i+=1
df=pd.DataFrame(Data,columns=['subreddit','body','score','controversiality','distinguished'])
df['index']=numbers
df.to_pickle("Data5000000.p")

