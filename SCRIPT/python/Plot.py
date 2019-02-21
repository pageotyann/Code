# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 11:26:55 2019

@author: pageot
"""

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np 
import seaborn as sns
import os
#STAT_DT_ALL_2017_PRA
# =============================================================================
# boucle barplot stat
# =============================================================================
list_csv=os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAY_PRAGRI/CSV")
names_crop=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Sorghum_Irr","Soybean_Irr","Peas_Irr","Sunflow_Irr","Others"]
names_RPG=["Maize","Soybean","Sorghum","Sunflower","Peas"]
code_crops_RPG=[1,2,3,4,5]
code_crops=[1,2,3,4,5,6,11,22,33,44,55]
for i in list_csv:
    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAY_PRAGRI/CSV/"+ i)
    zone=i[8:-4]
    if df.shape[0] != len(code_crops_RPG):
        print ("Error dimension")
    else:
        df["name"]=names_RPG
        df1=df.sort_values(by='sum', ascending=False)
        df1=df1.reset_index()
        y_pos = np.arange(len(list(df1.name)))
        fig = plt.figure(figsize=(10,15))
        #pal=sns.set_palette("RdYlBu",len(y_pos))
        #sns.barplot(df1.name,df1["mean"],palette=pal,yerr = df1["stddev"]) # permet d'ajoute les ecart types
        sns.barplot(df1.name,(df1["sum"]/sum(df["sum"])),palette=pal)
        plt.xticks(y_pos, list(df1.name),rotation=45)
        plt.xlabel("crops")
        plt.ylabel("Superficie en ha")
        plt.title(zone)
        plt.text(x=4,y=max(df["sum"]/sum(df["sum"])),s=round(sum(df["sum"]),2))
        plt.text(x=3,y=max(df["sum"]/sum(df["sum"])),s="superfice totale (ha):")
        label=round(df1["sum"]/sum(df["sum"]),2)
        # Tet on the top of each barplot
        for j in range(len(df1["sum"])):
            plt.text(x = y_pos[j] , y = (df1["sum"]/sum(df["sum"]))[j] +0.01, s = list(label)[j], size = 11)
        # Show graphic
        plt.show()
        fig.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAY_PRAGRI/PLOT/PLOT_SUM_POND/%s.png"%(zone))
# =============================================================================
# Ajoute de la fonction add
# =============================================================================
list_csv=os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAY_PRAGRI/CSV")
names_crop=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Sorghum_Irr","Soybean_Irr","Peas_Irr","Sunflow_Irr","Others"]
names_RPG=["Maize","Soybean","Sorghum","Sunflower","Peas"]
code_crops_RPG=[1,2,3,4,5]
code_crops=[1,2,3,4,5,6,11,22,33,44,55]
for i in list_csv:
    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAY_PRAGRI/CSV/"+ i)
    zone=i[8:-4]
    if df.shape[0] != len(code_crops_RPG):
        print ("Error dimension")
    else:
        df["name"]=names_RPG
        df1=df.sort_values(by='sum', ascending=False)
        df1=df1.reset_index()
        y_pos = np.arange(len(list(df1.name)))
        fig = plt.figure(figsize=(10,15))
        #pal=sns.set_palette("RdYlBu",len(y_pos))
        #sns.barplot(df1.name,df1["mean"],palette=pal,yerr = df1["stddev"]) # permet d'ajoute les ecart types
        sns.barplot(df1.name,(df1["sum"]/sum(df["sum"])),palette=pal)
        plt.xticks(y_pos, list(df1.name),rotation=45)
        plt.xlabel("crops")
        plt.ylabel("Superficie en ha")
        plt.title(zone)
        plt.text(x=4,y=max(df["sum"]/sum(df["sum"])),s=round(sum(df["sum"]),2))
        plt.text(x=3,y=max(df["sum"]/sum(df["sum"])),s="superfice totale (ha):")
        label=round(df1["sum"]/sum(df["sum"]),2)
        # Tet on the top of each barplot
        for j in range(len(df1["sum"])):
            plt.text(x = y_pos[j] , y = (df1["sum"]/sum(df["sum"]))[j] +0.01, s = list(label)[j], size = 11)
        # Show graphic
        plt.show()
        fig.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAY_PRAGRI/PLOT/PLOT_SUM_POND/%s.png"%(zone))
# =============================================================================
# Ensemble sur même graphique 
# =============================================================================
#list_csv=os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAY_PRAGRI/CSV")
#names_crop=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Sorghum_Irr","Soybean_Irr","Peas_Irr","Sunflow_Irr","Others"]
#names_RPG=["Maize","Soybean","Sorghum","Sunflower","Peas"]
#code_crops_RPG=[1,2,3,4,5]
#code_crops=[1,2,3,4,5,6,11,22,33,44,55]
#df_f=pd.DataFrame()
#for i in list_csv:
#    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAY_PRAGRI/CSV/"+ i)
#    zone=i[8:-4]
#    print(df)
#    df_f.append(df)
# =============================================================================
# TEST plot seaborn
# =============================================================================
#df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_2017_Pixel_cate_label_CrIrr.csv")
#name=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Sorghum_Irr","Soybean_Irr","Peas_Irr","Sunflow_Irr","Others"]
#
#df["name"]=name
#df1=df.sort_values(by='count', ascending=False)
#df1=df1.reset_index()
#y_pos = np.arange(len(list(df1.name)))
#
#df2=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_2017_Pixel_cate_label_CrIrr_tcj.csv")
#df2
##add=pd.DataFrame({"category":[3,5],"min":[0,0],"max":[0,0],"mean":[0,0],"stddev":[0,0],"sum":[0,0],"count":[0,0],"name":['Sorghum_Irr',"Peas_Irr"]},index=[6,8])
#add=pd.DataFrame({"category":[3,5],"min":[0,0],"max":[0,0],"mean":[0,0],
#                  "stddev":[0,0],"sum":[0,0],"count":[0,0]},index=[6,8])
#
##name2=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Soybean_Irr","Sunflow_Irr","Others"]
##name3=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Soybean_Irr","Sunflow_Irr","Others","Sorghum_Irr","Peas_Irr"]
#
#
#
#df3=pd.concat([df2,add],ignore_index=True)
#df3["name"]=name
#df4=df3.sort_values(by='count', ascending=False)
#df4=df4.reset_index()
##name4=list(df3.name)
#y_pos4 = np.arange(len(list(df4.name)))
#
#plt.figure(figsize=(10,15))
#plt.subplot(1,2,1)
#pal=sns.set_palette("RdYlBu",len(y_pos))
#
#
#sns.barplot(df1.name,df1["count"],palette= pal)
#plt.xticks(y_pos, name,rotation=45)
#plt.xlabel("crops")
#plt.ylabel("Nombre de polygon")
#plt.title("Ensemble des 9 tiles")
#label=list(df1["count"])
## Tet on the top of each barplot
#for i in range(len(df1["count"])):
#    plt.text(x = y_pos[i] -0.5 , y = df1["count"][i]+10, s = label[i], size = 11)
## Show graphic
#
#
#plt.subplot(1,2,2)
#pal=sns.set_palette("RdYlBu",len(y_pos))
#sns.barplot(df4.name,df4["count"],palette=pal)
#plt.xticks(y_pos4, list(df4.name),rotation=45)
#plt.xlabel("crops")
#plt.ylabel("Nombre de polygon")
#plt.title("tile TCJ")
#label2=list(df4["count"])
## Tet on the top of each barplot
#for i in range(len(df4["count"])):
#    plt.text(x = y_pos4[i]-0.5 , y = df4["count"][i] +10, s = label2[i], size = 11)
## Show graphic
#plt.show()