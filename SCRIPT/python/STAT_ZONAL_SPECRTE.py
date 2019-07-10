#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:38:21 2019

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
from scipy import *
from pylab import *

def pltemp(x):
    plt.figure(figsize=(15,10))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    plt.plot(x,linestyle="-")
    plt.xticks(rotation=90)
    
def pltemplui(y,x1,x2):
    plt.figure(figsize=(20,20))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    plt.bar(y,x1,color="blue",width=1)
    ax2 = plt.twinx()
    ax2.plot(y,x2,linewidth=2,color='r')
    
def pltSAR4(x,y1,y2,y3,y4):
    plt.figure(figsize=(15,15))
    ax1 = plt.subplot(411)
    plt.plot(y1.T.mean(),marker="o")
    plt.errorbar(x,y1.interpolate().T.mean(),yerr=y1.interpolate().T.std())
    plt.ylabel("db ascVV_VH")
    plt.title("CODE_CULTURE_"+str(i))
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2 = plt.subplot(412)
    plt.plot(y2.T.mean(),marker="o")
    plt.errorbar(x,y2.interpolate().T.mean(),yerr=y2.interpolate().T.std())
    plt.ylabel("db ascVV")
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax3 = plt.subplot(413)
    plt.plot(y3.T.mean(),marker="o")
    plt.errorbar(x, y3.interpolate().T.mean(),yerr=y3.interpolate().T.std())
    plt.ylabel("db ascVH")
    plt.setp(ax3.get_xticklabels(), visible=False)    
    ax4 = plt.subplot(414)
    plt.bar(x, y4,width=1)
    plt.ylabel("Precipitation en mm")
    
def intersectlist(x,y):
    a=set(x).intersection(set(y))
    return a
    
def SAR_process_db(list_lab,data,variable_resarch): # Attention variable_resarch
     for i in list_lab:
        print(i)
        globals()['cropslab%s' % i] = pd.DataFrame(data[data.labcroirr==i]).T
        globals()['%s%s' % (variable_resarch,i)]=[]
        for index,row in globals()['cropslab%s' % i].iterrows():
            if variable_resarch in index:
                globals()['%s%s' % (variable_resarch,i)].append (row)
                globals()['df%s%s' %(variable_resarch,i)]=pd.DataFrame(globals()['%s%s' % (variable_resarch,i)])
                globals()["df%s%s"% (variable_resarch,i)].replace(to_replace =0 , value= pd.NaT,inplace=True)
                globals()["dbdf%s%s" %(variable_resarch ,i)]=10*np.log10(globals()['df%s%s' % (variable_resarch,i)])
     return globals()['df%s%s' %(variable_resarch,i)]      


def sqlite_df(path,x):
    sql=sqlite3.connect(path)
    df=pd.read_sql_query("SELECT * FROM output", sql)
    globals()["%s"%x]=df.groupby("originfid").mean()
    return globals()["%s"%x]
    

def Optique_Process(list_lab,data,variable_resarch):
    for i in list_lab:
        print(i)
        globals()['cropslab%s' % i] = pd.DataFrame(data[data.labcroirr==i]).T
        globals()['%s%s' %(variable_resarch,i)]=[]
        for index,row in globals()['cropslab%s' % i].iterrows():
            if variable_resarch in index:
                globals()['%s%s' % (variable_resarch,i)].append (row)
                globals()['df%s%s' %(variable_resarch,i)]=pd.DataFrame(globals()['%s%s' %(variable_resarch,i)])
    return globals()['df%s%s' %(variable_resarch,i)]

if __name__ == "__main__":
    # =============================================================================
    # Optique
    # =============================================================================
    # Lectuer des files
        
