# -*- coding: utf-8 -*-
#!/usr/bin/python

#Created on Tue Jan  8 14:07:02 2019
#
#@author: pageot

import pickle 
import pandas as pd
import numpy as np
import os
import re
d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/"
d["test"]=d["SM_DATA"]+"TEST"
d["SM_DATA"]=d["data_file"] + "tmp/out_humidite/"
d["SRTM"]=d["data_file"] + "tmp/out_SRTM/"
d["pente"]=d["SRTM"] + "pente/" + "DT_ALL_2017_ER10_W84/"
d["expo"]=d["SRTM"]+ "SRTM/"+ "DT_ALL_2017_ER10_W84/"
d["DATA_ALL_E1"]=d["SM_DATA"]+ "emprise_1_S1a/"+"DT_ALL_2017_ER10_W84/"
d["DATA_ALL_E2"]=d["SM_DATA"]+ "emprise_2_S1a/"+"DT_ALL_2017_ER10_W84/"
d["DATA_ALL_E3"]=d["SM_DATA"]+ "emprise_3_S1a/"+"DT_ALL_2017_ER10_W84/"
d["DATA_ALL_E4"]=d["SM_DATA"]+ "emprise_4_S1a/"+"DT_ALL_2017_ER10_W84/"
d["DATA_ALL_E5"]=d["SM_DATA"]+ "emprise_5_S1b/"+"DT_ALL_2017_ER10_W84/"


d["test"]=d["SM_DATA"]+"TEST/"
d["A"]=d["test"]+"emprise_3_S1a/"+"DT_ALL_2017_ER10_W84/"
d["B"]=d["test"]+"emprise_4_S1b/"+"DT_ALL_2017_ER10_W84/"
#open de file extaction 
#pickle.load(open("./out_humidite/DT_2017_TARN_ER10_W84/hum_None_3149778.p"))
# il faut boucle sur les noms de fichier afin de produire un tableau ( converir en dataFRame)

a=pickle.load(open(d["DATA_ALL_E5"]+"hum_None_3280502.p"))
#b=pickle.load(open(d["DATA_ALL_E3"]+"hum_None_3280502.p"))
#Tab_testa=pd.DataFrame(a.items()) # code permettant de convertir dico en DF
#Tab_testb=pd.DataFrame(b.items())
#tdf=pd.merge(Tab_testa,Tab_testb,how='outer',on=0)


df = pd.DataFrame.from_dict(a, orient = 'index') # code permettant de convertir dico en DF avec indexation des first col
dfe=df.rename(index=str, columns={0:"3149778"})

#==============================================================================
# EMPRISE 1
#==============================================================================
#DF1=[]
#list_fichier=os.listdir(d["DATA_ALL_E1"])
#for i in list_fichier :
#    ch=d["DATA_ALL_E1"] 
#    idpar=i[9:-2]
#    reader=pickle.load(open(ch+i))
#    tab=pd.DataFrame(reader.items())
#    date1=list(tab.iloc[:,0])
#    tab=tab.rename(index=str,columns={1:idpar,0:'date1'})
##    tab=tab.T
#    DF1.append(tab)
#DF1=pd.concat(DF1,axis=1)
#DF1.drop('date1', axis=1, inplace=True)
##DF1['date'] = date1
#df1=DF1.T
#df1.columns = date1
#print df1
#df1.to_csv('DF1.csv', sep = '\t')
#
##==============================================================================
##Emprise 2 
##==============================================================================
#DF2=[]
#list_fichier=os.listdir(d["DATA_ALL_E2"])
#for i in list_fichier :
#    ch=d["DATA_ALL_E2"] 
#    idpar=i[9:-2]
#    reader=pickle.load(open(ch+i))
#    tab=pd.DataFrame(reader.items())
#    date2=list(tab.iloc[:,0])
#    tab=tab.rename(index=str,columns={1:idpar,0:'date2'})
#    DF2.append(tab)
#DF2=pd.concat(DF2,axis=1)
#DF2.drop('date2', axis=1, inplace=True)
##DF2['date2'] = date2
#df2=DF2.T
#df2.columns = date2 ### modification du nom des colonnes 
#print df2
#df2.to_csv('DF2.csv', sep = '\t')
#
#==============================================================================
# TEST
#==============================================================================
df=pd.DataFrame([])
list_dalle=os.listdir(d["test"])
for i in list_dalle:
    list_shp=os.listdir(d["test"]+i)
    for j in list_shp:
        list_parcelle=os.listdir(d["test"]+i+"/"+j)
        for k in list_parcelle:
            idpar=k[9:-2]
            reader=pickle.load(open(d["test"]+i+"/"+j+"/"+k))
            data=pd.DataFrame(reader.items())
            data.rename(index=str,columns={1:idpar},inplace=True)
            df=df.append(data,ignore_index=True)
