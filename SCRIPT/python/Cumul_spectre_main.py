#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:23:03 2019

@author: pageot
"""


import os
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
from STAT_ZONAL_SPECRTE import *
from scipy import stats
from TEST_ANALYSE_SIGNATURE import *

def calcumul_index_saison(path,x,name_champ_label,indice2,list_drop,pathlist_names_feature,years):
    
        sql=sqlite3.connect(path)
        df=pd.read_sql_query("SELECT * FROM output", sql)
        df=df.groupby("originfid").mean()
        if 'band' in df.columns[6] :
            globals()["df%s"%x]=col_sqlite(path,x,list_drop,pathlist_names_feature)
            label = globals()["df%s"%x][name_champ_label]
            globals()["%s"%x]=globals()["df%s"%x].astype(float)
            print(indice2)
            if indice2 not in ['NDVI', 'NDWI','SM','asc_vv','des_vv','asc_vh','des_vh','asc_userfeature1','des_userfeature1']:
                name_indice=indice2
                band1_indice=input("band ? :")
                band2_indice=input("band ? :")
                df_b1 = globals()["%s"%x].filter(like=band1_indice)
                df_b2 = globals()["%s"%x].filter(like=band2_indice)
                df_b1_col = df_b1.rename(columns=lambda x: x[-8:])
                df_b2_col = df_b2.rename(columns=lambda x: x[-8:])
                df_indice = (df_b2_col - df_b1_col)/(df_b2_col + df_b1_col)
                df_indice_col=df_indice.iloc[:-1]
                if years== 2017:
                    globals()["df_%s"%indice2] = df_indice_col.iloc[:,8:-3].cumsum(axis=1)
                else:
                    globals()["df_%s"%indice2] = df_indice_col.iloc[:,9:-3].cumsum(axis=1)
                globals()["df_%s"%indice2] = df_indice.cumsum(axis=1)
        
            else:
                if indice2 == "NDWI":
                    df_indice = globals()["df%s"%x].filter(like=indice2)
                    df_indice_col = df_indice.rename(columns=lambda x: x[-8:])
                    df_indice_col=df_indice_col.iloc[:-1]
                    df_indice_col=df_indice_col*-1
                else:
                    df_indice = globals()["df%s"%x].filter(like=indice2)
                    df_indice_col = df_indice.rename(columns=lambda x: x[-8:])
                    df_indice_col=df_indice_col.iloc[:-1]
                if years== 2017:
                    globals()["df_%s"%indice2] = df_indice_col.iloc[:,8:-3].cumsum(axis=1)
                else:
                    globals()["df_%s"%indice2] = df_indice_col.iloc[:,9:-3].cumsum(axis=1)
                
            globals()["df_%s"%indice2][name_champ_label]=label
            globals()["df_%s"%indice2]=globals()["df_%s"%indice2].astype(float)
            globals()["df_mean_%s"%indice2]=globals()["df_%s"%indice2].groupby(name_champ_label).mean().T 
            globals()["df_mean_%s"%indice2].index=pd.to_datetime(globals()["df_mean_%s"%indice2].index,format="%Y%m%d")
        else :
            label = df[name_champ_label]
            print(indice2)
            if indice2 not in ['ndvi', 'ndwi','asc_vv','des_vv','asc_vh','des_vh','asc_userfeature1','des_userfeature1','SM']:
                name_indice=indice2
                band1_indice=input("band ? :")
                band2_indice=input("band ? :")
                df_b1 = df.filter(like=band1_indice)
                df_b2 = df.filter(like=band2_indice)
                df_b1_col = df_b1.rename(columns=lambda x: x[-8:])
                df_b2_col = df_b2.rename(columns=lambda x: x[-8:])
                df_indice = (df_b2_col - df_b1_col)/(df_b2_col + df_b1_col)
                if years== 2017:
                    globals()["df_%s"%indice2] = df_indice_col.iloc[:,8:-3].cumsum(axis=1)
                else:
                    globals()["df_%s"%indice2] = df_indice_col.iloc[:,9:-3].cumsum(axis=1)
        
            else:
                df_indice = df.filter(like=indice2)
                df_indice_col = df_indice.rename(columns=lambda x: x[-8:])
                globals()["df_%s"%indice2] = df_indice_col.cumsum(axis=1)
                
            globals()["df_%s"%indice2][name_champ_label]=label
            globals()["df_mean_%s"%indice2]=globals()["df_%s"%indice2].groupby(name_champ_label).mean().T
            globals()["df_mean_%s"%indice2].index=pd.to_datetime(globals()["df_mean_%s"%indice2].index,format="%Y%m%d")
        return globals()["df_mean_%s"%indice2], globals()["df_%s"%indice2]

def calcumul_index(path,x,name_champ_label,indice2,list_drop,pathlist_names_feature):
        """ 
        Allows calculating the index cumul by sqlite OTB """
        sql=sqlite3.connect(path)
        df=pd.read_sql_query("SELECT * FROM output", sql)
        df=df.groupby("originfid").mean()
        if 'band' in df.columns[6] :
            globals()["df%s"%x]=col_sqlite(path,x,list_drop,pathlist_names_feature)
            label = globals()["df%s"%x][name_champ_label]
            globals()["%s"%x]=globals()["df%s"%x].astype(float)
            print(indice2)
            if indice2 not in ['NDVI', 'NDWI','SM','asc_vv','des_vv','asc_vh','des_vh','asc_userfeature1','des_userfeature1']:
                name_indice=indice2
                band1_indice=input("band ? :")
                band2_indice=input("band ? :")
                df_b1 = globals()["%s"%x].filter(like=band1_indice)
                df_b2 = globals()["%s"%x].filter(like=band2_indice)
                df_b1_col = df_b1.rename(columns=lambda x: x[-8:])
                df_b2_col = df_b2.rename(columns=lambda x: x[-8:])
                df_indice = (df_b2_col - df_b1_col)/(df_b2_col + df_b1_col)
                globals()["df_%s"%indice2] = df_indice.cumsum(axis=1)
        
            else:
                df_indice = globals()["df%s"%x].filter(like=indice2)
                df_indice_col = df_indice.rename(columns=lambda x: x[-8:])
                df_indice_col=df_indice_col.iloc[:-1]
                globals()["df_%s"%indice2] = df_indice_col.cumsum(axis=1)
                
            globals()["df_%s"%indice2][name_champ_label]=label
            globals()["df_%s"%indice2]=globals()["df_%s"%indice2].astype(float)
            globals()["df_mean_%s"%indice2]=globals()["df_%s"%indice2].groupby(name_champ_label).mean().T 
            globals()["df_mean_%s"%indice2].index=pd.to_datetime(globals()["df_mean_%s"%indice2].index,format="%Y%m%d")
        else :
            label = df[name_champ_label]
            print(indice2)
            if indice2 not in ['ndvi', 'ndwi','asc_vv','des_vv','asc_vh','des_vh','asc_userfeature1','des_userfeature1','SM']:
                name_indice=indice2
                band1_indice=input("band ? :")
                band2_indice=input("band ? :")
                df_b1 = df.filter(like=band1_indice)
                df_b2 = df.filter(like=band2_indice)
                df_b1_col = df_b1.rename(columns=lambda x: x[-8:])
                df_b2_col = df_b2.rename(columns=lambda x: x[-8:])
                df_indice = (df_b2_col - df_b1_col)/(df_b2_col + df_b1_col)
                globals()["df_%s"%indice2] = df_indice.cumsum(axis=1)
        
            else:
                df_indice = df.filter(like=indice2)
                df_indice_col = df_indice.rename(columns=lambda x: x[-8:])
                globals()["df_%s"%indice2] = df_indice_col.cumsum(axis=1)
                
            globals()["df_%s"%indice2][name_champ_label]=label
            globals()["df_mean_%s"%indice2]=globals()["df_%s"%indice2].groupby(name_champ_label).mean().T
            globals()["df_mean_%s"%indice2].index=pd.to_datetime(globals()["df_mean_%s"%indice2].index,format="%Y%m%d")
        return globals()["df_mean_%s"%indice2], globals()["df_%s"%indice2]
            
def plotindicecum(x,champ1,champ2,confiancesup,confianceinf,indice):
    fig, ax = plt.subplots(figsize=(20, 7))
    p1=plt.plot(x.index,x[champ1],color='blue')
    p2=plt.plot(x.index,x[champ2],color='red')
    plt.fill_between(x.index, confiancesup.T[champ1], confianceinf.T[champ1], facecolor='blue', alpha=0.2)
    plt.fill_between(x.index, confiancesup.T[champ2], confianceinf.T[champ2], facecolor='red', alpha=0.2)
    plt.title(r'Cumul des '+ indice+' et intervalle $\pm \sigma$ en 2017')
    plt.legend((p1[0],p2[0]),("Irr","Nirr"))
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.xlabel('Dates interpollees')
    plt.ylabel('Cumul '+ indice+' moyen')
    
    
if __name__ == '__main__':
    list_bd_drop=["region","labcroirr","ogc_fid"]
    list_bd_d=["region","labcroirr","ogc_fid","alt_band_0"]
    list_drop_bv=["labcroirr","ogc_fid","alt_band_0"]
    list_drop=["labcroirr","ogc_fid"]
    tile =["TDJ","TYP","TCJ","ADOUR","TARN","NESTE"]    #nom de fichier avec les stats 
    BV=["ADOUR","TARN","NESTE"]
    #    features=['NDVI','NDWI','NDRE1',"NDRE2",'asc_vv','des_vv','asc_vh','des_vh','des_userfeature1','asc_userfeature1']
    
    features=['NDVI','NDWI','asc_vv','des_vv','asc_vh','des_vh','des_userfeature1','asc_userfeature1']
    
#    for i in os.listdir( "/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"):
#        print (r" watershed : {}".format(i))
#        for j in features:
#            if "2017" in i:
#                calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"+str(i),'dfbv','labcroirr' ,j,list_drop_bv,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
#                if "NESTE" in i:
#                    globals()["df_mean_%s"%j].columns=["Maize","Soybean","Sorghum"]
#                    globals()["_%s"% (j)],globals()["b_sup%s"% (j)]=stats.t.interval(0.95,globals()["df_mean_%s"%j].shape[1]-1,loc= globals()["df_mean_%s"%j].T,scale=stats.sem(globals()["df_mean_%s"%j].T))
#                    globals()["_%s"% (j)]=pd.DataFrame( globals()["_%s"% (j)])
#                    globals()["_%s"% (j)].index=["Maize","Soybean","Sorghum"]
#                    globals()["b_sup%s"% (j)]=pd.DataFrame( globals()["b_sup%s"% (j)])
#                    globals()["b_sup%s"% (j)].index=["Maize","Soybean","Sorghum"]
#                    plotindicecum(globals()["df_mean_%s"%j],"Maize","Soybean",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#                    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_crops2017%s_%s.png"% (j,i[5:]))
#
#                else:
#                    globals()["df_mean_%s"%j].columns=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#                    globals()["_%s"% (j)],globals()["b_sup%s"% (j)]=stats.t.interval(0.95,globals()["df_mean_%s"%j].shape[1]-1,loc= globals()["df_mean_%s"%j].T,scale=stats.sem(globals()["df_mean_%s"%j].T))
#                    globals()["_%s"% (j)]=pd.DataFrame( globals()["_%s"% (j)])
#                    globals()["_%s"% (j)].index=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#                    globals()["b_sup%s"% (j)]=pd.DataFrame( globals()["b_sup%s"% (j)])
#                    globals()["b_sup%s"% (j)].index=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#                    plotindicecum(globals()["df_mean_%s"%j],"Maize_Irr","Maize_Nirr",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#                    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maize2017%s_%s.png"% (j,i[5:]))
#                    plotindicecum(globals()["df_mean_%s"%j],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#                    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Soybean2017%s_%s.png"% (j,i[5:]))
#            else:
#                calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"+str(i),'dfbv','labcroirr' ,j,list_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TYN2018.txt")
#                if "NESTE" in i:
#                    globals()["df_mean_%s"%j].columns=["Maize","Soybean","Sorghum","Sunflower"]
#                    globals()["_%s"% (j)],globals()["b_sup%s"% (j)]=stats.t.interval(0.95,globals()["df_mean_%s"%j].shape[1]-1,loc= globals()["df_mean_%s"%j].T,scale=stats.sem(globals()["df_mean_%s"%j].T))
#                    globals()["_%s"% (j)]=pd.DataFrame( globals()["_%s"% (j)])
#                    globals()["_%s"% (j)].index=["Maize","Soybean","Sorghum","Sunflower"]
#                    globals()["b_sup%s"% (j)]=pd.DataFrame( globals()["b_sup%s"% (j)])
#                    globals()["b_sup%s"% (j)].index=["Maize","Soybean","Sorghum","Sunflower"]
#                    plotindicecum(globals()["df_mean_%s"%j],"Maize","Soybean",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#                    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_crops2018%s_%s.png"% (j,i[5:]))
#                else:
#                    globals()["df_mean_%s"%j].columns=["Maize_Irr",'Maize_Nirr',"Soybean_Irr","Soybean_Nirr","Sorghum","Sunflower"]
#                    globals()["_%s"% (j)],globals()["b_sup%s"% (j)]=stats.t.interval(0.95,globals()["df_mean_%s"%j].shape[1]-1,loc= globals()["df_mean_%s"%j].T,scale=stats.sem(globals()["df_mean_%s"%j].T))
#                    globals()["_%s"% (j)]=pd.DataFrame( globals()["_%s"% (j)])
#                    globals()["_%s"% (j)].index=["Maize_Irr",'Maize_Nirr',"Soybean_Irr","Soybean_Nirr","Sorghum","Sunflower"]
#                    globals()["b_sup%s"% (j)]=pd.DataFrame( globals()["b_sup%s"% (j)])
#                    globals()["b_sup%s"% (j)].index=["Maize_Irr",'Maize_Nirr',"Soybean_Irr","Soybean_Nirr","Sorghum","Sunflower"]
#                    plotindicecum(globals()["df_mean_%s"%j],"Maize_Irr","Maize_Nirr",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#                    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Maize2018%s_%s.png"% (j,i[5:]))
#                    plotindicecum(globals()["df_mean_%s"%j],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#                    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Soybean2018%s_%s.png"% (j,i[5:]))

#

## =============================================================================
#    graphique paper cumul
#  =============================================================================
    for bv in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"):
        print (bv)
        for j in ["NDVI","NDWI","NDRE1","des_userfeature1","des_vv","des_vh"]:
            if "2017" in bv:
                print ('bv')
                if "NESTE" in bv:
                    z=bv[:5]
#                    calcumul_index_saison("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"+str(bv),'dfbv','labcroirr',j,list_drop_bv,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt",'2017')
#                    globals()["df_mean_%s"%j].columns=["Maize","Soybean","Sorghum"]
#                    globals()["df_mean_%s%s"%(z,j)]=globals()["df_mean_%s"%j]
#                    globals()["_%s%s"% (z,j)],globals()["b_sup%s%s"% (z,j)]=stats.t.interval(0.95,globals()["df_mean_%s%s"%(z,j)].shape[1]-1,loc= globals()["df_mean_%s%s"%(z,j)].T,scale=stats.sem(globals()["df_mean_%s%s"%(z,j)].T))
#                    globals()["_%s%s"% (z,j)]=pd.DataFrame( globals()["_%s%s"% (z,j)])
#                    globals()["_%s%s"% (z,j)].index=["Maize","Soybean","Sorghum"]
#                    globals()["b_sup%s%s"% (z,j)]=pd.DataFrame( globals()["b_sup%s%s"% (z,j)])
#                    globals()["b_sup%s%s"% (z,j)].index=["Maize","Soybean","Sorghum"]
                else:
                    z=bv[:5]
                    calcumul_index_saison("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"+str(bv),'dfbv','labcroirr' ,j,list_drop_bv,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt",'2017')
                    globals()["df_mean_%s"%j].columns=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
                    globals()["df_mean_%s%s"%(z,j)]=globals()["df_mean_%s"%j]
                    globals()["_%s%s"% (z,j)],globals()["b_sup%s%s"% (z,j)]=stats.t.interval(0.95,globals()["df_mean_%s%s"%(z,j)].shape[1]-1,loc= globals()["df_mean_%s%s"%(z,j)].T,scale=stats.sem(globals()["df_mean_%s%s"%(z,j)].T))
                    globals()["_%s%s"% (z,j)]=pd.DataFrame( globals()["_%s%s"% (z,j)])
                    globals()["_%s%s"% (z,j)].index=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
                    globals()["b_sup%s%s"% (z,j)]=pd.DataFrame( globals()["b_sup%s%s"% (z,j)])
                    globals()["b_sup%s%s"% (z,j)].index=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#            
#            else:
#                 if "NESTE" in bv:
#                    z=bv[:5]
##                    calcumul_index_saison("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"+str(bv),'dfbv','labcroirr' ,j,list_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TYN2018.txt",'2018')
##                    globals()["df_mean_%s"%j].columns=["Maize","Soybean","Sorghum","Sunflower"]
##                    globals()["df_mean_%s%s"%(z,j)]=globals()["df_mean_%s"%j]
##                    globals()["_%s%s"% (z,j)],globals()["b_sup%s%s"% (z,j)]=stats.t.interval(0.95,globals()["df_mean_%s%s"%(z,j)].shape[1]-1,loc= globals()["df_mean_%s%s"%(z,j)].T,scale=stats.sem(globals()["df_mean_%s%s"%(z,j)].T))
##                    globals()["_%s%s"% (z,j)]=pd.DataFrame( globals()["_%s%s"% (z,j)])
##                    globals()["_%s%s"% (z,j)].index=["Maize","Soybean","Sorghum","Sunflower"]
##                    globals()["b_sup%s%s"% (z,j)]=pd.DataFrame( globals()["b_sup%s%s"% (z,j)])
##                    globals()["b_sup%s%s"% (z,j)].index=["Maize","Soybean","Sorghum","Sunflower"]
#                 else:
#                    z=bv[:5]
#                    calcumul_index_saison("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"+str(bv),'dfbv','labcroirr' ,j,list_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TYN2018.txt",'2018')
#                    globals()["df_mean_%s"%j].columns=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#                    globals()["df_mean_%s%s"%(z,j)]=globals()["df_mean_%s"%j]
#                    globals()["_%s%s"% (z,j)],globals()["b_sup%s%s"% (z,j)]=stats.t.interval(0.95,globals()["df_mean_%s%s"%(z,j)].shape[1]-1,loc= globals()["df_mean_%s%s"%(z,j)].T,scale=stats.sem(globals()["df_mean_%s%s"%(z,j)].T))
#                    globals()["_%s%s"% (z,j)]=pd.DataFrame( globals()["_%s%s"% (z,j)])
#                    globals()["_%s%s"% (z,j)].index=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#                    globals()["b_sup%s%s"% (z,j)]=pd.DataFrame( globals()["b_sup%s%s"% (z,j)])
#                    globals()["b_sup%s%s"% (z,j)].index=["Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]

    fig, ax = plt.subplots(figsize=(20, 7))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    ax1=plt.subplot(231)
    plt.title("Watershed : Adour")
    p1=plt.plot(df_mean_ADOURNDVI.index,df_mean_ADOURNDVI["Maize_Irr"],color='blue')
    p2=plt.plot(df_mean_ADOURNDVI.index,df_mean_ADOURNDVI["Maize_Nirr"],color='red')
    plt.fill_between(df_mean_ADOURNDVI.index, b_supADOURNDVI.T["Maize_Irr"], _ADOURNDVI.T["Maize_Irr"], facecolor='blue', alpha=0.2)
    plt.fill_between(df_mean_ADOURNDVI.index,  b_supADOURNDVI.T["Maize_Nirr"], _ADOURNDVI.T["Maize_Nirr"], facecolor='red', alpha=0.2)
    plt.legend((p1[0],p2[0]),("Irr","Nirr"))
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.ylabel('Cumul %s moyen'%"NDVI")
    plt.setp(ax1.get_xticklabels(),visible=False)
    ax2=plt.subplot(232)
    plt.title("Watershed : Adour")
    p1=plt.plot(df_mean_ADOURNDWI.index,df_mean_ADOURNDWI["Maize_Irr"],color='blue')
    p2=plt.plot(df_mean_ADOURNDWI.index,df_mean_ADOURNDWI["Maize_Nirr"],color='red')
    plt.fill_between(df_mean_ADOURNDWI.index, b_supADOURNDWI.T["Maize_Irr"], _ADOURNDWI.T["Maize_Irr"], facecolor='blue', alpha=0.2)
    plt.fill_between(df_mean_ADOURNDWI.index,  b_supADOURNDWI.T["Maize_Nirr"], _ADOURNDWI.T["Maize_Nirr"], facecolor='red', alpha=0.2)
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.ylabel('Cumul %s moyen'%"NDWI")
    plt.setp(ax2.get_xticklabels(),visible=False)  
    ax3=plt.subplot(233)
    plt.title("Watershed : Adour")
    p1=plt.plot(df_mean_ADOURNDRE1.index,df_mean_ADOURNDRE1["Maize_Irr"],color='blue')
    p2=plt.plot(df_mean_ADOURNDRE1.index,df_mean_ADOURNDRE1["Maize_Nirr"],color='red')
    plt.fill_between(df_mean_ADOURNDRE1.index, b_supADOURNDRE1.T["Maize_Irr"], _ADOURNDRE1.T["Maize_Irr"], facecolor='blue', alpha=0.2)
    plt.fill_between(df_mean_ADOURNDRE1.index,  b_supADOURNDRE1.T["Maize_Nirr"], _ADOURNDRE1.T["Maize_Nirr"], facecolor='red', alpha=0.2)
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.ylabel('Cumul %s moyen'%"NDRE")
    plt.setp(ax3.get_xticklabels(),visible=False) 
    ax4=plt.subplot(234)
    plt.title("Watershed : Adour")
    p1=plt.plot(df_mean_ADOURdes_vv.index,df_mean_ADOURdes_vv["Maize_Irr"],color='blue')
    p2=plt.plot(df_mean_ADOURdes_vv.index,df_mean_ADOURdes_vv["Maize_Nirr"],color='red')
    plt.fill_between(df_mean_ADOURdes_vv.index, b_supADOURdes_vv.T["Maize_Irr"], _ADOURdes_vv.T["Maize_Irr"], facecolor='blue', alpha=0.2)
    plt.fill_between(df_mean_ADOURdes_vv.index,  b_supADOURdes_vv.T["Maize_Nirr"], _ADOURdes_vv.T["Maize_Nirr"], facecolor='red', alpha=0.2)
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.ylabel('Cumul %s moyen'%"VV")
    plt.xlabel('Dates interpollees')
    plt.legend((p1[0],p2[0]),("Irr","Nirr"))
    plt.setp(ax4.get_xticklabels(),visible=True, rotation=45)
    ax5=plt.subplot(235)
    plt.title("Watershed : Adour")
    p1=plt.plot(df_mean_ADOURdes_vh.index,df_mean_ADOURdes_vh["Maize_Irr"],color='blue')
    p2=plt.plot(df_mean_ADOURdes_vh.index,df_mean_ADOURdes_vh["Maize_Nirr"],color='red')
    plt.fill_between(df_mean_ADOURdes_vh.index, b_supADOURdes_vh.T["Maize_Irr"], _ADOURdes_vh.T["Maize_Irr"], facecolor='blue', alpha=0.2)
    plt.fill_between(df_mean_ADOURdes_vh.index,  b_supADOURdes_vh.T["Maize_Nirr"], _ADOURdes_vh.T["Maize_Nirr"], facecolor='red', alpha=0.2)
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.ylabel('Cumul %s moyen'%"VH")
    plt.setp(ax5.get_xticklabels(),visible=True, rotation=45) 
    ax6=plt.subplot(236)
    plt.title("Watershed : Adour")
    p1=plt.plot(df_mean_ADOURdes_userfeature1.index,df_mean_ADOURdes_userfeature1["Maize_Irr"],color='blue')
    p2=plt.plot(df_mean_ADOURdes_userfeature1.index,df_mean_ADOURdes_userfeature1["Maize_Nirr"],color='red')
    plt.fill_between(df_mean_ADOURdes_userfeature1.index, b_supADOURdes_userfeature1.T["Maize_Irr"], _ADOURdes_userfeature1.T["Maize_Irr"], facecolor='blue', alpha=0.2)
    plt.fill_between(df_mean_ADOURdes_userfeature1.index,  b_supADOURdes_userfeature1.T["Maize_Nirr"], _ADOURdes_userfeature1.T["Maize_Nirr"], facecolor='red', alpha=0.2)
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.ylabel('Cumul %s moyen'%"VH/VV")
    plt.xlabel('Dates interpollees')
    plt.setp(ax6.get_xticklabels(),visible=True,rotation=45) 

    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/ADOUR_BV_MAIZE_2017.png")
    
             

# =============================================================================
#     Cumul de l'humidité du sol (SM)
# =============================================================================      
#    list_bd_drop=["labcroirr","ogc_fid",'alt_band_0']
#    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TCJ_CUMUL_SM/Samples_region_2_seed3_learn.sqlite",'dfSM','labcroirr','SM',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_SM.txt")
#    df_mean_SM.columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#
#    index=["SM"]
#    for i in index:
#        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["df_mean_%s"%i].shape[1]-1,loc= globals()["df_mean_%s"%i].T,scale=stats.sem(globals()["df_mean_%s"%i].T))
#        globals()["_%s"% (i)]=pd.DataFrame( globals()["_%s"% (i)])
#        globals()["_%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#        globals()["b_sup%s"% (i)]=pd.DataFrame( globals()["b_sup%s"% (i)])
#        globals()["b_sup%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
#        plotindicecum(globals()["df_mean_%s"%i],"Maize_Irr","Maize_Nirr", globals()["b_%s"% (i)] ,globals()["b_sup%s"% (i)],i)
#        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maizeSAR2017%s.png"% i)
#        
#        
#        sql=sqlite3.connect("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/"+str(i)+"_S1_S2"+"/learningSamples/Samples_region_1_seed0_learn.sqlite")
#        df=pd.read_sql_query("SELECT * FROM output", sql)
#        df=df.groupby("originfid").mean()


#    sql=sqlite3.connect("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"+str(bv))
#    df=pd.read_sql_query("SELECT * FROM output", sql)
#    df=df.groupby("originfid").mean()
#    if 'band' in df.columns[6] :
#        globals()["df%s"%"x"]=col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"+str(bv),"x",list_drop_bv,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
#        label = globals()["df%s"%"x"]["labcroirr"]
#        globals()["%s"%"x"]=globals()["df%s"%"x"].astype(float)
#        print("NDVI")
#        if 'NDVI' not in ['NDVI', 'NDWI','SM','asc_vv','des_vv','asc_vh','des_vh','asc_userfeature1','des_userfeature1']:
#            name_indice="NDVI"
#            band1_indice=input("band ? :")
#            band2_indice=input("band ? :")
#            df_b1 = globals()["%s"%"x"].filter(like=band1_indice)
#            df_b2 = globals()["%s"%"x"].filter(like=band2_indice)
#            df_b1_col = df_b1.rename(columns=lambda x: x[-8:])
#            df_b2_col = df_b2.rename(columns=lambda x: x[-8:])
#            df_indice = (df_b2_col - df_b1_col)/(df_b2_col + df_b1_col)
#            globals()["df_%s"%"NDVI"] = df_indice.cumsum(axis=1)
#    
#        else:
#            df_indice = globals()["df%s"%"x"].filter(like="NDVI")
#            df_indice_col = df_indice.rename(columns=lambda x: x[-8:])
#            df_indice_col=df_indice_col.iloc[:-1]
#            globals()["df_%s"%'NDVI'] = df_indice_col.iloc[:,8:-3].cumsum(axis=1)
#            
#        globals()["df_%s"%'NDVI']['labcroirr']=label
#        globals()["df_%s"%'NDVI']=globals()["df_%s"%'NDVI'].astype(float)
#        globals()["df_mean_%s"%'NDVI']=globals()["df_%s"%'NDVI'].groupby('labcroirr').mean().T 
#        globals()["df_mean_%s"%'NDVI'].index=pd.to_datetime(globals()["df_mean_%s"%'NDVI'].index,format="%Y%m%d")
    
#    calcumul_index_saison("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/ADOUR_Samples_2018.sqlite",'dfbv','labcroirr' ,"NDWI",list_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TYN2018.txt",'2018')
#
#    plt.plot(df_mean_NDWI.index,df_mean_NDWI[1.0])
#    plt.plot(df_mean_NDWI.index,df_mean_NDWI[11.0])