#   
    sqlite_df('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed4_learn.sqlite','dfr14')
    
    #lister les labels dans le file sqlite 
    lab=dfr14.labcroirr.astype(int)
    lab=list(set(lab))
    
    #loop sur les label 
    
    for i in lab:
        print(i)
        globals()['cropslab%s' % i] = pd.DataFrame(dfr14[dfr14.labcroirr==i]).T
        globals()['NDVI%s' % i]=[]
        for index,row in globals()['cropslab%s' % i].iterrows():
            if "ndvi" in index:
                globals()['NDVI%s' % i].append (row)
                globals()['dfndvi%s' % i]=pd.DataFrame(globals()['NDVI%s' % i])
        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["dfndvi%s"%i].shape[1]-1,loc= globals()["dfndvi%s"%i].T.mean(),scale=stats.sem(globals()["dfndvi%s"%i].T.mean()))
        plt.figure(figsize=(15,10))
        #y_pos=np.arange(df.shape[0])
        sns.set(style="darkgrid")
        sns.set_context('paper')
        #plt.plot(globals()['dfndvi%s' % i])
        plt.plot(globals()['dfndvi%s' % i].index,globals()['dfndvi%s' % i].T.mean())
        plt.fill_between(globals()['dfndvi%s' % i].index, globals()["b_sup%s"% (i)], globals()["_%s"% (i)], facecolor='blue', alpha=0.2)
#        plt.errorbar(globals()['dfndvi%s' % i].index,globals()['dfndvi%s' % i].T.mean(),yerr=globals()['dfndvi%s' % i].T.std())
        plt.xticks(rotation=90)
        plt.title("CODE_CULTURE"+"_"+str(i))
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/NDVI_2017/plot_NDWI_TEMPOREL_%s.png"%(i))

    # =============================================================================
    # RADAR
    # =============================================================================
    for i in lab:
        print(i)
        globals()['cropslab%s' % i] = pd.DataFrame(dfr14[dfr14.labcroirr==i]).T
        globals()['VHdes%s' % i]=[]
        globals()['VVdes%s' % i]=[]
        globals()['VHasc%s' % i]=[]
        globals()['VVasc%s' % i]=[]
        globals()['VV_VHasc%s' % i]=[]
        globals()['VV_VHdes%s' % i]=[]
        for index,row in globals()['cropslab%s' % i].iterrows():
            if "des_vh" in index:
                globals()['VHdes%s' % i].append (row)
                globals()['dfVH%s' % i]=pd.DataFrame(globals()['VHdes%s' % i])
                globals()["dbdfdesVH%s" % i]=10*np.log10(globals()['dfVH%s' % i])
                #globals()["dbdfdesVH%s" % i].to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/DATAFRAME/dbdfdesVH%s.csv"%(i))
            if "asc_vh" in index:
                globals()['VHasc%s' % i].append (row)
                globals()['dfVHasc%s' % i]=pd.DataFrame(globals()['VHasc%s' % i])
                globals()["dbdfascVH%s" % i]=10*np.log10(globals()['dfVHasc%s' % i])
                #globals()["dbdfascVH%s" % i].to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/DATAFRAME/dbdfascVH%s.csv"%(i))
            if "asc_vv" in index:
                globals()['VVasc%s' % i].append (row)
                globals()['dfVVasc%s' % i]=pd.DataFrame(globals()['VVasc%s' % i])
                globals()["dbdfascVV%s" % i]=10*np.log10(globals()['dfVVasc%s' % i])
                #globals()["dbdfascVV%s" % i].to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/DATAFRAME/dbdfascVV%s.csv"%(i)) 
            if "des_vv" in index:
                globals()['VVdes%s' % i].append (row)
                globals()['dfVV%s' % i]=pd.DataFrame(globals()['VVdes%s' % i])
                globals()["dbdfdesVV%s" % i]=10*np.log10(globals()['dfVV%s' % i])
                #globals()["dbdfdesVV%s" % i].to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/DATAFRAME/dbdfdesVV%s.csv"%(i))  
            if "asc_userfeature1" in index:
                globals()['VV_VHasc%s' % i].append (row)
                globals()['dfVV_VH%s' % i]=pd.DataFrame(globals()['VV_VHasc%s' % i])
                globals()["dbdfascVV_VH%s" % i]=10*np.log10(globals()['dfVV_VH%s' % i])
                #globals()["dbdfascVV_VH%s" % i].to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/DATAFRAME/dbdfascVV_VH%s.csv"%(i))  
            if "des_userfeature1" in index:
                globals()['VV_VHdes%s' % i].append (row)
                globals()['dfVV_VHdes%s' % i]=pd.DataFrame(globals()['VV_VHdes%s' % i])
                globals()["dbdfdesVV_VH%s" % i]=10*np.log10(globals()['dfVV_VHdes%s' % i])
                #globals()["dbdfdesVV_VH%s" % i].to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/DATAFRAME/dbdfdesVV_VH%s.csv"%(i))
    
    polarisation=["ascVV",'desVV','ascVH','desVH',"desVV_VH","ascVV_VH"]       
    for p in polarisation:
        for i in lab:
            plt.figure(figsize=(15,10))
            sns.set(style="darkgrid")
            sns.set_context('paper')
            #plt.plot(globals()['dbdfdesVV_VH%s' % i].iloc[:,0:-1])
            plt.errorbar(globals()["dbdf%s%s" % (p,i)].index,globals()["dbdf%s%s" %(p,i)].T.mean(),yerr=globals()["dbdf%s%s" %(p,i)].T.std())
            plt.xticks(rotation=90)
            plt.title("CODE_CULTURE"+"_"+str(i))
            plt.ylabel("db %s"%(p))
            plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/SAR_2017/plot_%s_TEMPOREL_%s_mean.png"%(p,i))
    
    
    
    
  
     
        
    
    # =============================================================================
    # Gestion des datas SAFRAN 
    # =============================================================================
