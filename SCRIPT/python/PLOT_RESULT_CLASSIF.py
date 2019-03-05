#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:44:18 2019

@author: pageot
"""



# =============================================================================
# Parametrisation des PATH
# =============================================================================
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np 
import seaborn as sns
import os


d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/"

# =============================================================================
# Plot Resul Classif  
# ===========================================================================

dfall=pd.DataFrame()
dfaccu=pd.DataFrame()
dfrapp=pd.DataFrame()
dffsc=pd.DataFrame()
names_df=["Classe","Accur","Rappel","F_score","Confusion_classe"]
names_dfs=["index","Classe","Accur","Rappel","F_score","Confusion_classe","step","mean_Accur","std_accu","mean_rappel","std_rappel","mean_Fscore","std_F_score"]
nombre_de_classe=17

for j in os.listdir(d["data_file"]):
    print (j)
    for i in os.listdir(d["data_file"] +j):
        print (i)
        df=pd.read_csv(d["data_file"]+j+"/"+i+"/"+"RESULTS.txt",sep='\|',skiprows=int(19))
        df.columns=names_df
        df1=df.drop([0])
        df1=df1.reset_index()
        origin=pd.DataFrame({'step':j},index=[0],dtype="category")
        origindup=pd.DataFrame(np.repeat(origin.values,df.shape[0]),dtype="category")
        df1["step"]=origindup
        accu=df1["Accur"].str.split(expand=True)
        accu.drop([1],axis=1,inplace=True)
        dfaccu=dfaccu.append(accu).astype(float)
        rap=df1["Rappel"].str.split(expand=True)
        rap.drop([1],axis=1,inplace=True)
        dfrapp=dfrapp.append(rap).astype(float)
        Fsc=df1["F_score"].str.split(expand=True)
        Fsc.drop([1],axis=1,inplace=True)
        dffsc=dffsc.append(Fsc).astype(float)
        dfall=dfall.append(df1)

data=pd.concat([dfall,dfaccu,dfrapp,dffsc],axis=1)
data.columns=names_dfs
# =============================================================================
#  plot comparer les run  
# =============================================================================
plt.figure(figsize=(10,10))
sns.set(style="darkgrid")
sns.set_context('paper')
sns.barplot(DF["step"],DF["mean_rappel"],yerr=DF["std_rappel"])## Comparer la précisoon mean total entre plusieurs step
plt.xticks(np.arange(len(os.listdir(d["data_file"]))), df1.step ,rotation=45)

# =============================================================================
# Plot visualisation run[i] par classe
# =============================================================================
plt.figure(figsize=(10,10))
sns.set(style="darkgrid")
sns.set_context('paper')
sns.barplot(DF["Classe"][0:nombre_de_classe],DF["mean_Accur"][0:nombre_de_classe])
y_pos=np.arange(df1.shape[0])
plt.xticks(np.arange(df1.shape[0]), df1.Classe ,rotation=45)
label=round(DF["mean_Accur"][0:nombre_de_classe],2)
for i in y_pos:
    plt.text(x = y_pos[i]-0.2 , y = DF["mean_Accur"][0:17][i], s = label[i], size = 11)

# =============================================================================
# Plot comparer les Accur entre classse entre run
# =============================================================================
plt.figure(figsize=(20,20))
sns.set(style="darkgrid")
sns.set_context('paper')
g=sns.catplot(x="Classe", y="Accur", col="step",data=dfall, kind="bar",ci=None)
g.set_axis_labels("", "Accurecy")
g.set_xticklabels(df1.Classe,rotation=45)
#g.set_titles("{col_name} {col_var}")
g.despine(left=True)
plt.show()
g.savefig(d["data_file"]+"plot.png")



run=dfall.groupby('step').mean()
run.drop('index',1,inplace=True)
R1=dfall.groupby('RESULAT_TEST_PLOT').mean()
R2=dfall.groupby('RESULAT_TEST_PLOT_v2').mean()
g=[]
for i in run.values:
    print (i)
    for j in i:
        print (j)
        g.append(j)
        y_pos=run.shape[0],run.shape[0]+1
        plt.bar(y_pos,j)
        plt.xticks(y_pos, tuple(run.index))
        
    plt.show()


Accu=dfall["Accur"].str.split(expand=True)
Accu.drop([1],axis=1,inplace=True).astype(float)
rapp=dfall["Rappel"].str.split(expand=True)
rapp.drop([1],axis=1,inplace=True).astype(float)
F_sc=dfall["F_score"].str.split(expand=True)
F_sc.drop([1],axis=1,inplace=True)


names_dfs=["index","Classe","Accur","Rappel","F_score","Confusion_classe","step","mean_Accur","std_accu","mean_rappel","std_rappel","mean_F_score","std_F_score"]
DF=pd.concat([dfall,Accu,rapp,F_sc],axis=1)
DF.columns=names_dfs



