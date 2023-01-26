#!/usr/bin/env python
# coding: utf-8

# In[79]:


import pandas as pd


# In[80]:


pd.__version__


# In[81]:


df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)


# In[82]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# In[83]:


from sqlalchemy import create_engine


# In[84]:


engine = create_engine('postgresql://nnesco:nnesco100@localhost:5433/ny_taxi')


# In[85]:


engine.connect()


# In[86]:


print(pd.io.sql.get_schema(df, name='yellow_tripdata', con=engine))


# In[87]:


df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)


# In[76]:


df = next(df_iter)


# In[69]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# In[70]:


df


# In[71]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[88]:


get_ipython().run_line_magic('time', "df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')")


# In[ ]:


from time import time

while True:
    t_start = time()
    df = next(df_iter)
    
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
    
    t_end = time()
    print('inserted another chunk..., took %.3f seconds' % (t_end - t_start))


# In[ ]:




