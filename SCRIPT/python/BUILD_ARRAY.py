#!/usr/bin/python
# coding: utf-8

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

# faire un dico ou bien une parser 
d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/"
d["SM_DATA"]=d["data_file"] + "SM_DT_STAT_ZONAL/"
d["ADOUR"]=d["SM_DATA"] + "DT_ADOUR_SM2017/DATA_CSV/"
#d["SRTM"]=d["data_file"] + "SRTM/STAT_STRM_DT2017/DATA_CSV/"
#  création d'un tableu vide = avec pandas
DF=[]
time=[]
# print DF

list_fichier=os.listdir(d["ADOUR"])
for i in list_fichier :
	zone= i[2:8]
	date= i[8:16]
	# print date 
	ch=d["ADOUR"] 
	reader=pd.read_csv(ch+i)
	ZE=(zone* reader.shape[0])
	ZE=ZE.split("_")
	ZE= pd.DataFrame(ZE[1:len(ZE)])
	sel_names=reader.loc[:,['ID_PARCEL','CODE_CULTU','DT_COMM']]
	sel_variable=reader.loc[:,['_mean','_std','_var']]
	DF.append(sel_variable)
	time.append(date)
DF=pd.concat(DF, axis=1, join_axes=[sel_variable.index])
DF=pd.concat([DF, ZE], axis=1)
DF=pd.DataFrame(DF)
DF=pd.concat([DF,sel_names],axis=1)
#DF=DF.set_index(['ID_PARCEL',sel_names.index])
list_fichierT=os.listdir(d["SRTM"])

print d["SRTM"]
DF2=[]
for j in list_fichierT:
    ch=d["SRTM"]
    reader2=pd.read_csv(ch+j)
#    print reader2
    sel_variable2=reader2.loc[:,['ID_PARCEL','_DEMmean','_DEMstd','_DEMvar']]
    sel_names2=reader2.loc[:,['ID_PARCEL']]
    DF2.append(sel_variable2)
DF2=pd.concat(DF2,axis=1)
#print DF2

#==============================================================================
# Fusion tableau 
#==============================================================================
DF_ALL=pd.merge(DF, DF2, how = 'outer')
print DF_ALL

#print pd.isnull(DF_ALL)
#print DF_ALL.loc['NaN']
#print DF_ALL
#==============================================================================
# Gestion des ente
#==============================================================================
#TE=np.repeat(time,3)
#TE=list(TE)
##
#names_var=['ID_PARCEL','CODE_CULTU','DT_COMM']
#HEAD=names_var+TE
##HEAD=pd.DataFrame(HEAD)
##HEAD=HEAD.T
##print HEAD
##
##DF_ALL = DF_ALL.rename(columns=str(HEAD))
#for x in HEAD:
#    print x
#    DF_ALL.columns = DF_ALL.columns.str.replace('_',x)
#    print DF_ALL





#DF_ALL.columns = DF_ALL.columns.str.replace('_','')
#print DF_ALL
##DF= DF.append(HEAD)
##print DF.index
#print type(HEAD)

#print DF

#==============================================================================
#PLOT 
#==============================================================================
#x=[1,2,3,4]
#y=[1,2,3]
#plt.plot(x,y)
#
#plt.show()

