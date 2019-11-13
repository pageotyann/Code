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
#    Travail sur les deux zones NORD et SUD
    colnames=[]
    for y in ['2018','2017']:
        globals()["dfallSUD%s"% (y)]=pd.DataFrame()
        globals()["dfallNORD%s"% (y)]=pd.DataFrame()
        for i in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_METEO_MONTH/"):
            if "NORD" in i and y[-2:] in i :
                print (r" ici: %s" %i)
                sql=sqlite3.connect("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_METEO_MONTH/"+i)
                df=pd.read_sql_query("SELECT * FROM output", sql)
                df=df.groupby("originfid").mean()
                labnord=df.labcroirr
                pluiNORD=df.value_0
                colnames.append(i[27:31])
                globals()["dfallNORD%s"% y]=globals()["dfallNORD%s"% y].append(pluiNORD)
            elif "SUD" in i and y[-2:] in i:
                print (i)
                sql=sqlite3.connect("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_METEO_MONTH/"+i)
                df=pd.read_sql_query("SELECT * FROM output", sql)
                df=df.groupby("originfid").mean()
                labsud=df.labcroirr
                pluiSUD=df.value_0
                colnames.append(i[27:31])
                globals()["dfallSUD%s"% y]=globals()["dfallSUD%s"% y].append(pluiSUD)
                    
        for z in ["NORD","SUD"]:
            globals()["dfall%s%s"% (z,y)]=globals()["dfall%s%s"% (z,y)].T
            globals()["dfall%s%s"% (z,y)].columns=set(colnames)
            if z =="NORD":
                globals()["dfall%s%s"% (z,y)]["lab"]=labnord.astype(int)
            else:
                 globals()["dfall%s%s"% (z,y)]["lab"]=labsud.astype(int)
            globals()["dfall%s%s"% (z,y)]=globals()["dfall%s%s"% (z,y)].reindex(columns = ['Apri', 'May1', 'June','July','Augu',"Sept","Octo",'lab'])
            globals()["cropslab1%s%s"%(z,y)]=globals()["dfall%s%s"% (z,y)][globals()["dfall%s%s"% (z,y)].lab==1]
            
        globals()["cum_SAFRAN1NORD%s"%y]=globals()["cropslab1NORD%s"%(y)].iloc[:,:-1].T.cumsum()
        globals()["cum_SAFRAN1SUD%s"%y]=globals()["cropslab1SUD%s"%(y)].iloc[:,:-1].T.cumsum()    
#        Calcule des intervalles de confiances 
        globals()["_NORD%s"%y],globals()["b_NORD%s"%y]=stats.t.interval(0.95, globals()["cum_SAFRAN1NORD%s"%y].shape[1]-1,loc= globals()["cum_SAFRAN1NORD%s"%y].T,scale=stats.sem( globals()["cum_SAFRAN1NORD%s"%y].T))
        globals() ["_SUD%s"%y],globals()["b_SUD%s"%y]=stats.t.interval(0.95,globals()["cum_SAFRAN1SUD%s"%y].shape[1]-1,loc=globals()["cum_SAFRAN1SUD%s"%y].T,scale=stats.sem(globals()["cum_SAFRAN1SUD%s"%y].T))
    
        globals()["_NORD%s"%y]=pd.DataFrame(globals()["_NORD%s"%y])
        globals()["b_NORD%s"%y]=pd.DataFrame(globals()["b_NORD%s"%y])
        globals()["_SUD%s"%y]=pd.DataFrame(globals() ["_SUD%s"%y])
        globals()["b_SUD%s"%y]=pd.DataFrame(globals()["b_SUD%s"%y])
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax1=plt.subplot(221)
    sns.set(style="darkgrid")
    sns.set_context('paper')
    plt.title("Watershed : Adour")
    p1=plt.plot(cum_SAFRAN1NORD2018.T.mean(),color='blue')
    p2=plt.plot(cum_SAFRAN1SUD2018.T.mean(),color="red")
    plt.fill_between(cum_SAFRAN1NORD2018.index, b_NORD2018.mean(), _NORD2018.mean(), facecolor='blue', alpha=0.2)
    plt.fill_between(cum_SAFRAN1SUD2018.index,  b_SUD2018.mean(), _SUD2018.mean(), facecolor='red', alpha=0.2)
    plt.legend((p1[0],p2[0]),("North","South"))
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.ylim(0,700)
    plt.ylabel('Cumul %s mean in 2018'%"rainfall")
    ax1=plt.subplot(222)
    plt.title("Watershed : Adour")
    p1=plt.plot(cum_SAFRAN1NORD2017.T.mean(),color='blue')
    p2=plt.plot(cum_SAFRAN1SUD2017.T.mean(),color="red")
    plt.fill_between(cum_SAFRAN1NORD2017.index, b_NORD2017.mean(), _NORD2017.mean(), facecolor='blue', alpha=0.2)
    plt.fill_between(cum_SAFRAN1SUD2017.index,  b_SUD2017.mean(), _SUD2017.mean(), facecolor='red', alpha=0.2)
    plt.legend((p1[0],p2[0]),("North","South"))
    plt.xticks(size='large')
    plt.yticks(size='large')
    plt.ylim(0,700)
    plt.ylabel('Cumul %s mean in 2017'%"rainfall")
    plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/Culum_plui_2017_2018_Adour.png")


