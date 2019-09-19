#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 15:21:12 2019

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
from Cumul_spectre_main import *

if __name__ == '__main__':
    dfall2017=pd.DataFrame()
    colnames=[]
    for i in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_METEO_MONTH/"):
        if "18" not in i:
            sql=sqlite3.connect("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_METEO_MONTH/"+i)
            df=pd.read_sql_query("SELECT * FROM output", sql)
            df=df.groupby("originfid").mean()
            lab=df.labcroirr
            plui=df.value_0
            colnames.append(i[27:33])
            dfall2017=dfall2017.append(plui)
    dfall2017=dfall2017.T
    dfall2017.columns=colnames
    dfall2017["lab"]=lab
    dfall2017=dfall2017.reindex(columns = ['April_', 'May_Ra', 'June_R','July_R','August',"Septem","Octob_",'lab'])
    for i in set(lab):
        globals()["cropslab%s"%int(i)]=dfall2017[dfall2017.lab==i]
        globals()["cum_SAFRAN%s"%int(i)]=globals()["cropslab%s"%int(i)].iloc[:,:-1].T.cumsum()
        plt.plot(globals()["cum_SAFRAN%s"%int(i)].T.mean())
        plt.show()
    df2017_cum=cropslab1.iloc[:,:-1].T.cumsum(axis=1)
    plt.plot(df2017_cum)
