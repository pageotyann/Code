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
    plt.errorbar(x,y1.interpolate().T.mean(),yerr=y1.interpolate().T.std())
    plt.ylabel("db ascVV_VH")
    plt.title("CODE_CULTURE_"+str(i))
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2 = plt.subplot(412)
    plt.errorbar(x,y2.interpolate().T.mean(),yerr=y2.interpolate().T.std())
    plt.ylabel("db ascVV")
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax3 = plt.subplot(413)
    plt.errorbar(x, y3.interpolate().T.mean(),yerr=y3.interpolate().T.std())
    plt.ylabel("db ascVH")
    plt.setp(ax3.get_xticklabels(), visible=False)    
    ax4 = plt.subplot(414)
    plt.bar(x, y4,width=1)
    plt.ylabel("Precipitation en mm")
    
def intersectlist(x,y):
    set(x).intersection(set(y))
    
if __name__ == "__main__":
# =============================================================================
# Optique
# =============================================================================
    # Lectuer des files
        
    d={}
    conn = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed4_learn.sqlite')
    conn1 = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R15_GAP30j/learningSamples/Samples_region_1_seed4_learn.sqlite')

    df=pd.read_sql_query("SELECT * FROM output", conn1)
    dfpar=df.groupby("originfid").mean()
    
    # Recuperation des names de cultures
    #names_crops=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/RUN/r9_crops_tcj_const_PSRI_ERR/final/nomenclature_V2_crops.txt",sep=":",names=["name","code"])
    
    #lister les labels dans le file sqlite 
    lab=dfpar.labcroirr.astype(int)
    lab=list(set(lab))
    
    #loop sur les label 
    
    for i in lab:
        print(i)
        globals()['cropslab%s' % i] = pd.DataFrame(dfpar[dfpar.labcroirr==i]).T
        globals()['NDVI30j%s' % i]=[]
        for index,row in globals()['cropslab%s' % i].iterrows():
            if "ndvi" in index:
                globals()['NDVI30j%s' % i].append (row)
                globals()['dfndvi30j%s' % i]=pd.DataFrame(globals()['NDVI30j%s' % i])
    
        plt.figure(figsize=(15,10))
        #y_pos=np.arange(df.shape[0])
        sns.set(style="darkgrid")
        sns.set_context('paper')
        #plt.plot(globals()['dfndvi%s' % i])
        plt.errorbar(globals()['dfndvi%s' % i].index,globals()['dfndvi%s' % i].T.mean(),yerr=globals()['dfndvi%s' % i].T.std())
        plt.xticks(rotation=90)
        plt.title("CODE_CULTURE"+"_"+str(i))
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/NDVI_2017/plot_NDWI_TEMPOREL_%s.png"%(i))
    
    
    
    
    conn = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed4_learn.sqlite')
