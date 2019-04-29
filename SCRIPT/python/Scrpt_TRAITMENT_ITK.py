#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:00:40 2019

@author: pageot
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

if __name__ == "__main__":
    # =============================================================================
    # Connection file sonde a ITK parcelle via Multi_Index    
    # =============================================================================
    Tensiodata=pd.DataFrame()
    for i in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_TERRAIN_PARTENAIRES/DONNEES_TERRAIN_ADOUR_2018/DONNEES_TENSIO/2017/"):
        if ".csv" in i:    
            print(i)   
            Nsonde=i[0:5]
            globals()["data%s"%Nsonde]=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_TERRAIN_PARTENAIRES/DONNEES_TERRAIN_ADOUR_2018/DONNEES_TENSIO/2017/"+i,sep=',',parse_dates=["Time"])
            globals()["data%s"%Nsonde]["Nsonde"]=Nsonde
            Tensiodata=Tensiodata.append(globals()["data%s"%Nsonde])
    Tensiodata.drop(columns=['Seconds','ExtInt'],inplace=True)
     
    sondes=Tensiodata.groupby("Nsonde")      
    Sonde01643=sondes.get_group('01643')
    
    dfITK=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_TERRAIN_PARTENAIRES/DONNEES_TERRAIN_ADOUR_2018/DONNEES_TENSIO/ITK_parcelle_ADOUR_2017_f1.csv")
    dFITKPHENO=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_TERRAIN_PARTENAIRES/DONNEES_TERRAIN_ADOUR_2018/DONNEES_TENSIO/ITK_parcelle_ADOUR_2017.csv")
    ITKADOUR=pd.concat([dFITKPHENO,dfITK],axis=1)
    ITKADOUR.drop(columns=["Vallée Adour","Téléphone"],inplace=True)
    
    
    
    
    # =============================================================================
    # itk_tHERMQIUE      
    # =============================================================================
    ITK_TST=pd.DataFrame()
    for i in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_ITK/TST_STAT"):
        if ".csv" in i:
            df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_ITK/TST_STAT/"+i)
            date=i[42:50]
            lab=df.labcroirr.astype(int)
            globals()["meanTSTITK%s"%date]=df.value_0/100-273.15
            globals()["meanTSTITK%s"%date].rename("TST_"+date,inplace=True)
            ITK_TST=ITK_TST.append(globals()["meanTSTITK%s"%date])
    ITK_TST.sort_index(inplace=True)
    ITK_TST[ITK_TST<= -1]=pd.NaT
    ITK_TST_drop=ITK_TST.dropna(how='all')
    plt.figure(figsize=(10,10))
    plt.plot(ITK_TST_drop)
    plt.xticks(rotation=90)
    plt.legend(ITK_TST_drop)
