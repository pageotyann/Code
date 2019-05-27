#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:23:03 2019

@author: pageot
"""



import sqlite3
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
import STAT_ZONAL_SPECRTE
from scipy import stats

def calcumul_index(path,x,name_champ_label,indice2):
        """ 
        Allows calculating the index cumul by sqlite OTB """
        sqlite_df(path,x)
        label = globals()["%s"%x][name_champ_label]
        print(indice2)
        if indice2 not in ['ndvi', 'ndwi']:
            name_indice=indice2
            band1_indice=input("band :")
            band2_indice=input("band :")
            df_b1 = globals()["%s"%x].filter(like=band1_indice)
            df_b2 = globals()["%s"%x].filter(like=band2_indice)
            df_b1_col = df_b1.rename(columns=lambda x: x[-4:])
            df_b2_col = df_b2.rename(columns=lambda x: x[-4:])
            df_indice = (df_b2_col - df_b1_col)/(df_b2_col + df_b1_col)
            globals()["df_%s"%indice2] = df_indice.cumsum(axis=1)

        else:
            df_indice = globals()["%s"%x].filter(like=indice2)
            df_indice_col = df_indice.rename(columns=lambda x: x[-4:])
            globals()["df_%s"%indice2] = df_indice_col.cumsum(axis=1)
            
        globals()["df_%s"%indice2][name_champ_label]=label
        globals()["df_mean_%s"%indice2]=globals()["df_%s"%indice2].groupby(name_champ_label).mean().T 
        return globals()["df_mean_%s"%indice2]

            
def plotindicecum(x,champ1,champ2,confiancesup,confianceinf,indice):
    fig, ax = plt.subplots(figsize=(20, 7))
    p1=plt.plot(x.index,x[champ1],color='blue')
    p2=plt.plot(x.index,x[champ2],color='red')
    plt.fill_between(x.index, confiancesup.T[champ1], confianceinf.T[champ1], facecolor='blue', alpha=0.2)
    plt.fill_between(x.index, confiancesup.T[champ2], confianceinf.T[champ2], facecolor='red', alpha=0.2)
    plt.title(r'Cumul des '+ indice+' et intervalle $\pm \sigma$ en 2017')
    plt.legend((p1[0],p2[0]),("Irr","Nirr"))
    plt.xlabel('Dates interpollees')
    plt.ylabel('Cumul '+ indice+' moyen')
    
    
if __name__ == '__main__':
    
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','ndvi')
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','ndwi')
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','NDRE1')
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','NDRE2')
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','NDRE3')


    index=['ndvi','ndwi','NDRE1',"NDRE2","NDRE3"]
    for i in index:  
        globals()["df_mean_%s"%i].columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["df_mean_%s"%i].shape[1]-1,loc= globals()["df_mean_%s"%i].T,scale=stats.sem(globals()["df_mean_%s"%i].T))
        globals()["_%s"% (i)]=pd.DataFrame( globals()["_%s"% (i)])
        globals()["_%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["b_sup%s"% (i)]=pd.DataFrame( globals()["b_sup%s"% (i)])
        globals()["b_sup%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        plotindicecum(globals()["df_mean_%s"%i],"Maize_Irr","Maize_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/cumul_maize%s.png"% i)
        plotindicecum(globals()["df_mean_%s"%i],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Soybean%s.png"% i)
    
# =============================================================================
#     Test sur TYP
# =============================================================================
    d={} 
    d['TYP']="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TYP_S2/learningSamples"
    calcumul_index(d["TYP"]+"/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','ndvi')
    calcumul_index(d["TYP"]+"/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','ndwi')
    calcumul_index(d["TYP"]+"/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','NDRE1')
    calcumul_index(d["TYP"]+"/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','NDRE2')

    index=['ndvi','ndwi','NDRE1',"NDRE2"]
    for i in index:  
        globals()["df_mean_%s"%i].columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["df_mean_%s"%i].shape[1]-1,loc= globals()["df_mean_%s"%i].T,scale=stats.sem(globals()["df_mean_%s"%i].T))
        globals()["_%s"% (i)]=pd.DataFrame( globals()["_%s"% (i)])
        globals()["_%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["b_sup%s"% (i)]=pd.DataFrame( globals()["b_sup%s"% (i)])
        globals()["b_sup%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        plotindicecum(globals()["df_mean_%s"%i],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maize_TYP%s.png"% i)