#==============================================================================
# Boucle sur ensemble des emprise SM
#==============================================================================
#a=pickle.load(open(d["DATA_ALL_E3"]+"hum_None_3277665.p"))



DALL1=pd.DataFrame([])
DALL=[]
DATE=[]
IDPAR=[]
#DALL={}
list_emprise=os.listdir(d["SM_DATA"])
for i in list_emprise:
    list_fichier=os.listdir(d["SM_DATA"]+i)
    for j in list_fichier: 
        list_file_shp=os.listdir(d["SM_DATA"]+i+"/"+j)
        for k in list_file_shp:
            idpar=k[9:-2]
            reader1=pickle.load(open(d["SM_DATA"]+i+"/"+j+"/"+k))
            tab=pd.DataFrame(reader1.items())
            IDPAR.append(idpar)
            IDPAR_ss=set(IDPAR)
            IDPAR=list(IDPAR_ss)
            date=list(tab.iloc[:,0])
            DATE.extend(date)
            DATE_ss= set(DATE)
            DATE = list(DATE_ss)
list_emprise=os.listdir(d["SM_DATA"])
for i in list_emprise:
    list_fichier=os.listdir(d["SM_DATA"]+i)
    for j in list_fichier: 
        list_file_shp=os.listdir(d["SM_DATA"]+i+"/"+j)
        for k in list_file_shp:
            reader=pickle.load(open(d["SM_DATA"]+i+"/"+j+"/"+k))
            idpar=k[9:-2]
            for t in DATE: 
                if t not in reader.keys():
                    reader.update({t:'Nan'})
            tab1=pd.DataFrame(reader.items())
            tab3=tab1.rename(index=str,columns={1:idpar,0:'date'})
            DALL1=DALL1.append(tab3,ignore_index=True)      
#DALL1=pd.concat(DALL1,axis=1)
#
#DALL1.drop('date',axis=1,inplace=True)
#df_f=DALL1.T
#df_f.columns= DATE
#df_f=df_f.sort_index(axis=1,ascending=True)
#df_f.to_csv("df_f.csv",sep='\t')

MNTALL=[]
DEM=os.listdir(d["SRTM"])
for s in DEM:
    shp_file=os.listdir(d["SRTM"]+s)
    for p in shp_file:
        parcelle=os.listdir(d["SRTM"]+s+"/"+p)
        for c in parcelle:
            idplot=c[9:-2]
            readerDEM=pickle.load(open(d["SRTM"] + s +"/"+p+"/"+c))
            for g in readerDEM.keys():
                if readerDEM.keys() == [20181207]:
                    readerDEM['pente']=readerDEM.pop(20181207)
                else:
                    readerDEM['expo']=readerDEM.pop(20181208)
                df=pd.DataFrame(readerDEM.items())
                df=df.rename(index=str,columns={1:idplot})
                dfT=df.T
                MNTALL.append(dfT)
                
                


MNT_expo=pd.concat(MNTALL[0:1710],axis=0)
MNT_pente=pd.concat(MNTALL[1711:],axis=0)
MNT_pente=MNT_pente.drop(0)
MNT_pente=MNT_pente.rename(index=str,columns={'0':'pente'})
MNT_expo=MNT_expo.drop(0)
MNT_expo=MNT_expo.rename(index=str,columns={'0':'expo'})

MNTALL2=MNT_pente.join(MNT_expo, how='outer')

MNTALL2.to_csv("df_MNT.csv",sep="\t")

    
