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
from STAT_ZONAL_SPECRTE import *
from scipy import stats
import TEST_ANALYSE_SIGNATURE


def calcumul_index(path,x,name_champ_label,indice2,list_drop,pathlist_names_feature):
        """ 
        Allows calculating the index cumul by sqlite OTB """
        sql=sqlite3.connect(path)
        df=pd.read_sql_query("SELECT * FROM output", sql)
        df=df.groupby("originfid").mean()
        if 'band' in df.columns[6] :
            col_sqlite(path,x,list_drop,pathlist_names_feature)
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
    tile =["TDJ","TCJ","TYP"]    #nom de fichier avec les stats 
#    features=['NDVI','NDWI','NDRE1',"NDRE2",'asc_vv','des_vv','asc_vh','des_vh','des_userfeature1','asc_userfeature1']
    
    features=['NDVI','NDWI','asc_vv','des_vv','asc_vh','des_vh','des_userfeature1','asc_userfeature1']
    
    for i in tile :
        for j in features:
            print (i)
            if i == "TDJ":
                calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/"+str(i)+"_S1_S2"+"/learningSamples/Samples_region_1_seed0_learn.sqlite","df45","labcroirr",j,list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
            elif i =="TYP":
                calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/"+str(i)+"_S1_S2"+"/learningSamples/Samples_region_1_seed0_learn.sqlite",'45','labcroirr',j,list_bd_d, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR_TYP.txt") 
            else:
                calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/"+str(i)+"_S1_S2"+"/learningSamples/Samples_region_1_seed0_learn.sqlite",'45','labcroirr',j.lower(),list_bd_d, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR_TYP.txt")
        if i =="TCJ":   
            globals()["df_mean_%s"%j].columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
            globals()["_%s"% (j)],globals()["b_sup%s"% (j)]=stats.t.interval(0.95,globals()["df_mean_%s"%j].shape[1]-1,loc= globals()["df_mean_%s"%j].T,scale=stats.sem(globals()["df_mean_%s"%j].T))
            globals()["_%s"% (j)]=pd.DataFrame( globals()["_%s"% (j)])
            globals()["_%s"% (j)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower",'Peas']
            globals()["b_sup%s"% (j)]=pd.DataFrame( globals()["b_sup%s"% (j)])
            globals()["b_sup%s"% (j)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
            plotindicecum(globals()["df_mean_%s"%j],"Maize_Irr","Maize_Nirr",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#            plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maize2017%s.png"% i)
            plotindicecum(globals()["df_mean_%s"%j],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#            plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Soybean2017%s.png"% i)
        else:
            globals()["df_mean_%s"%j].columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
            globals()["_%s"% (j)],globals()["b_sup%s"% (j)]=stats.t.interval(0.95,globals()["df_mean_%s"%j].shape[1]-1,loc= globals()["df_mean_%s"%j].T,scale=stats.sem(globals()["df_mean_%s"%j].T))
            globals()["_%s"% (j)]=pd.DataFrame( globals()["_%s"% (j)])
            globals()["_%s"% (j)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
            globals()["b_sup%s"% (j)]=pd.DataFrame( globals()["b_sup%s"% (j)])
            globals()["b_sup%s"% (j)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
            plotindicecum(globals()["df_mean_%s"%j],"Maize_Irr","Maize_Nirr",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#            plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maize2017%s.png"% i)
            plotindicecum(globals()["df_mean_%s"%j],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (j)],globals()["b_sup%s"% (j)],j)
#            plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Soybean2017%s.png"% i)
# =============================================================================
    #     2017  revoir path
    # =============================================================================
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','ndvi',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','ndwi',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDRE1',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDRE2',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDRE3',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")


    index=['ndvi','ndwi','NDRE1',"NDRE2","NDRE3"]
    for i in index:  
        globals()["df_mean_%s"%i].columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["df_mean_%s"%i].shape[1]-1,loc= globals()["df_mean_%s"%i].T,scale=stats.sem(globals()["df_mean_%s"%i].T))
        globals()["_%s"% (i)]=pd.DataFrame( globals()["_%s"% (i)])
        globals()["_%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["b_sup%s"% (i)]=pd.DataFrame( globals()["b_sup%s"% (i)])
        globals()["b_sup%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        plotindicecum(globals()["df_mean_%s"%i],"Maize_Irr","Maize_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maize2017%s.png"% i)
        plotindicecum(globals()["df_mean_%s"%i],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Soybean2017%s.png"% i)
#    
    # =============================================================================
    #     Test sur TYP
    # =============================================================================
    d={} 
    d['TYP']="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TYP_S1_S2/learningSamples"
    calcumul_index(d["TYP"]+"/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','ndvi', list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index(d["TYP"]+"/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','ndwi', list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index(d["TYP"]+"/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','NDRE1', list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index(d["TYP"]+"/Samples_region_1_seed4_learn.sqlite",'df45','labcroirr','NDRE2', list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")

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
        
    # =============================================================================
    #   TDJ 2017
    # =============================================================================
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDVI',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDWI',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDRE1',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDRE2',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','asc_vv',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','asc_vh',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','des_vv',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','des_vh',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','des_userfeature1',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TDJ_S1_S2_carte_leve_data/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','asc_userfeature1',list_bd_d,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")

    
    
    
    
    index=['NDVI','NDWI','NDRE1',"NDRE2",'asc_vv','des_vv','asc_vh','des_vh','des_userfeature1','asc_userfeature1']
    for i in index:  
        globals()["df_mean_%s"%i].columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["df_mean_%s"%i].shape[1]-1,loc= globals()["df_mean_%s"%i].T,scale=stats.sem(globals()["df_mean_%s"%i].T))
        globals()["_%s"% (i)]=pd.DataFrame( globals()["_%s"% (i)])
        globals()["_%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
        globals()["b_sup%s"% (i)]=pd.DataFrame( globals()["b_sup%s"% (i)])
        globals()["b_sup%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
        plotindicecum(globals()["df_mean_%s"%i],"Maize_Irr","Maize_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
#        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maize2018%s.png"% i)
        plotindicecum(globals()["df_mean_%s"%i],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
#        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Soybean2018%s.png"% i)
    
    # =============================================================================
    #    2018     
    # =============================================================================
    


    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDVI',list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDWI',list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDRE1',list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDRE2',list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','NDRE3',list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")


    index=['NDVI','NDWI','NDRE1',"NDRE2","NDRE3"]
    for i in index:  
        globals()["df_mean_%s"%i].columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["df_mean_%s"%i].shape[1]-1,loc= globals()["df_mean_%s"%i].T,scale=stats.sem(globals()["df_mean_%s"%i].T))
        globals()["_%s"% (i)]=pd.DataFrame( globals()["_%s"% (i)])
        globals()["_%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["b_sup%s"% (i)]=pd.DataFrame( globals()["b_sup%s"% (i)])
        globals()["b_sup%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        plotindicecum(globals()["df_mean_%s"%i],"Maize_Irr","Maize_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maize2018%s.png"% i)
        plotindicecum(globals()["df_mean_%s"%i],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_Soybean2018%s.png"% i)
        
# equation NDRE 1
#        _b5a ; _b8a
#esaution NDRE 2
#        _b8a : b6
#equation NDRE 3
    # =============================================================================
    #  Cumul des simga 0
    # =============================================================================

    list_bd_drop=["region","labcroirr","ogc_fid"]

    # =============================================================================
    #   SAR 2017
    # =============================================================================
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TCJ_S1_S2/learningSamples/Samples_region_1_seed0_learn.sqlite",'45','labcroirr','asc_vv',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','asc_vh',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','des_vv',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','des_vh',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','des_userfeature1',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed0_learn.sqlite",'df45','labcroirr','asc_userfeature1',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")

   
    index=['asc_vv','des_vv','asc_vh','des_vh','des_userfeature1','asc_userfeature1']
    for i in index:  
        globals()["df_mean_%s"%i].columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["df_mean_%s"%i].shape[1]-1,loc= globals()["df_mean_%s"%i].T,scale=stats.sem(globals()["df_mean_%s"%i].T))
        globals()["_%s"% (i)]=pd.DataFrame( globals()["_%s"% (i)])
        globals()["_%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        globals()["b_sup%s"% (i)]=pd.DataFrame( globals()["b_sup%s"% (i)])
        globals()["b_sup%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower","Peas"]
        plotindicecum(globals()["df_mean_%s"%i],"Maize_Irr","Maize_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maizeSAR2017%s.png"% i)
        plotindicecum(globals()["df_mean_%s"%i],"Soybean_Irr","Soybean_Nirr",globals()["_%s"% (i)],globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_SoybeanSAR2017%s.png"% i)
        
  # =============================================================================
#     Cumul de l'humidité du sol (SM)
# =============================================================================      
    list_bd_drop=["labcroirr","ogc_fid",'alt_band_0']
    calcumul_index("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/TCJ_CUMUL_SM/Samples_region_2_seed3_learn.sqlite",'dfSM','labcroirr','SM',list_bd_drop, "/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_SM.txt")
    df_mean_SM.columns=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]

    index=["SM"]
    for i in index:
        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["df_mean_%s"%i].shape[1]-1,loc= globals()["df_mean_%s"%i].T,scale=stats.sem(globals()["df_mean_%s"%i].T))
        globals()["_%s"% (i)]=pd.DataFrame( globals()["_%s"% (i)])
        globals()["_%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
        globals()["b_sup%s"% (i)]=pd.DataFrame( globals()["b_sup%s"% (i)])
        globals()["b_sup%s"% (i)].index=["Maize_Irr","Soybean_Irr","Others","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"]
        plotindicecum(globals()["df_mean_%s"%i],"Maize_Irr","Maize_Nirr", globals()["b_%s"% (i)] ,globals()["b_sup%s"% (i)],i)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_CUMUL_temporelle/cumul_maizeSAR2017%s.png"% i)
        
        
        sql=sqlite3.connect("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/"+str(i)+"_S1_S2"+"/learningSamples/Samples_region_1_seed0_learn.sqlite")
        df=pd.read_sql_query("SELECT * FROM output", sql)
        df=df.groupby("originfid").mean()

