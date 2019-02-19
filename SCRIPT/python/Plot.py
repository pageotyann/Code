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
name=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Sorghum_Irr","Soybean_Irr","Peas_Irr","Sunflow_Irr","Others"]
y_pos = np.arange(len(name))
df["name"]=name
print (df)


plt.figure(figsize=(15,10))
sns.barplot(df.name,df["count"])
plt.xticks(y_pos, name,rotation=45)
plt.xlabel("crops")
plt.ylabel("Nombre de polygon")

label=["n=691","n=153","n=20","n=469","n=2448","n=20","n=3","n=1247","n=4","n=6","n=193"]
# Tet on the top of each barplot
for i in range(len(df["count"])):
    plt.text(x = y_pos[i] -0.2 , y = df["count"][i] +10, s = label[i], size = 11)
# Show graphic
plt.show()

df2=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_2017_Pixel_cate_label_CrIrr_tcj.csv")
df2
name2=["Maize_Nirr","Soybean_Nirr","Peas_Nirr","Sunflow_Nirr","Maize_Irr","Sorghum_Nirr","Soybean_Irr","Sunflow_Irr","Others"]
df2["name"]=name2

plt.figure(figsize=(15,10))
y_pos2 = np.arange(len(name2))
sns.barplot(df2.name,df2["count"])
plt.xticks(y_pos2, name,rotation=45)
plt.xlabel("crops")
plt.ylabel("Nombre de polygon")

label=["n=227","n=86","n=13","n=318","n=1315","n=16","n=891","n=1","n=110"]
# Tet on the top of each barplot
for i in range(len(df2["count"])):
    plt.text(x = y_pos2[i] -0.2 , y = df2["count"][i] +10, s = label[i], size = 11)
# Show graphic
plt.show()