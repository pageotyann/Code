#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:26:12 2019

@author: pageot
"""


import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np 
import seaborn as sns
import os


df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_DT_TCJ_LabCrirr.csv")
df.drop([7],inplace=True)# Suppression du sunflower_irr car sous représenter
df=df.sort_values(by='category', ascending=True)
names_crop_tcj=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum_Nirr","Sunflower_Nirr","Peas_Nirr"]
df["name"]=names_crop_tcj
df=df.reset_index()
y_pos= np.arange(len(list(df.name)))
plt.figure(figsize=(10,10))
sns.set(style="darkgrid")
sns.set_context('paper')
pal=sns.set_palette("RdYlBu",len(y_pos))
sns.barplot(df.name,df["sum"]/0.01,palette=pal)
plt.xticks(y_pos, names_crop_tcj,rotation=45)
plt.xlabel("OS")
plt.ylabel("nombre de pixels")
plt.text(x=df.shape[0]-2,y=max(df["sum"]/0.01)+0.005,s=round(float(sum(df["sum"])),2))
plt.text(x=df.shape[0]-6,y=max(df["sum"]/0.01)+0.005,s="superfice totale (ha):")
label=round(df["sum"]/0.01,2)
        # Tet on the top of each barplot
for j in range(len(df["sum"])):
    plt.text(x = y_pos[j] -0.3 , y = (df["sum"]/0.01)[j], s = list(label)[j], size = 11)