#    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/SIM2_2018_201901.csv",sep=";")
#    
#    LAMBX=df.LAMBX*100
#    LAMBY=df.LAMBY*100
#    df["lambX"]=LAMBX
#    df['lambY']=LAMBY
#    df.to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/SAFRAN2018_L2.csv")
    
    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/SAFRAN_TCJ.csv")
    df1=df.drop([0])
    preliq=df1[["DATE","PRELIQ_Q","X","Y"]]
    
    preliq2=preliq.sort_values(by="DATE")
    meandate=preliq2.groupby("DATE").mean()
    
    # =============================================================================
    # Groupe en fonction des date S1
    # =============================================================================
    
    images=[]
    with open("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/tmp/S1_vh_DES_dates_interpolation.txt", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            images.append(row[0])
    images2=[]
    with open("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/tmp/S1_vv_ASC_dates_interpolation.txt", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            images2.append(row[0])
    
    images_S1_asc=list(map(int,images2))
    images_S1_des=list(map(int,images))
    # =============================================================================
    # Contrution df annuel avec NAT
    # =============================================================================
    date_safran=list(meandate.index)
    meandate.index=pd.to_datetime(meandate.index,format='%Y%m%d')
    
    for i in date_safran:
        if i not in images_S1_asc :
            result1=set(list(date_safran)).union(set(images_S1_asc)) - set(list(date_safran)).intersection(set(images_S1_asc))
            miss1=np.array(list(result1))
            val1=np.repeat(pd.NaT,miss1.shape[0])
        else:
            result2=set(list(date_safran)).union(set(images_S1_des)) - set(list(date_safran)).intersection(set(images_S1_des))
            miss2=np.array(list(result2))
            val2=np.repeat(pd.NaT,miss2.shape[0])
     
    polarisation=["ascVV",'desVV','ascVH','desVH',"desVV_VH","ascVV_VH"]       
    for p in polarisation:
        print (p)     
        for i in lab:
            globals()["dbdf%s%s" %(p,i)]["date"]=globals()["images_S1_%s" %(p[0:3])]
            globals()["dbdf%s%s" %(p,i)].date=pd.to_datetime(globals()["dbdf%s%s" %(p,i)].date,format="%Y%m%d")
            globals()["dbdf%s%s"%(p,i)]=globals()["dbdf%s%s"%(p,i)].set_index("date")
            for j in list(globals()["dbdf%s%s" %(p,i)].columns): 
                globals()["dbdf%sNA%s"%(p,i)]=globals()["dbdf%s%s" %(p,i)].resample('D').asfreq()
                globals()["dbdf%sNA%s"%(p,i)].to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/dbdf%s%s.csv"%(p,i))
    
    # =============================================================================
    # Plot db Radar et SAfran pluvio
    # =============================================================================
    for p in polarisation:
        for i in lab:  
            pltemplui(meandate.index[0:-4],meandate.PRELIQ_Q[:-4],globals()["dbdf%sNA%s"%("ascVV_VH",i)].interpolate().T.mean())
            plt.title("CODE_CULTURE"+"_"+str(i))
            plt.ylabel("db %s"%("ascVV_VH"))
            plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/SAR_2017/plot_SAR_%s_%s_SAFRAN_mean.png"%("ascVV_VH",i))
    
    # =============================================================================
    # Avec des errort bar
    # =============================================================================
    for p in polarisation:
        for i in lab:
            if "asc" in p:
                plt.figure(figsize=(15,15))
                ax1 = plt.subplot(411)
                plt.plot(globals()["dbdfascVV_VH%s"%(i)].T.mean(),marker="o")
                plt.errorbar(meandate.index[:-4],globals()["dbdf%sNA%s"%("ascVV_VH",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("ascVV_VH",i)].interpolate().T.std())
                plt.ylabel("db ascVV_VH")
                plt.title("CODE_CULTURE_"+str(i))
                plt.setp(ax1.get_xticklabels(), visible=False)
                
                # share x only
                ax2 = plt.subplot(412)
                plt.plot(globals()["dbdfascVV%s"%(i)].T.mean(),marker="o")
                plt.errorbar(meandate.index[:-4],globals()["dbdf%sNA%s"%("ascVV",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("ascVV",i)].interpolate().T.std())
                plt.ylabel("db ascVV")
                # make these tick labels invisible
                plt.setp(ax2.get_xticklabels(), visible=False)
                
                # share x and y
                ax3 = plt.subplot(413)
                plt.plot(globals()["dbdfascVH%s"%(i)].T.mean(),marker="o")
                plt.errorbar(meandate.index[:-4], globals()["dbdf%sNA%s"%("ascVH",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("ascVH",i)].interpolate().T.std())
                plt.ylabel("db ascVH")
                plt.setp(ax3.get_xticklabels(), visible=False)
                
                ax5 = plt.subplot(414)
                plt.bar(meandate.index[:-4], meandate.PRELIQ_Q[:-4],width=1)
                plt.ylabel("Precipitation en mm")
                plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/SAR_2017/plot_SAR_%s_%s_SAFRAN_mean.png"%("orbiteasc",i))
            else:
                plt.figure(figsize=(15,15))
                ax1 = plt.subplot(411)
                plt.plot(globals()["dbdfdesVV_VH%s"%(i)].T.mean(),marker="o")
                plt.errorbar(meandate.index[5:-9],globals()["dbdf%sNA%s"%("desVV_VH",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("desVV_VH",i)].interpolate().T.std())
                plt.ylabel("db desVV_VH")
                plt.title("CODE_CULTURE_"+str(i))
                plt.setp(ax1.get_xticklabels(), visible=False)
                
                # share x only
                ax2 = plt.subplot(412)
                plt.plot(globals()["dbdfdesVV%s"%(i)].T.mean(),marker="o")
                plt.errorbar(meandate.index[5:-9],globals()["dbdf%sNA%s"%("desVV",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("desVV",i)].interpolate().T.std())
                plt.ylabel("db desVV")
                # make these tick labels invisible
                plt.setp(ax2.get_xticklabels(), visible=False)
                
                # share x and y
                ax3 = plt.subplot(413)
                plt.plot(globals()["dbdfdesVH%s"%(i)].T.mean(),marker="o")
                plt.errorbar(meandate.index[5:-9], globals()["dbdf%sNA%s"%("desVH",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("desVH",i)].interpolate().T.std())
                plt.ylabel("db desVH")
                plt.setp(ax3.get_xticklabels(), visible=False)
                
                ax4 = plt.subplot(414)
                plt.bar(meandate.index[5:-9], meandate.PRELIQ_Q[5:-9],width=1)
                plt.ylabel("Precipitation en mm")
                plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/SAR_2017/plot_SAR_%s_%s_SAFRAN_mean.png"%("orbitedes",i))
    


    # =============================================================================
    #   SAR Orbite 132 ASC_ vv
    # =============================================================================
    images=[]
    with open("/datalocal/vboxshare/THESE/CLASSIFICATION/IMG_SAT/DATA_S1/list_vv_img.txt", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            images.append(row[0])
    date=[]
    for i in images:
        date.append(i[17:25])
            
    
    images_S1_asc132 = list(map(int,date))
    images_S1_asc132 = list(set(images_S1_asc132))
    images_S1_asc132 = sorted(images_S1_asc132)
    
    sqlite_df('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/SampleExtractionSAR_vvASC.tif.sqlite','dfVVASC')
    dfVVASC=dfVVASC.drop([458])
    
    lab=dfVVASC.labcroirr.astype(int)
    lab=list(set(lab))
    
    #loop sur les label 
    SAR_process_db(lab,dfVVASC,'value')
    for i in lab:
        globals()["dbdfvalue%s" % i]["date"]=images_S1_asc132
        globals()["dbdfvalue%s" %i].date=pd.to_datetime(globals()["dbdfvalue%s" % i].date,format="%Y%m%d")
        globals()["dbdfVV%s"%(i)]=globals()["dbdfvalue%s"%(i)].set_index("date")
        for j in list(globals()["dbdfVV%s" %(i)].columns): 
            globals()["dbdfVVNA%s"%(i)]=globals()["dbdfVV%s" %(i)].resample('D').asfreq()

        plt.figure(figsize=(15,15)) 
        ax1=plt.subplot(211)
        plt.plot(globals()["dbdfVVNA%s"%(i)].T.mean(),marker="o")
        plt.errorbar(meandate.index[156:-4],globals()["dbdfVVNA%s"%(i)].interpolate().T.mean(),yerr=globals()["dbdfVVNA%s"%(i)].interpolate().T.std(),linewidth=1,linestyle='-')
        plt.ylabel("db ascVV_VH")
        plt.title("CODE_CULTURE_"+str(i))
        plt.setp(ax1.get_xticklabels(), visible=False)
        ax5 = plt.subplot(212)
        plt.bar(meandate.index[156:-4], meandate.PRELIQ_Q[156:-4],width=1)
        plt.ylabel("Precipitation en mm")


    # =============================================================================
    # Profil TST 
    # =============================================================================
    a=set(meandate.index).intersection(set(TimeTSTNIRR.index))
    
    timeTST=pd.DataFrame()
    Years=[]
    for i in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_TST/"):
        print (i)
        tile=i[35:41]
        print (tile)
        date=i[42:50]
        print (date)
        sqlite_df("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_TST/" +i,"dfTST")
        lab=dfTST.labcroirr.astype(int)
        globals()["meanTST%s"%(date)]=round(dfTST.value_0/100-273.15,2)
        globals()["meanTST%s"%date].rename("TST_"+date,inplace=True)
        timeTST=timeTST.append(globals()["meanTST%s"%date])
        Years.append(date)
    timeTST.sort_index(inplace=True)
    timeTST[timeTST<= -1]=pd.NaT
    timeTST["date"]=sorted(Years)
    timeTST.date=pd.to_datetime(timeTST.date,format="%Y%m%d")
    TimeTST=timeTST.groupby(timeTST.date).mean()
    plt.figure(figsize=(10,10))
    plt.subplot(211)
    plt.plot(meandate.loc[a].index,TimeTST.loc[a],marker='o')
    plt.subplot(212)
    plt.bar(meandate.loc[a].index,meandate.loc[a].PRELIQ_Q,width=5)

    timeTSTNIRR=pd.DataFrame()
    Years=[]
    for i in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_TST/STAT_NIRR/"):
        print (i)
        tile=i[35:41]
        print (tile)
        date=i[42:50]
        print (date)
        sqlite_df("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_TST/STAT_NIRR/" +i,"dfTST")
        lab=dfTST.labcroirr.astype(int)
        globals()["meanTST%s"%(date)]=round(dfTST.value_0/100-273.15,2)
        globals()["meanTST%s"%date].rename("TST_"+date,inplace=True)
        timeTSTNIRR=timeTSTNIRR.append(globals()["meanTST%s"%date])
        Years.append(date)
    timeTSTNIRR.sort_index(inplace=True)
    timeTSTNIRR[timeTSTNIRR<= -1]=pd.NaT
    timeTSTNIRR["date"]=sorted(Years)
    timeTSTNIRR.date=pd.to_datetime(timeTSTNIRR.date,format="%Y%m%d")
    TimeTSTNIRR=timeTSTNIRR.groupby(timeTSTNIRR.date).mean()
    plt.figure(figsize=(10,10))
    plt.subplot(211)
    plt.plot(meandate.loc[a].index,TimeTSTNIRR.loc[a],marker='o')
    plt.subplot(212)
    plt.bar(meandate.loc[a].index,meandate.loc[a].PRELIQ_Q,width=5)

#    # =============================================================================
#    # SRTM_STAT
#    # =============================================================================
#    STASRTM = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/SRTM_TCJ_SLP_SampleExtraction.sqlite')
#    df=pd.read_sql_query("SELECT * FROM output", STASRTM)
#    
#    dfpar=df.groupby("originfid").mean()
#    dfpar=df.groupby("originfid").var()
#    
#    dflab=dfpar.groupby("labcroirr").mean()
#    
#    plt.figure(figsize=(15,15))
#    sns.set(style="darkgrid")
#    sns.set_context('paper')
#    g=sns.violinplot(x='labcroirr', y='value_0', data=dfpar)
#    plt.ylabel("mean_elevation")
#    #g.set_xticklabels(,rotation=90)
#    plt.xlabel("label")
#    
#    
#    STApente = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SRTM_TCJ/S2__TEST_AUX_REFDE2_T31TCJ_0001_SLP_R1.TIF_SampleExtraction.sqlite')
#    dfslp=pd.read_sql_query("SELECT * FROM output", STApente)
#    
#    dfpar=dfslp.groupby("originfid").mean()
#    
#    plt.figure(figsize=(15,15))
#    sns.set(style="darkgrid")
#    sns.set_context('paper')
#    g=sns.violinplot(x='labcroirr', y='value_0', data=dfslp)
#    plt.ylabel("mean_pente")
#    #g.set_xticklabels(,rotation=90)
#    plt.xlabel("label")
#    
#    
#    STAexpo = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SRTM_TCJ/RECLASS_EXPO_MASK_T31TCJ.tif_SampleExtraction.sqlite')
#    dfexpo=pd.read_sql_query("SELECT * FROM output", STAexpo)
#    
#    dfpar=dfexpo.groupby("originfid").mean()
#    
#    plt.figure(figsize=(15,15))
#    sns.set(style="darkgrid")
#    sns.set_context('paper')
#    g=sns.box(x='labcroirr', y='value_0', data=dfexpo)
#    plt.ylabel("mean_pente")
#    #g.set_xticklabels(,rotation=90)
#    plt.xlabel("label")
#    
#    #loop sur file tile SRTM et pente et EXPO 
#    
#    d={}
#    d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/"
#    d["ALL"]=d["data_file"]+"STAT_SRTM_DT_ALL/"
#    for i in os.listdir(d["ALL"]):
#        tile=i[19:26]
#        var=i[32:35]
#        print (tile)
#        print (var)
#        dfsrtm = sqlite3.connect(d["ALL"]+i)
#        df=pd.read_sql_query("SELECT * FROM output", dfsrtm)
#        dfpar=df.groupby("originfid").mean()
#        plt.figure(figsize=(15,15))
#        sns.set(style="darkgrid")
#        sns.set_context('paper')
#        g=sns.violinplot(x='labcroirr', y='value_0', data=df)
#        plt.ylabel(var+tile)
#        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLT_SRTM_DT/%s_%s.png"%(var,tile))