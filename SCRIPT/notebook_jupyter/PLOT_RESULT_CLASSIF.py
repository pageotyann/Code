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




def plt_classif(df,var1,var2,var3):
    plt.figure(figsize=(10,10))
    y_pos=np.arange(df.shape[0])
    sns.set(style="darkgrid")
    sns.set_context('paper')
    plt.bar(y_pos,df["mean_"+var1],yerr=df["std_"+var1],capsize=3,width = 1,label=var1)
    plt.bar(y_pos+df.shape[0]+0.5,df["mean_"+var2],yerr=df["std_"+var2],capsize=3,width = 1,label=var2)
    plt.bar(y_pos+df.shape[0]*2.25,df["mean_"+var3],yerr=df["std_"+var3],capsize=3,width = 1,label=var3)
    plt.xticks(y_pos, tuple(df.index),rotation=90)
#    plt.text(y_pos+df.shape[0]+0.5, 0, "df.index")
    plt.legend()
    plt.show()

d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/RUN/"
d["SAVE"]="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/"
# =============================================================================
# Plot Resul Classif  
# ===========================================================================

dfall=pd.DataFrame()
dfaccu=pd.DataFrame()
dfrapp=pd.DataFrame()
dffsc=pd.DataFrame()
names_df=["Classe","Accur","Rappel","F_score","Confusion_classe"]
names_dfs=["index","Classe","Precision","Rappel","F_score","Confusion_classe","step","mean_Precision","std_Precision","mean_rappel","std_rappel","mean_Fscore","std_Fscore"]
nombre_de_classe=8

for j in os.listdir(d["data_file"]):
    for i in os.listdir(d["data_file"] +j):
        df=pd.read_csv(d["data_file"]+j+"/"+i+"/"+"RESULTS.txt",sep='\|',skiprows=int(18))
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
data.sort_index(by=["step","Classe"],ascending=True,inplace=True)
data.reset_index(inplace=True)
dfstep=data.groupby('step').mean()
dfstep.drop(['level_0','index'],axis=1,inplace=True)
#dita=data.drop([2,12,17],axis=0)
# =============================================================================
#  plot comparer les run  
# =============================================================================
plt_classif(dfstep,'Precision','Fscore','rappel')


# =============================================================================
# Plot visualisation run[i] par classe
# =============================================================================
#plt.figure(figsize=(10,10))
#sns.set(style="darkgrid")
#sns.set_context('paper')
#sns.barplot(data["Classe"][0:nombre_de_classe],data["mean_Precision"][0:nombre_de_classe])
#y_pos=np.arange(data.shape[0])
#plt.xticks(np.arange(data.shape[0]), df1.Classe ,rotation=45)
#label=round(data["mean_Precision"][0:nombre_de_classe],2)
#for i in y_pos:
#    plt.text(x = y_pos[i]-0.2 , y = data["mean_Precision"][0:17][i], s = label[i], size = 11)
#
## =============================================================================
## Plot comparer les Accur entre classse entre run
## =============================================================================
#
#plt.figure(figsize=(15,15))
#sns.set(style="darkgrid")
#sns.set_context('paper')
#
#g=sns.catplot(x="Classe", y="mean_Precision", col="step",data=data, kind="bar",ci=None)
#g.set_axis_labels("", "Accurecy")
#g.set_xticklabels(df1.Classe,rotation=45)
##g.set_titles("{col_name} {col_var}")
##g.despine(left=True)
#plt.show()
#
#g=sns.catplot(x="Classe", y="mean_Fscore", col="step",data=data, kind="bar",ci=None)
#g.set_axis_labels("", "F-score")
#g.set_xticklabels(df1.Classe,rotation=45)
##g.set_titles("{col_name} {col_var}")
##g.despine(left=True)
#plt.show()
#
#g=sns.catplot(x="Classe", y="mean_rappel", col="step",data=data, kind="bar",ci=None)
#g.set_axis_labels("", "Rappel")
#g.set_xticklabels(df1.Classe,rotation=45)
##g.set_titles("{col_name} {col_var}")
##g.despine(left=True)
#
#
#
#plt.show()
#print (data[["Classe","step","mean_Precision","mean_Fscore","mean_rappel"]])

#g.savefig(d["data_file"]+"plot.png")