#    conn = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R13_S1_S2/learningSamples/Samples_region_1_seed4_learn.sqlite')
    df=pd.read_sql_query("SELECT * FROM output", conn)
    dfpar=df.groupby("originfid").mean()
    
    # Recuperation des names de cultures
    #names_crops=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/RUN/r9_crops_tcj_const_PSRI_ERR/final/nomenclature_V2_crops.txt",sep=":",names=["name","code"])
    # =============================================================================
    # RADAR
    # =============================================================================
    #lister les labels dans le file sqlite 
    lab=dfpar.labcroirr.astype(int)
    lab=list(set(lab))
    
    #loop sur les label 
    
    for i in lab:
        print(i)
        globals()['cropslab%s' % i] = pd.DataFrame(dfpar[dfpar.labcroirr==i]).T
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
    
    
    #if i == names_crops.code:
    #    print (names_crops.code)
    #Maize irrigated:1
    #Maize no irrigated:11
    #Soybean irrigated:2
    #Soybean no irrigated:22
    #Sorghum no irrigated:33
    #Sunflower no irrigated:44
    #Peas no irrigated:55
    #Others:6
    #
    
    
    
    # =============================================================================
    # SPECTRE SM
    # =============================================================================
    timeSM=pd.DataFrame()
    for i in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SM_DT/"):
        print (i)
        date=i[3:11]
        STASMD = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SM_DT/'+i)
        dfSM=pd.read_sql_query("SELECT * FROM output", STASMD)
        dfpar=dfSM.groupby("originfid").mean()
        lab=dfpar.labcroirr.astype(int)
        globals()["meansm%s"%date]=dfpar.value_0
        globals()["meansm%s"%date].rename("SM_"+date,inplace=True)
        timeSM=timeSM.append(globals()["meansm%s"%date])
        
    timeSM=timeSM.sort_index(ascending=True)
    timesm=timeSM.T/5
    timesm["label"]=lab
    label=list(set(lab))
    for j in label:
        print(j)
        globals()['SMcropslab%s' % j] = pd.DataFrame(timesm[timesm.label==j]).T
        plt.figure(figsize=(15,10))
        plt.errorbar(globals()['SMcropslab%s' % j].index,globals()['SMcropslab%s' % j].T.mean(),yerr=globals()['SMcropslab%s' % j].T.std())
        #pltemp(globals()['SMcropslab%s' % j].iloc[:-1,:10])
        plt.title("CODE_CULTURE"+"_"+str(j))
        plt.ylabel("soil moisture en mv")
        plt.xticks(rotation=90)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_SM/PLOT_TEMPO_SM_%s_mean.png"%(j))
     
        
    
    # =============================================================================
    # Gestion des datas SAFRAN et digramme ombrothermqiue
    # =============================================================================
    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/preliq2017.csv")
    
    LAMBX=df.LAMBX*100
    LAMBY=df.LAMBY*100
    df["lambX"]=LAMBX
    df['lambY']=LAMBY
    df.to_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/preliq2017_v2.csv")
    
    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/SAFRAN_TCJ.csv")
    df1=df.drop([0])
    preliq=df1[["DATE","PRELIQ_Q","X","Y"]]
    
    preliq2=preliq.sort_values(by="DATE")
    meandate=preliq2.groupby("DATE").mean()
    
    # =============================================================================
    # Groupe en fonctiondes date S1
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
     ## 4 fois plus rapide        
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
    # SAFRAN_SM
    # =============================================================================
    date_SM=[]
    for i in timeSM.index:
        h=i[3:]
        date_SM.append(h)
    dateSM=list(map(int,date_SM))
    
    resultSM=set(list(date_safran)).intersection(set(dateSM))
    
    SAFRAN_SM=meandate.loc[dateSM]
    SAFRAN_SM.index=pd.to_datetime(SAFRAN_SM.index,format='%Y%m%d')
    label=list(set(lab))
    for j in label:
        pltemplui(SAFRAN_SM.index,SAFRAN_SM.PRELIQ_Q,globals()['SMcropslab%s' % j].iloc[:-1,:].T.mean())
        plt.title("CODE_CULTURE"+"_"+str(j))
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_SM/PLOT_SM_PLUVIO_%s.png"%(j))
    
    
    # =============================================================================
    # SRTM_STAT
    # =============================================================================
    STASRTM = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/SRTM_TCJ_SLP_SampleExtraction.sqlite')
    df=pd.read_sql_query("SELECT * FROM output", STASRTM)
    
    dfpar=df.groupby("originfid").mean()
    dfpar=df.groupby("originfid").var()
    
    dflab=dfpar.groupby("labcroirr").mean()
    
    plt.figure(figsize=(15,15))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    g=sns.violinplot(x='labcroirr', y='value_0', data=dfpar)
    plt.ylabel("mean_elevation")
    #g.set_xticklabels(,rotation=90)
    plt.xlabel("label")
    
    
    STApente = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SRTM_TCJ/S2__TEST_AUX_REFDE2_T31TCJ_0001_SLP_R1.TIF_SampleExtraction.sqlite')
    dfslp=pd.read_sql_query("SELECT * FROM output", STApente)
    
    dfpar=dfslp.groupby("originfid").mean()
    
    plt.figure(figsize=(15,15))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    g=sns.violinplot(x='labcroirr', y='value_0', data=dfslp)
    plt.ylabel("mean_pente")
    #g.set_xticklabels(,rotation=90)
    plt.xlabel("label")
    
    
    STAexpo = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_SRTM_TCJ/RECLASS_EXPO_MASK_T31TCJ.tif_SampleExtraction.sqlite')
    dfexpo=pd.read_sql_query("SELECT * FROM output", STAexpo)
    
    dfpar=dfexpo.groupby("originfid").mean()
    
    plt.figure(figsize=(15,15))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    g=sns.box(x='labcroirr', y='value_0', data=dfexpo)
    plt.ylabel("mean_pente")
    #g.set_xticklabels(,rotation=90)
    plt.xlabel("label")
    
    #loop sur file tile SRTM et pente et EXPO 
    
    d={}
    d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/"
    d["ALL"]=d["data_file"]+"STAT_SRTM_DT_ALL/"
    for i in os.listdir(d["ALL"]):
        tile=i[19:26]
        var=i[32:35]
        print (tile)
        print (var)
        dfsrtm = sqlite3.connect(d["ALL"]+i)
        df=pd.read_sql_query("SELECT * FROM output", dfsrtm)
        dfpar=df.groupby("originfid").mean()
        plt.figure(figsize=(15,15))
        sns.set(style="darkgrid")
        sns.set_context('paper')
        g=sns.violinplot(x='labcroirr', y='value_0', data=df)
        plt.ylabel(var+tile)
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLT_SRTM_DT/%s_%s.png"%(var,tile))
    
    # =============================================================================
    # CODE ANCIERN 
    # =============================================================================
            
    #polarisation=["ascVV",'desVV','ascVH','desVH',"desVV_VH","ascVV_VH"]       
    #for p in polarisation:
    #    print (p)     
    #    for i in lab:
    #        globals()["dbdf%s%s" %(p,i)]["date"]=globals()["images_S1_%s" %(p[0:3])]
    #        others=pd.DataFrame()
    #        for j in list(globals()["dbdf%s%s" %(p,i)].columns): 
    #            if 'asc' in p:
    #                add=pd.DataFrame({"date":list(miss1), j:list(val1)})
    #                others=others.append(add)
    #            else:
    #                add=pd.DataFrame({"date":list(miss2), j:list(val2)})
    #                others=others.append(add)
    #        globals()["db%s"% i]=pd.concat([globals()["dbdf%s%s" %(p,i)],others])
    #        #globals()["dbdf%s"% i]=globals()["db%s"% i].sort_values(by="date")
    #        globals()["dbdf%sNA%s"%(p,i)] =globals()["db%s"% i].groupby("date").mean()
        
    
    # =============================================================================
    # Avec des errort bar
    # =============================================================================
    for p in polarisation:
        for i in lab:
            if p in "asc":
                plt.figure(figsize=(15,15))
                ax1 = plt.subplot(411)
                plt.errorbar(meandate.index[:-4],globals()["dbdf%sNA%s"%("ascVV_VH",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("ascVV_VH",i)].interpolate().T.std())
                plt.ylabel("db ascVV_VH")
                plt.title("CODE_CULTURE_"+str(i))
                plt.setp(ax1.get_xticklabels(), visible=False)
                
                # share x only
                ax2 = plt.subplot(412)
                plt.errorbar(meandate.index[:-4],globals()["dbdf%sNA%s"%("ascVV",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("ascVV",i)].interpolate().T.std())
                plt.ylabel("db ascVV")
                # make these tick labels invisible
                plt.setp(ax2.get_xticklabels(), visible=False)
                
                # share x and y
                ax3 = plt.subplot(413)
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
                plt.errorbar(meandate.index[5:-9],globals()["dbdf%sNA%s"%("desVV_VH",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("desVV_VH",i)].interpolate().T.std())
                plt.ylabel("db desVV_VH")
                plt.title("CODE_CULTURE_"+str(i))
                plt.setp(ax1.get_xticklabels(), visible=False)
                
                # share x only
                ax2 = plt.subplot(412)
                plt.errorbar(meandate.index[5:-9],globals()["dbdf%sNA%s"%("desVV",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("desVV",i)].interpolate().T.std())
                plt.ylabel("db desVV")
                # make these tick labels invisible
                plt.setp(ax2.get_xticklabels(), visible=False)
                
                # share x and y
                ax3 = plt.subplot(413)
                plt.errorbar(meandate.index[5:-9], globals()["dbdf%sNA%s"%("desVH",i)].interpolate().T.mean(),yerr=globals()["dbdf%sNA%s"%("desVH",i)].interpolate().T.std())
                plt.ylabel("db desVH")
                plt.setp(ax3.get_xticklabels(), visible=False)
                
                ax4 = plt.subplot(414)
                plt.bar(meandate.index[5:-9], meandate.PRELIQ_Q[5:-9],width=1)
                plt.ylabel("Precipitation en mm")
                plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_TEMPOREL/SAR_2017/plot_SAR_%s_%s_SAFRAN_mean.png"%("orbitedes",i))

    # =============================================================================
    # PLOT_SM_PLUVIO
    # =============================================================================
    
    dateSM=pd.to_datetime(dateSM,format="%Y%m%d")
    meandate.index=pd.to_datetime(meandate.index,format="%Y%m%d")
    timeSM=timeSM.sort_index()
    label=list(set(lab))
    for j in label[:-1]:
        print(j)
        globals()['SMcropslab%s' % j] = pd.DataFrame(timesm[timesm.label==j]).T
        plt.figure(figsize=(15,10))
        ax1 = plt.subplot(411)
        plt.errorbar(meandate.loc[dateSM].index,globals()['SMcropslab%s' % j][:-1].T.mean(),yerr=globals()['SMcropslab%s' % j][:-1].T.std())
        #pltemp(globals()['SMcropslab%s' % j].iloc[:-1,:10])
        plt.title("CODE_CULTURE"+"_"+str(j))
        plt.ylabel("soil moisture en mv vol %")
        plt.setp(ax1.get_xticklabels(), visible=False)
        # share x only
        ax2 = plt.subplot(412)
        plt.bar(meandate.loc[dateSM].index,meandate.loc[dateSM].PRELIQ_Q,width=1)
        plt.ylabel("Précipitation en mm")
        plt.savefig("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_SM/plot_SM_%s_SAFRAN_mean.png"%(j))

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
            
    
    images_S1_asc=list(map(int,date))
    images_S1_asc=list(set(images_S1_asc))
    images_S1_asc =images_S1_asc.sort()
    conn = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/SampleExtractionSAR_vvASC.tif.sqlite')
    df=pd.read_sql_query("SELECT * FROM output", conn)
    dfpar=df.groupby("originfid").mean()
    dfpar=dfpar.drop([458])
    
    lab=dfpar.labcroirr.astype(int)
    lab=list(set(lab))
    
    #loop sur les label 
    
    for i in lab:
        print(i)
        globals()['cropslab%s' % i] = pd.DataFrame(dfpar[dfpar.labcroirr==i]).T
        globals()['VVasc%s' % i]=[]
        for index,row in globals()['cropslab%s' % i].iterrows():
            globals()['VVasc%s' % i].append (row)
            globals()['dfVV%s' % i]=pd.DataFrame(globals()['VVasc%s' % i])
            globals()["dbdfVV%s" % i]=10*np.log10(globals()['dfVV%s' % i])
            globals()["dbdfVV%s" % i]=globals()["dbdfVV%s" % i][8:]
        globals()["dbdfVV%s" % i]["date"]=images_S1_asc
        globals()["dbdfVV%s" %i].date=pd.to_datetime(globals()["dbdfVV%s" % i].date,format="%Y%m%d")
        globals()["dbdfVV%s"%(i)]=globals()["dbdfVV%s"%(i)].set_index("date")
        for j in list(globals()["dbdfVV%s" %(i)].columns): 
            globals()["dbdfVVNA%s"%(i)]=globals()["dbdfVV%s" %(i)].resample('D').asfreq()

        plt.figure(figsize=(15,15))
        plt.errorbar(meandate.index[:-4],globals()["dbdfVVNA%s"%(i)].interpolate().T.mean(),yerr=globals()["dbdfVVNA%s"%(i)].interpolate().T.std())
        plt.ylabel("db ascVV_VH")
        plt.title("CODE_CULTURE_"+str(i))
        plt.setp(ax1.get_xticklabels(), visible=False)
    
