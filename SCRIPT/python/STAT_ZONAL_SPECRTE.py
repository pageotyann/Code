#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:38:21 2019

@author: pageot
"""

import os
import sqlite3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np 
import seaborn as sns
import csv

# =============================================================================
# Optique
# =============================================================================
# Lectuer des files
d={}
conn = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/Samples_region_1_seed4_learn.sqlite')
df=pd.read_sql_query("SELECT * FROM output", conn)
dfpar=df.groupby("originfid").mean()

# Recuperation des names de cultures
#names_crops=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/RUN/r9_crops_tcj_const_PSRI_ERR/final/nomenclature_V2_crops.txt",sep=":",names=["name","code"])

#lister les labels dans le file sqlite 
lab=dfpar.labcroirr.astype(int)
lab=list(set(lab))

#loop sur les label 

for i in lab:
    print(i)
    globals()['cropslab%s' % i] = pd.DataFrame(dfpar[dfpar.labcroirr==i]).T
    globals()['NDVI%s' % i]=[]
    for index,row in globals()['cropslab%s' % i].iterrows():
        if "ndvi" in index:
            globals()['NDVI%s' % i].append (row)
            globals()['dfndvi%s' % i]=pd.DataFrame(globals()['NDVI%s' % i])

    plt.figure(figsize=(15,10))
    #y_pos=np.arange(df.shape[0])
    sns.set(style="darkgrid")
    sns.set_context('paper')
    plt.plot(globals()['dfndvi%s' % i])
    plt.xticks(rotation=90)
    plt.title("CODE_CULTURE"+"_"+str(i))
    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/NDVI_2017/plot_NDVI_TEMPOREL_%s"%(i))




conn = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R13_S1_S2/learningSamples/Samples_region_1_seed2_learn.sqlite')
df=pd.read_sql_query("SELECT * FROM output", conn)
dfpar=df.groupby("originfid").mean()

# Recuperation des names de cultures
#names_crops=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/RUN/r9_crops_tcj_const_PSRI_ERR/final/nomenclature_V2_crops.txt",sep=":",names=["name","code"])
# =============================================================================
# RADAR
# =============================================================================
#lister les labels dans le file sqlite 
lab=dfpar.labcroirr.astype(int)
lab=list(set(lab))

#loop sur les label 

for i in lab:
    print(i)
    globals()['cropslab%s' % i] = pd.DataFrame(dfpar[dfpar.labcroirr==i]).T
    globals()['VV%s' % i]=[]
    for index,row in globals()['cropslab%s' % i].iterrows():
        if "des_vv" in index:
            globals()['VV%s' % i].append (row)
            globals()['dfVV%s' % i]=pd.DataFrame(globals()['VV%s' % i])
            globals()["dbdfVV%s" % i]=10*np.log(globals()['dfVV%s' % i])
    plt.figure(figsize=(15,10))
    #y_pos=np.arange(df.shape[0])
    sns.set(style="darkgrid")
    sns.set_context('paper')
    plt.plot(globals()['dbdfVV%s' % i])
    plt.xticks(rotation=90)
    plt.title("CODE_CULTURE"+"_"+str(i))
    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/SAR_2017/plot_desVV_TEMPOREL_%s"%(i))


#if i == names_crops.code:
#    print (names_crops.code)
#Maize irrigated:1
#Maize no irrigated:11
#Soybean irrigated:2
#Soybean no irrigated:22
#Sorghum no irrigated:33
#Sunflower no irrigated:44
#Peas no irrigated:55
#Others:6
#


# =============================================================================
# SRTM_STAT
# =============================================================================
STASRTM = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/SRTM_TCJ_SLP_SampleExtraction.sqlite')
df=pd.read_sql_query("SELECT * FROM output", STASRTM)

dfpar=df.groupby("originfid").mean()
dfpar=df.groupby("originfid").var()

dflab=dfpar.groupby("labcroirr").mean()

plt.figure(figsize=(15,15))
sns.set(style="darkgrid")
sns.set_context('paper')
g=sns.violinplot(x='labcroirr', y='value_0', data=dfpar)
plt.ylabel("mean_elevation")
#g.set_xticklabels(,rotation=90)
plt.xlabel("label")


STApente = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SRTM_TCJ/S2__TEST_AUX_REFDE2_T31TCJ_0001_SLP_R1.TIF_SampleExtraction.sqlite')
dfslp=pd.read_sql_query("SELECT * FROM output", STApente)

dfpar=dfslp.groupby("originfid").mean()

plt.figure(figsize=(15,15))
sns.set(style="darkgrid")
sns.set_context('paper')
g=sns.violinplot(x='labcroirr', y='value_0', data=dfslp)
plt.ylabel("mean_pente")
#g.set_xticklabels(,rotation=90)
plt.xlabel("label")


STAexpo = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SRTM_TCJ/RECLASS_EXPO_MASK_T31TCJ.tif_SampleExtraction.sqlite')
dfexpo=pd.read_sql_query("SELECT * FROM output", STAexpo)

dfpar=dfexpo.groupby("originfid").mean()

plt.figure(figsize=(15,15))
sns.set(style="darkgrid")
sns.set_context('paper')
g=sns.box(x='labcroirr', y='value_0', data=dfexpo)
plt.ylabel("mean_pente")
#g.set_xticklabels(,rotation=90)
plt.xlabel("label")

#loop sur file tile SRTM et pente et EXPO 

d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/"
d["ALL"]=d["data_file"]+"STAT_SRTM_DT_ALL/"
for i in os.listdir(d["ALL"]):
    tile=i[19:26]
    var=i[32:35]
    print (tile)
    print (var)
    dfsrtm = sqlite3.connect(d["ALL"]+i)
    df=pd.read_sql_query("SELECT * FROM output", dfsrtm)
    dfpar=df.groupby("originfid").mean()
    plt.figure(figsize=(15,15))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    g=sns.violinplot(x='labcroirr', y='value_0', data=df)
    plt.ylabel(var+tile)
    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLT_SRTM_DT/%s_%s.png"%(var,tile))

# =============================================================================
# SPECTRE SM
# =============================================================================
timeSM=pd.DataFrame()
for i in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SM_DT/"):
    print (i)
    date=i[3:11]
    STASMD = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SM_DT/'+i)
    dfSM=pd.read_sql_query("SELECT * FROM output", STASMD)
    dfpar=dfSM.groupby("originfid").mean()
    lab=dfpar.labcroirr.astype(int)
    globals()["meansm%s"%date]=dfpar.value_0
    globals()["meansm%s"%date].rename("SM_"+date,inplace=True)
    timeSM=timeSM.append(globals()["meansm%s"%date])

timesm=timeSM.T
timesm["label"]=lab
label=list(set(lab))
for j in label:
    print(j)
    globals()['SMcropslab%s' % j] = pd.DataFrame(timesm[timesm.label==j]).T
    plt.figure(figsize=(15,10))
    #y_pos=np.arange(df.shape[0])
    sns.set(style="darkgrid")
    sns.set_context('paper')
    plt.plot(globals()['SMcropslab%s' % j],linestyle="",marker='o')
    plt.xticks(rotation=90)
    plt.title("CODE_CULTURE"+"_"+str(j))
    

# =============================================================================
# Gestion des datas SAFRAN
# =============================================================================
df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/preliq2017.csv")

LAMBX=df.LAMBX*100
LAMBY=df.LAMBY*100
df["lambX"]=LAMBX
df['lambY']=LAMBY
df.to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/preliq2017_v2.csv")

df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/SAFRAN_TCJ.csv")
df1=df.drop([0])
preliq=df1[["DATE","PRELIQ_Q","X","Y"]]
preliq2=preliq.sort_values(by="DATE")
meandate=preliq2.groupby("DATE").mean()

# =============================================================================
# Groupe en fonctiondes date S1
# =============================================================================
date_S1=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R13_S1_S2/tmp/S1_vh_DES_dates_interpolation.txt",names=None)

images=[]
with open("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R13_S1_S2/tmp/S1_vh_DES_dates_interpolation.txt", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        images.append(row[0])

images_S1=list(map(int,images))

date=meandate.index
images_S1=list(map(int,images))
SAFRAN_S1=meandate.loc[images_S1]

plt.figure(figsize=(20,20))
sns.set(style="darkgrid")
sns.set_context('paper')
plt.bar(images_S1,SAFRAN_S1.PRELIQ_Q,color="blue",width=5)
ax2 = plt.twinx()
ax2.plot(images_S1,dbdfVV1)
plt.xticks(images_S1,rotation=90)

# =============================================================================
# Test plot VVdb et Safran
# =============================================================================
