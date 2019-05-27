#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
import STAT_ZONAL_SPECRTE

path = "/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed4_learn.sqlite"
#path = "/home/dahingerv/Documents/Iota/2018_S2_MaiNov/1504_Loiret/Results/learningSamples/Samples_region_1_seed0_learn.sqlite"
indice = 'ndvi'#en minuscule

conn = sqlite3.connect(path)
df = pd.read_sql_query("SELECT * FROM output", conn)

dfpar = df.groupby("originfid").mean()
dfpar.head()


# Garder la colonne irigation, puis la supprimer
irrig = dfpar['labcroirr']
dfpar.drop(['labcroirr'], axis='columns', inplace=True)


# Sélectionner les colonnes en fonction de l'indice souhaité, puis renommer les colonnes
df_indice = dfpar.filter(like=indice)
df_indice_col = df_indice.rename(columns=lambda x: x[-4:])


# Faire le cumul date par date
df_cumul = df_indice_col.cumsum(axis=1)
df_cumul.head()

# Ajouter la colonne irrigation
df_cumul['labcroirr']=irrig

# Calculer les moyennes et les écarts-types
df_cumul_mean= df_cumul.groupby("labcroirr").mean().T
#df_cumul_std= df_cumul.groupby("labcroirr").std().T

df_cumul_mean.columns = ["Maïs irrigué","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum_Nirr","Sunflower_Nirr","Peas"]
#df_cumul_std.columns = ["Maïs irrigué","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum_Nirr","Sunflower_Nirr","Peas"]


t = df_cumul_mean.index.values

X1 = df_cumul_mean["Maize_Nirr"]
X2 = df_cumul_mean["Maïs irrigué"]

sigma1,simag2=stats.t.interval(0.95,df_cumul_mean.T.shape[1]-1,loc=df_cumul_mean.T,scale=stats.sem(df_cumul_mean))
            confianceinf.append(globals()["_%s"% (i)])
            confiancesup.append(globals()["b_sup%s"% (i)])

sigma1 = df_cumul_std["Maize_Nirr"]
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
fig.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/CUMUL_Maize"+ indice+"ecartType_2017.png")


t = df_cumul_mean.index.values

X2 = df_cumul_mean["Soybean_Irr"]
X1 = df_cumul_mean["Soybean_Nirr"]

sigma1 = df_cumul_std["Soybean_Irr"]
sigma2 = df_cumul_std["Soybean_Nirr"]

fig, ax = plt.subplots(figsize=(20, 7))
ax.plot(t, X1,  label="Soja non irrigue", color='orange')
ax.plot(t, X2, label="Soja irrigue", color='blue')
ax.fill_between(t, X1+sigma1, X1-sigma1, facecolor='orange', alpha=0.2)
ax.fill_between(t, X2+sigma2, X2-sigma2, facecolor='blue', alpha=0.2)
ax.set_title(r'Cumul des '+ indice+' et intervalle $\pm \sigma$ en 2017')
ax.legend(loc='upper left')
ax.set_xlabel('Dates interpollees')
ax.set_ylabel('Cumul '+ indice+' moyen')
fig.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/CUMUL_soybean"+ indice+"ecartType_2017.png")


