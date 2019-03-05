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



df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_2017_Pixel_cate_label_CrIrr.csv")

# name=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Sorghum_Irr","Soybean_Irr","Peas_Irr","Sunflow_Irr","Others"]
names_crop=["Maize_Irr","Soybean_Irr","Sorghum_Irr","Sunflower_Irr","Peas_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum_Nirr","Sunflower_Nirr","Peas_Nirr"]
#names_RPG=["Maize","Soybean","Sorghum","Sunflower","Peas"]

df1=df.sort_values(by='category', ascending=True)
df1["name"]=names_crop
df1=df1.reset_index()
y_pos = np.arange(len(list(df1.name)))
df2=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_2017_Pixel_cate_label_CrIrr_tcj.csv")
df2
name2=["Maize_Irr","Soybean_Irr","Sunflower_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum_Nirr","Sunflow_Nirr","Peas_Nirr"]

df2=df2.sort_values(by='category', ascending=True)
df2["name"]=name2
df2=df2.reset_index()

plt.figure(figsize=(15,15))
sns.set(style="darkgrid")
sns.set_context('paper')
plt.subplot(2,2,1)
pal=sns.set_palette("RdYlBu",len(y_pos))
sns.barplot(df1.name,df1["count"])
plt.xticks(y_pos, names_crop,rotation=45)
plt.xlabel("crops")
plt.ylabel("Nombre de polygon")
plt.title("Ensemble des 9 tiles")
plt.text(x=df.shape[0]-2,y=max(df["count"]),s=int(sum(df["count"])))
plt.text(x=df.shape[0]-7,y=max(df["count"]),s="Nombre total d'entitées :")
label=round(df1["count"],2)
# Tet on the top of each barplot
for i in range(len(df1["count"])):
    plt.text(x = y_pos[i] -0.3 , y = df1["count"][i] +10, s = label[i], size = 11)



plt.subplot(2,2,2)

y_pos2 = np.arange(len(name2))
sns.barplot(df2.name,df2["count"])
plt.xticks(y_pos2, name2,rotation=45)
plt.xlabel("crops")
plt.ylabel("Nombre de polygon")
plt.title("Tile TCJ")
plt.text(x=df2.shape[0]-2,y=max(df2["count"]),s=int(sum(df2["count"])))
plt.text(x=df2.shape[0]-6,y=max(df2["count"]),s="Nombre total d'entitées :")
label=round(df2["count"],2)
# Tet on the top of each barplot
for i in range(len(df2["count"])):
    plt.text(x = y_pos2[i] -0.3 , y = df2["count"][i] +10, s = label[i], size = 11)




df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_DT_TCJ_LabCrirr.csv")
df=df.sort_values(by='category', ascending=True)
names_crop_tcj=["Maize_Irr","Soybean_Irr","Sunflower_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum_Nirr","Sunflower_Nirr","Peas_Nirr"]
df["name"]=names_crop_tcj
df=df.reset_index()
y_pos= np.arange(len(list(df.name)))
plt.subplot(2,2,4)
sns.barplot(df.name,df["sum"]/sum(df["sum"]),palette=pal)
plt.xticks(y_pos, names_crop,rotation=45)
plt.xlabel("OS")
plt.ylabel("Réparition")
plt.text(x=df.shape[0]-2,y=max(df["sum"]/sum(df["sum"]))+0.005,s=round(float(sum(df["sum"])),2))
plt.text(x=df.shape[0]-6,y=max(df["sum"]/sum(df["sum"]))+0.005,s="superfice totale (ha):")
label=round(df["sum"]/sum(df["sum"]),2)
        # Tet on the top of each barplot
for j in range(len(df["sum"]/sum(df["sum"]))):
    plt.text(x = y_pos[j] -0.3 , y = (df["sum"]/sum(df["sum"]))[j], s = list(label)[j], size = 11)


df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_DT_ALL_lab_Crirr.csv")
df=df.sort_values(by='category', ascending=True)
df["name"]=names_crop
df=df.reset_index()
y_pos= np.arange(len(list(df.name)))
plt.subplot(2,2,3)
sns.barplot(df.name,df["sum"]/sum(df["sum"]),palette=pal)
plt.xticks(y_pos, names_crop,rotation=45)
plt.xlabel("OS")
plt.ylabel("Reparition")
plt.text(x=df.shape[0]-7.5,y=max(df["sum"]/sum(df["sum"]))+0.005,s=round(float(sum(df["sum"])),2))
plt.text(x=df.shape[0]-11.5,y=max(df["sum"]/sum(df["sum"]))+0.005,s="superfice totale (ha):")
label=round(df["sum"]/sum(df["sum"]),3)
        # Tet on the top of each barplot
for j in range(len(df["sum"]/sum(df["sum"]))):
    plt.text(x = y_pos[j] -0.4 , y = (df["sum"]/sum(df["sum"]))[j], s = list(label)[j], size = 11)

plt.show()