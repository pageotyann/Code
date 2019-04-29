#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
import STAT_ZONAL_SPECRTE

# In[2]:


path = "/home/dahingerv/Documents/Iota/2017_S2/Loiret_2803/Results/learningSamples/Samples_region_1_seed0_learn.sqlite"
#path = "/home/dahingerv/Documents/Iota/2018_S2_MaiNov/1504_Loiret/Results/learningSamples/Samples_region_1_seed0_learn.sqlite"
indice = 'ndwi'#en minuscule


# In[3]:


conn = sqlite3.connect(path)
df = pd.read_sql_query("SELECT * FROM output", conn)

# In[4]:


dfpar = df.groupby("originfid").mean()
dfpar.head()


# In[5]:


# Garder la colonne irigation, puis la supprimer
irrig = dfpar['irrigation']
dfpar.drop(['irrigation'], axis='columns', inplace=True)


# In[6]:


# Sélectionner les colonnes en fonction de l'indice souhaité, puis renommer les colonnes
df_indice = dfpar.filter(like=indice)
df_indice_col = df_indice.rename(columns=lambda x: x[-4:])


# In[7]:


# Faire le cumul date par date
df_cumul = df_indice_col.cumsum(axis=1)
df_cumul.head()


# In[8]:


# Ajouter la colonne irrigation
df_cumul['irrigation']=irrig


# In[9]:


# Calculer les moyennes et les écarts-types
df_cumul_mean= df_cumul.groupby("irrigation").mean().T
df_cumul_std= df_cumul.groupby("irrigation").std().T
df_cumul_mean.columns = ["Maïs non irrigué","Maïs irrigué"]
df_cumul_std.columns = ["Maïs non irrigué","Maïs irrigué"]


# In[10]:


#df_cumul_mean.plot(title='Cumul des NDVI en 2018', color = ['gold', 'blue'])


# In[12]:


t = df_cumul_mean.index.values

X1 = df_cumul_mean["Maïs non irrigué"]
X2 = df_cumul_mean["Maïs irrigué"]

sigma1 = df_cumul_std["Maïs non irrigué"]
sigma2 = df_cumul_std["Maïs irrigué"]

fig, ax = plt.subplots(figsize=(20, 7))
ax.plot(t, X1,  label="Mais non irrigue", color='orange')
ax.plot(t, X2, label="Mais irrigue", color='blue')
ax.fill_between(t, X1+sigma1, X1-sigma1, facecolor='orange', alpha=0.2)
ax.fill_between(t, X2+sigma2, X2-sigma2, facecolor='blue', alpha=0.2)
ax.set_title(r'Cumul des '+ indice+' et intervalle $\pm \sigma$ en 2017')
ax.legend(loc='upper left')
ax.set_xlabel('Dates interpollees')
ax.set_ylabel('Cumul '+ indice+' moyen')
#plt.savefig("CUMUL_"+ indice+"ecartType_2017.png")


# In[ ]:




