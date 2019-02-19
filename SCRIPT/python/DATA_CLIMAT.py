# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on Thu Jan 17 10:06:03 2019

@author: pageot
"""


import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt


d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/SYNOP_MF"
list_synop=os.listdir(d['data_file'])
list_sta=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/postesSynop.csv")
list_stat_supp=list(list_sta.iloc[42:,1])
list_stat_int=list(list_sta.iloc[[26,27,28,31,32,33,34],1])
list_stat_supp.append(78890)
list_stat_supp.append(61970)
list_sta=list_sta[:42]


#data=pd.DataFrame([])
#
now = datetime.datetime.now()
        
df=pd.DataFrame([])
for i in list_synop:
    reader=pd.read_csv(d['data_file']+"/"+i,sep=';')
    tab=reader.rename(index=str,columns={'numer_sta':'ID'})
    for j in list_stat_int:
        tabdata=tab[tab.ID == j]
        tab_sta=list_sta.append([list_sta]*(tabdata.shape[0]/42),ignore_index=True)
        Fusion=tab_sta.merge(tabdata, on='ID')
        df2=Fusion.drop_duplicates(keep="last")
        df=df.append(df2,ignore_index=True)
Data_climat=df.iloc[:,[1,2,3,4,5,6,12,-18]]
Data_climat['t']=Data_climat['t'].replace(to_replace=['mq'],value=-9999)
Data_climat['rr24']=Data_climat['rr24'].replace(to_replace=['mq'],value=-9999)
Data_climat[['t','rr24']]=Data_climat[['t','rr24']].astype(float)
Data_climat['t']=Data_climat['t']-273.15
Data_climat.drop_duplicates(keep="last", inplace=True)    
a=[]


Data_climat['date']=Data_climat['date'].astype(str)
#Spliter les dates en AAAAMMJJ et 
JJall=[]
for s in Data_climat.date:
    JJ=s[0:8]
    JJall.append(JJ)
Data_climat['JJ']=JJall
Data_climat['JJ']=Data_climat['JJ'].astype(int)
DF_Tmean=Data_climat.groupby(['Nom','JJ'])['t'].mean().reset_index()

now2= datetime.datetime.now()
print (now2-now)       
DF_Tmean.to_csv("DATA_climat.csv",sep="\t")


#==============================================================================
# divers Test
#==============================================================================
#Tmean=[]
#rowa=[]
#stat=list(set(Data_climat.Nom))
#jj=list(set(Data_climat.JJ))
#jj=sorted(jj)


#for l in stat:
#    for t in jj:
#        a=Data_climat.t.loc[(Data_climat['Nom']==l) & (Data_climat['JJ']==t)].mean()
#        Tmean.append(a)
## ajoute condition de présence de la date sur le lieu. 
#rowa=sorted(rowa)
#list_id=list(Data_climat.id)
#ju=[]
#for i in list_id:
#    g=list_id[i] in rowa
#    ju.append(g)
#        
#
#Data_climat['drop']=ju
#Data_climat['drop']=Data_climat['drop'].replace(to_replace=False,value=pd.NaT)
#df_climat=Data_climat
#Data_climat=Data_climat.dropna()
#Data_climat['t_mean']=Tmean



    
#extraction des stations d'interets

#list_stat_int=list(list_sta.iloc[[26,27,28,31,32,33,34],1])
#dfs_cli=pd.DataFrame([])
#for k in list_stat_int: 
#    df_climat=data.loc[data.ID==k]
#    dfs_cli=dfs_cli.append(df_climat,ignore_index=True)
#    data_climat=dfs_cli.iloc[:,[1,2,3,4,5,6,12,-18]]
#    data_climat['t']=data_climat['t'].replace(to_replace=['mq'],value=-9999)
#    data_climat['rr24']=data_climat['rr24'].replace(to_replace=['mq'],value=-9999)
#    data_climat[['t','rr24']]=data_climat[['t','rr24']].astype(float)
#    data_climat['t']=data_climat['t']-273.15
#    data_climat.drop_duplicates(keep="last", inplace=True)
#a=[]
#for r in data_climat.date:
#    if r%100000 == 0:
#        b=1
#    else:
#        b=pd.NaT
#    a.append(b)
#data_climat['drop']=a
#
#data_climat['date']=data_climat['date'].astype(str)
##Spliter les dates en AAAAMMJJ et 
#JJall=[]
#for s in data_climat.date:
#    JJ=s[0:8]
#    JJall.append(JJ)
#data_climat['JJ']=JJall
#data_climat['JJ']=data_climat['JJ'].astype(int)
#
#Tmean=[]
#for t in data_climat.JJ:
#    a= data_climat.t.loc[data_climat['JJ']==t].mean()
#    Tmean.append(a)
#data_climat['t_mean']=Tmean
#data_climat=data_climat.dropna()
#now2= datetime.datetime.now()
#print (now2-now)       
#Data_climat.to_csv("DATA_climat.csv",sep="\t")


##test extctraction deux colones + conversion T en T°c
#test=Data_climat.iloc[0:]
#test['date']=test['date'].astype(str)
#idr=[i for i in np.arange(0,test.shape[0],1)]
#test['id']=idr
##Spliter les dates en AAAAMMJJ et 
#JJall=[]
#for s in test.date:
#    JJ=s[0:8]
#    JJall.append(JJ)
#test['JJ']=JJall
#test['JJ']=test['JJ'].astype(int)
#
#temean=[]
#rowa=[]
#stat=list(set(test.Nom))
#jj=list(set(test.JJ))
#
#for t in jj:
#    for l in stat:
#        a=test.t.loc[(test['Nom']==l) & (test['JJ']==t)].mean()
#        temean.append(a)
#        h=test.id.loc[(test['Nom']==l) & (test['JJ']==t)].iloc[0]
#        rowa.append(h)
#rowa=sorted(rowa)
#list_id=list(test.id)
##Moyenner les dates
#
#      
#
##supp les lignes en trop afin d'ajoute la valeur journalière    
#
#a=[]
#for i in list_id:
#    g=list_id[i] in rowa
#    a.append(g)
#        
#
#test['drop']=a
#test['drop']=test['drop'].replace(to_replace=False,value=pd.NaT)
#test1['t_mean']=temean
#test1=test.dropna()
#depa= [] 
#fin = []
#for t in test.date:
#    if t%100000 == 10000:
#        print t
#        fin.append(t) 
#    if t%100000 == 0: 
#        print t
#        depa.append(t)
#
#redd=pd.DataFrame([])
#bluee=pd.DataFrame([])
#for i in depa:
#    qa=test.loc[test['date'] == i]
#    redd=redd.append(qa,ignore_index=False)
#for h in fin:
#    tr=test.loc[test['date'] ==h]
#    bluee=bluee.append(tr, ignore_index=False)
#redd.drop_duplicates(keep="last",inplace=True)
#bluee.drop_duplicates(keep="last", inplace=True)    
##tré les ID par 
#bluee.sort_index(axis = 0, ascending = True,inplace =True)  
#redd.sort_index(axis = 0, ascending = True,inplace =True)  
## 2 solution
#depar=pd.DataFrame(redd.iloc[:,-1])
#depar=depar.reset_index()
#fini=pd.DataFrame(bluee.iloc[:,-1])
#fini=fini.reset_index()
#tabs=[depar,fini]
#
#boucletab=pd.concat(tabs,axis=1,ignore_index=False)
#boucletab.replace(to_replace=['Nan'],value=-9999,inplace=True)
#boucletab.drop('index',axis=1,inplace=True)
##boucletab.columns = range(boucletab.shape[1])
#boucletab=boucletab.astype(int)
#date_moyenne=[]
#for index,row in boucletab.iterrows():
#    print row
#    a=test.t[row[0]:row[1]].mean()
#    print a
#    date_moyenne.append(a)



#
##==============================================================================
## creation plot dynamique rr + t
##==============================================================================
#plt.plot(DF_Tmean.Nom, DF_Tmean.t)



