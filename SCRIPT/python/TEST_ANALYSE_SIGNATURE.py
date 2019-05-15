#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:13:13 2019

@author: pageot

script pour comparer les trajectoires des signture temporelles sur une petit zone a la parcelle
"""

import os
import sqlite3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import seaborn as sns
import csv
import STAT_ZONAL_SPECRTE


def pltmutli(x,x2,y1,y1bis,y2,y2bis,y3,y3bis,y4,y4bis,y5,y5bis,x3,y6):
    plt.figure(figsize=(20,20))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    ax1 = plt.subplot(611)
    p1=plt.plot(x,y1,color='blue')
    p2=plt.plot(x,y1bis,color='red',linestyle='--')
    plt.ylabel("NDVI")
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2 = plt.subplot(612)
    plt.plot(x,y2,color="blue")
    plt.plot(x,y2bis,color='red',linestyle='--')
    plt.ylabel("NDWI")
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax3 = plt.subplot(613)
    plt.plot(x2,y3,color='blue')
    plt.plot(x2, y3bis,color="red",linestyle='--')
    plt.ylabel("VV")
    plt.setp(ax3.get_xticklabels(), visible=False)    
    ax4 = plt.subplot(614)
    plt.plot(x2,y4,color='blue')
    plt.plot(x2, y4bis,color='red',linestyle='--')
    plt.ylabel("VH")
    plt.setp(ax4.get_xticklabels(), visible=False)
    ax5 = plt.subplot(615)
    plt.plot(x2,y5,color='blue')
    plt.plot(x2, y5bis,color='red',linestyle='--')
    plt.ylabel("VH/VV")
    plt.setp(ax5.get_xticklabels(),rotation=False)
    plt.legend((p1[0],p2[0]),("Irrigué","Non Irrigué"))
    ax6 = plt.subplot(616)
    plt.bar(x3,y6,color='blue',width=1)
    plt.ylabel("pluviométrie en mm")
    plt.setp(ax6.get_xticklabels(),rotation=90)
    

    
def indexdate(df,intervalle_inf,out,intervalle_sup=len(df.index)):
    globals()["%s"% out ] = df.rename(index=lambda x: x[intervalle_inf:intervalle_sup])
    globals()["%s"%out].sort_index(inplace=True)
    globals()["%s"%out].index=pd.to_datetime(globals()["%s"%out].index,format="%Y%m%d")
    
def col_sqlite(path,name,list_bd_drop):
    dfnames=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt",sep=',', header=None)
    df1=dfnames.T
    df1.columns=["band_name"]
    colnames=list(df1.band_name.apply(lambda s: s[2:-1]))
    
    df=pd.read_csv(path)
    globals()["%s"% name ]=df.groupby("originfid").mean()
    labcroirr=globals()["%s"% name ].labcroirr
    globals()["%s"% name ].drop(columns=list_bd_drop,inplace=True)
    globals()["%s"% name ]=globals()["%s"% name ].T

    globals()["%s"% name ]["band_names"]=colnames
    globals()["%s"% name ]["date"] = globals()["%s"% name ].band_names.apply(lambda s: s[-8:])
    globals()["%s"% name ].set_index("band_names",inplace=True)
    globals()["%s"% name ]=globals()["%s"% name ].T
    globals()["%s"% name ]["labcroirr"]= labcroirr

if __name__ == '__main__':
    d={}
    d["SAVE"]="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/"
#    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/tmp/TEST_ANALYSE_SIGNAL/ZONE_TEST_MAIZE.csv")
#    dfpar=df.groupby("originfid").mean()
    label=[1,11]
    polarisation=["des_vv","asc_vv","des_vh","asc_vh","userfeature"]
    indice=["NDVI","NDWI","Brightness"]
    features=polarisation+indice
    drop_band=['X', 'Y', 'region', 'labcroirr',"alt_band_0"]
    
   # =============================================================================
#     SAFRAN
# =============================================================================
    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/SAFRAN_TCJ.csv")
    date=sorted(list(set(df.DATE)))
    
#    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/SAFRAN/SAFRAN_TCJ_NORD.csv")
#    SAFRAN_EST_TCJ=df.groupby('gid').mean() 
#    gid=SAFRAN_EST_TCJ.index
#    df_ESTCJ=SAFRAN_EST_TCJ.drop(columns=['X','Y','labelirr', 'labelcrirr','originfid','area','surf_parc',"id","labcroirr"])
#    dfEST_TCJ=df_ESTCJ.T
#    dfEST_TCJ['date']=date
#    dfEST_TCJ.set_index("date",inplace=True)
#    dfEST_TCJ.index=pd.to_datetime(dfEST_TCJ.index,format="%Y%m%d")
    
# =============================================================================
#     Ceate plot
# =============================================================================
    for m in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/SAFRAN/"):
        print (m)
        tile=m[-9:-4]
        print (tile)
        df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/SAFRAN/%s"% m)
        globals()["SAFR%s"% (tile)]=df.groupby('gid').mean() 
        gid=globals()["SAFR%s"% (tile)].index
        globals()["dfSAFR%s"% (tile)]=globals()["SAFR%s"% (tile)].drop(columns=['X','Y','labelirr', 'labelcrirr','originfid','area','surf_parc',"id","labcroirr"])
        globals()["dfSAFR%s"% (tile)]=globals()["dfSAFR%s"% (tile)].T
        globals()["dfSAFR%s"% (tile)]['date']=date
        globals()["dfSAFR%s"% (tile)].set_index("date",inplace=True)
        globals()["dfSAFR%s"% (tile)].index=pd.to_datetime(globals()["dfSAFR%s"% (tile)].index,format="%Y%m%d")

    for z in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/tmp/TEST_ANALYSE_SIGNAL/"):
        print(z)
        tile=z[-9:-4]
        print (tile)
        if z != 'DT_MAIZE_TDJ_N.csv':
            col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/tmp/TEST_ANALYSE_SIGNAL/%s"%(z),"df%s"%(tile),drop_band[0:4])    
        else: 
            col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/tmp/TEST_ANALYSE_SIGNAL/%s"%(z),"df%s"%(tile),drop_band)
            
        for p in polarisation:
            SAR_process_db(label,globals()["df%s"% tile],p)
            
        for ind in indice:
            print (ind)
            Optique_Process(label,globals()["df%s"% tile],ind)
            
        for f in indice:
            indexdate(globals()["df%s1"% (f)],-8,f.upper()+"1")
            indexdate(globals()["df%s11"% (f)],-8,f.upper()+"11")

        globals()["VV%s1"% (tile)]=pd.concat([dbdfdes_vv1,dbdfasc_vv1])
        indexdate(globals()["VV%s1"% (tile)],-8,"VV1")
    
        globals()["VH%s1"% (tile)]=pd.concat([dbdfdes_vh1,dbdfasc_vh1])
        indexdate(globals()["VH%s1"% (tile)],-8,"VH1")
    
        
        globals()["VV%s11"% (tile)]=pd.concat([dbdfdes_vv11,dbdfasc_vv11])
        indexdate(globals()["VV%s11"% (tile)],-8,"VV11")
        
        globals()["VH%s11"% (tile)]=pd.concat([dbdfdes_vh11,dbdfasc_vh11])
        indexdate(globals()["VH%s11"% (tile)],-8,"VH11")
    
        
        indexdate(dbdfuserfeature1,-8,"VH_VV1")
        indexdate(dbdfuserfeature11,-8,"VH_VV11")
        print(globals()["dfSAFR%s"% (tile)]) #" VERIFIER COCONDANCE DES METEO
        
        pltmutli(NDVI1.index,VV1.index,NDVI1,NDVI11,NDWI1,NDWI11,VV1,VV11,VH1,VH11,VH_VV1,VH_VV11,globals()["dfSAFR%s"% (tile)].index,globals()["dfSAFR%s"% (tile)].iloc[:,1])    
        plt.savefig(d["SAVE"]+"comparaison_IRR_NIRR_%s.png"% tile)

    
# =============================================================================
#     GEstion DATA TDJ add nom band + date
# =============================================================================
    col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/tmp/TEST_ANALYSE_SIGNAL/DT_MAIZE_TCJ_O.csv",'dfTDJ',drop_band[0:4])
   
    for p in polarisation:
        SAR_process_db(label,dfTDJ,p)
        
    for ind in indice:
        print (ind)
        Optique_Process(label,dfTDJ,ind)
        
    for f in indice:
        indexdate(globals()["df%s1"% f],-8,f.upper()+"1")
        indexdate(globals()["df%s11"% f],-8,f.upper()+"11")

    VV1=pd.concat([dbdfdes_vv1,dbdfasc_vv1])
    indexdate(VV1,-8,"VV1")

    VH1=pd.concat([dbdfdes_vh1,dbdfasc_vh1])
    indexdate(VH1,-8,"VH1")

    
    VV11=pd.concat([dbdfdes_vv11,dbdfasc_vv11])
    indexdate(VV11,-8,"VV11")
    
    VH11=pd.concat([dbdfdes_vh11,dbdfasc_vh11])
    indexdate(VH11,-8,"VH11")

    
    indexdate(dbdfuserfeature1,-8,"VH_VV1")
    indexdate(dbdfuserfeature11,-8,"VH_VV11")
    
    pltmutli(NDVI1.index,VV1.index,NDVI1,NDVI11,NDWI1,NDWI11,VV1,VV11,VH1,VH11,VH_VV1,VH_VV11,dfSAFRTCJ_O.index,dfSAFRTCJ_O.iloc[:,1])
    plt.savefig(d["SAVE"]+"comparaison_IRR_NIRR_TDJ_NORD.png")
#    

#    sns.set(style="darkgrid")
#    sns.set_context('paper')
#    plt.plot(VV1,color='blue')
#    plt.plot(VVa1,color='red')
#    plt.xticks(rotation=90)
#    plt.show()