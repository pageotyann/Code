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
from STAT_ZONAL_SPECRTE import *
from scipy import stats


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
    plt.setp(ax5.get_xticklabels(),visible=False)
    plt.legend((p1[0],p2[0]),("Irrigué","Non Irrigué"))
    ax6 = plt.subplot(616)
    plt.bar(x3,y6,color='blue',width=1)
    plt.ylabel("pluviométrie en mm")
    plt.setp(ax6.get_xticklabels(),rotation=90)
    
def pltmutlimode(x,x2,x3,x4,y1,y1bis,y2,y2bis,y3,y3bis,y3tris,y3quad,y4,y4bis,y4tris,y4quad,y5,y5bis,x6,y6):
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
    p3=plt.plot(x2,y3,color='blue')
    plt.plot(x2, y3bis,color="red",linestyle='-')
    p4=plt.plot(x3,y3tris,color='blue',linestyle=':')
    plt.plot(x3,y3quad,color='red',linestyle=':')
    plt.legend((p3[0],p4[0]),("asc","des"))
    plt.ylabel("VV")
    plt.setp(ax3.get_xticklabels(), visible=False)    
    ax4 = plt.subplot(614)
    plt.plot(x2,y4,color='blue')
    plt.plot(x2,y4bis,color='red',linestyle='-')
    plt.plot(x3,y4tris,color='blue',linestyle=':')
    plt.plot(x3,y4quad,color='red',linestyle=':')
    plt.legend((p3[0],p4[0]),("asc","des"))
    plt.ylabel("VH")
    plt.setp(ax4.get_xticklabels(), visible=False)
    ax5 = plt.subplot(615)
    plt.plot(x4,y5,color='blue')
    plt.plot(x4, y5bis,color='red',linestyle='--')
    plt.ylabel("VH/VV")
    plt.setp(ax5.get_xticklabels(),visible=False)
    plt.legend((p1[0],p2[0]),("Irrigué","Non Irrigué"))
    ax6 = plt.subplot(616)
    plt.bar(x6,y6,color='blue',width=1)
    plt.ylabel("pluviométrie en mm")
    plt.setp(ax6.get_xticklabels(),rotation=90)
    
def plotconfi(x,x2,x3,y1,y1bis,y3,y3bis,y3tris,y3quad,y4,y4bis,y4tris,y4quad,yr,yrbis,yr1,yrbis1,x6,y6,confsup,confinf):
    plt.figure(figsize=(20,20))
    sns.set(style="darkgrid")
    sns.set_context('paper')
    ax1 = plt.subplot(811)
    p1=plt.plot(x,y1.T.mean(),color='blue')
    p2=plt.plot(x,y1bis.T.mean(),color='red',linestyle='--')
    plt.fill_between(x, confsup[0], confinf[0], facecolor='blue', alpha=0.2)
    plt.fill_between(x, confsup[1], confinf[1], facecolor='red', alpha=0.2)
    plt.ylabel("NDVI")
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2 = plt.subplot(812)
    plt.plot(x2, y3.T.mean(), color='blue',linestyle=":")
    plt.fill_between(x2, confsup[2], confinf[2], facecolor='blue', alpha=0.2)
    plt.plot(x2, y3bis.T.mean(), color='red',linestyle=":")
    plt.fill_between(x2, confsup[3], confinf[3], facecolor='red', alpha=0.2)
    plt.ylabel("VV asc")
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax3 = plt.subplot(813)
    plt.plot(x3, y3tris.T.mean(), color='blue')
    plt.fill_between(x3, confsup[4], confinf[4], facecolor='blue', alpha=0.2)
    plt.plot(x3, y3quad.T.mean(), color='red')
    plt.fill_between(x3, confsup[5], confinf[5], facecolor='red', alpha=0.2)
    plt.ylabel("VV des")
    plt.legend((p1[0],p2[0]),("Irrigué","Non Irrigué"))
    plt.setp(ax3.get_xticklabels(), visible=False)    
    ax4 = plt.subplot(814)
    plt.plot(x2, y4.T.mean(), color='blue')
    plt.fill_between(x2, confsup[6], confinf[6], facecolor='blue', alpha=0.2)
    plt.plot(x2, y4bis.T.mean(), color='red')
    plt.fill_between(x2, confsup[7], confinf[7], facecolor='red', alpha=0.2)
    plt.ylabel("VH asc")
    plt.setp(ax4.get_xticklabels(), visible=False)
    ax5 = plt.subplot(815)
    plt.plot(x3, y4tris.T.mean(), color='blue',linestyle=":")
    plt.fill_between(x3, confsup[8], confinf[8], facecolor='blue', alpha=0.2)
    plt.plot(x3, y4quad.T.mean(), color='red',linestyle=":")
    plt.fill_between(x3, confsup[9], confinf[9], facecolor='red', alpha=0.2)
    plt.ylabel("VH des")
    plt.setp(ax5.get_xticklabels(),visible=False)
    plt.legend((p1[0],p2[0]),("Irrigué","Non Irrigué"))
    ax6= plt.subplot(816)
    plt.plot(yr.index, yr.T.mean(), color='blue',linestyle=":")
    plt.fill_between(yr.index, confsup[10], confinf[10], facecolor='blue', alpha=0.2)
    plt.plot(yr.index, yrbis.T.mean(), color='red',linestyle=":")
    plt.fill_between(yr.index, confsup[11], confinf[11], facecolor='red', alpha=0.2)
    plt.ylabel("ratio des_VH/VV")
    plt.setp(ax6.get_xticklabels(),visible=False)
    ax7= plt.subplot(817)
    plt.plot(yr1.index, yr1.T.mean(), color='blue',linestyle=":")
    plt.fill_between(yr1.index, confsup[12], confinf[12], facecolor='blue', alpha=0.2)
    plt.plot(yr1.index, yrbis1.T.mean(), color='red',linestyle=":")
    plt.fill_between(yr1.index, confsup[13], confinf[13], facecolor='red', alpha=0.2)
    plt.ylabel("ratio asc_VH/VV")
    plt.setp(ax7.get_xticklabels(),visible=False)
    ax8 = plt.subplot(818)
    plt.bar(x6,y6,color='blue',width=1)
    plt.ylabel("pluviométrie en mm")
    plt.setp(ax8.get_xticklabels(),rotation=90)

def col_sqlite(path,name,list_bd_drop,pathlist_names_feature):
    """
    Permet d'attribuer le nom des primitives dans le sqlite a partir de la list des primitives"""
    
    
    dfnames=pd.read_csv(pathlist_names_feature,sep=',', header=None) 
    df1=dfnames.T
    df1.columns=["band_name"]
    colnames=list(df1.band_name.apply(lambda s: s[2:-1]))
    
    if ".csv" in path:
        df=pd.read_csv(path)
        globals()["%s"% name ]=df.groupby("originfid").mean()
        labcroirr=globals()["df%s"% name ].labcroirr
        globals()["df%s"% name ].drop(columns=list_bd_drop,inplace=True)
        globals()["df%s"% name ]=globals()["df%s"% name ].T

        globals()["df%s"% name ]["band_names"]=colnames
        globals()["df%s"% name ]["date"] = globals()["%s"% name ].band_names.apply(lambda s: s[-8:])
        globals()["df%s"% name ].set_index("band_names",inplace=True)
        globals()["df%s"% name ]=globals()["%s"% name ].T
        globals()["df%s"% name ]["labcroirr"]= labcroirr
    else:
       sql=sqlite3.connect(path)
       df=pd.read_sql_query("SELECT * FROM output", sql)
       globals()["df%s"%name]=df.groupby("originfid").mean()
       labcroirr=globals()["df%s"%name]["labcroirr"]
       globals()["df%s"%name].drop(columns=list_bd_drop,inplace=True)
       globals()["df%s"% name ]=globals()["df%s"%name].T
       globals()["df%s"% name ]["band_names"]=colnames
       globals()["df%s"% name ]["date"] = globals()["df%s"% name ].band_names.apply(lambda s: s[-8:])
       globals()["df%s"% name ].set_index("band_names",inplace=True)
       globals()["df%s"% name ]=globals()["df%s"% name ].T
       globals()["df%s"% name ]["labcroirr"]= labcroirr
    return  globals()["df%s"% name ]

def indexdate(df,intervalle_inf,out):
    globals()["%s"% out ] = df.rename(index=lambda x: x[intervalle_inf:])
    globals()["%s"%out].sort_index(inplace=True)
    globals()["%s"%out].index=pd.to_datetime(globals()["%s"%out].index,format="%Y%m%d")

if __name__ == '__main__':
    d={}
    d["SAVE"]="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/"
#    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/tmp/TEST_ANALYSE_SIGNAL/ZONE_TEST_MAIZE.csv")
#    dfpar=df.groupby("originfid").mean()
    Label=[1,2,11,22,33,44]
    label=[1,11]
    polarisation=["asc_vv","des_vv","asc_vh","des_vh","des_userfeature",'asc_userfeature']
    indice=["NDVI","NDWI","Brightness"]
    Indice=["ndvi","ndwi","brightness"]
    features=indice[0:1]+polarisation
#    drop_band=['X', 'Y', 'region', 'labcroirr',"alt_band_0"]
    list_bd_drop=["region","labcroirr","ogc_fid","alt_band_0"]
    list_drop=["labcroirr","ogc_fid"]
    list_drop_bv=["labcroirr","ogc_fid","alt_band_0"]
   # =============================================================================
#     SAFRAN
# =============================================================================
#    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/DONNEES_METEO/SAFRAN_TCJ.csv")
#    date=sorted(list(set(df.DATE)))
    
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

    for z in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/"):
        print(z)
        if '2017' in z:
            tile=z[:3]
            date="2017"
            col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/%s"%z ,tile,list_drop_bv,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")     
        else: 
            tile=z[:3]
            print ('BV')
            col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/%s" %z, tile ,list_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TYN2018.txt")
            date="2018"
        for p in polarisation:
            print (p)
            for i in Label:
                globals()['cropslab%s' % i] = pd.DataFrame( globals()["df%s"% tile ][ globals()["df%s"% tile ].labcroirr==i]).T
                globals()['%s%s' % (p,i)]=[]
                for index,row in globals()['cropslab%s' % i].iterrows():
                    if p in index:
                        globals()['%s%s' % (p,i)].append (row)
                        globals()['df%s%s' %(p,i)]=pd.DataFrame(globals()['%s%s' % (p,i)])
                        globals()["df%s%s"% (p,i)].replace(to_replace =0 , value= pd.NaT,inplace=True)
                        globals()["dbdf%s%s" %(p ,i)]=10*np.log10(globals()['df%s%s' % (p,i)])


        for ind in indice:
            print (ind)
            for i in Label:
                globals()['cropslab%s' % i] = pd.DataFrame(globals()["df%s"% tile ][globals()["df%s"% tile ].labcroirr==i]).T
                globals()['%s%s' %(ind,i)]=[]
                for index,row in globals()['cropslab%s' % i].iterrows():
                    if ind in index:
                        globals()['%s%s' % (ind,i)].append (row)
                        globals()['df%s%s' %(ind,i)]=pd.DataFrame(globals()['%s%s' %(ind,i)])
                        
        for f in features:
            for i in Label:
                if f in polarisation:
                    indexdate(globals()["dbdf%s%s"% (f,i)],-8,'%s%s' % (f,i))
                else:
                    indexdate(globals()["df%s%s"% (f,i)],-8,'%s%s' % (f,i))

                
        confianceinf=[]
        confiancesup=[]

        for i in ["NDVI","asc_userfeature","des_userfeature"]:
            for l in Label:
                print ("%s%s"%(i,l))
                a="%s%s"%(i,l)
                globals()["_%s%s"% (i,l)],globals()["b_sup%s%s"% (i,l)]=stats.t.interval(0.95,globals()["%s%s"%(i,l)].shape[1]-1,loc=globals()["%s%s"%(i,l)].T.mean(),scale=stats.sem(globals()["%s%s"%(i,l)].T))
                confianceinf.append(globals()["_%s%s"% (i,l)])
                confiancesup.append(globals()["b_sup%s%s"% (i,l)])

#        
        for m in os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/SAFRAN/"): # regle meteo pour 2018 sur les auters zones 
            print (m)
            if "2017" in z :
                if m[:3] == tile :
                    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/SAFRAN/%s" % m)
                    df=df[["DATE","PRELIQ_Q"]]
                    globals()["dfSAFR%s"% (tile)]=df.set_index("DATE")
                    globals()["dfSAFR%s"% (tile)].index=pd.to_datetime(globals()["dfSAFR%s"% (tile)].index,format="%Y%m%d")
                elif m[4:7] == tile:
                    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/SAFRAN/%s" % m)
                    df=df[["DATE","PRELIQ_Q"]]
                    globals()["dfSAFR%s"% (tile)]=df.set_index("DATE")
                    globals()["dfSAFR%s"% (tile)].index=pd.to_datetime(globals()["dfSAFR%s"% (tile)].index,format="%Y%m%d")
            else:
                if m[4:7] == tile :
                    df=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/SAFRAN/%s" % m)
                    df=df[["DATE","PRELIQ_Q"]][0:365]
                    globals()["dfSAFR%s"% (tile)]=df.set_index("DATE")
                    globals()["dfSAFR%s"% (tile)].index=pd.to_datetime(globals()["dfSAFR%s"% (tile)].index,format="%Y%m%d")
                    

#        pltmutli(NDVI1.index,VV1.index,NDVI1,NDVI11,NDWI1,NDWI11,VV1,VV11,VH1,VH11,VH_VV1,VH_VV11,globals()["dfSAFR%s"% (tile)].index,globals()["dfSAFR%s"% (tile)].PRELIQ_Q)    
#        plt.savefig(d["SAVE"]+"PLOT_TEMPOREL/comparaison_IRR_NIRR_2017%s.png"% tile)
#        pltmutlimode(NDVI1.index,VVa1.index,VVd1.index,VH_VV1.index,NDVI1,NDVI11,NDWI1,NDWI11,VVa1,VVa11,VVd1,VVd11,VHa1,VHa11,VHd1,VHd11,VH_VV1,VH_VV11,globals()["dfSAFR%s"% (tile)].index,globals()["dfSAFR%s"% (tile)].PRELIQ_Q)
#        plt.savefig(d["SAVE"]+"PLOT_TEMPOREL/comparaison_IRR_NIRR_SARMODE_2017%s.png"% tile)

#        plotconfi(NDVI1.index,asc_vv11.index,des_vv1.index,NDVI1,NDVI11,asc_vv1,asc_vv11,des_vv1,des_vv11,asc_vh1,asc_vh11,des_vh1,des_vh11,des_userfeature1,des_userfeature11,asc_userfeature1,asc_userfeature11,globals()["dfSAFR%s"% (tile)].index,globals()["dfSAFR%s"% (tile)].PRELIQ_Q,confiancesup,confianceinf)
#        plt.savefig(d["SAVE"]+"PLOT_TEMPOREL/comparaison_IRR_NIRR_SARMODE_confiance_2017%s.png"% tile)
#        plotconfi(NDVI1.index,asc_vv11.index,des_vv1.index,NDVI1,NDVI11,asc_vv1,asc_vv11,des_vv1,des_vv11,asc_vh1,asc_vh11,des_vh1,des_vh11,des_userfeature1,des_userfeature11,asc_userfeature1,asc_userfeature11,dfSAFRTCJ.index,dfSAFRTCJ.PRELIQ_Q,confiancesup,confianceinf)

#        
        
        
        
        
        
                ##        
        plt.figure(figsize=(13,10))
        sns.set(style="darkgrid")
        sns.set_context('paper')
        ax1 = plt.subplot(311)
        p1=plt.plot(NDVI1.index,NDVI1.T.mean(),color='blue')
        plt.fill_between(NDVI1.index, confiancesup[0], confianceinf[0], facecolor='blue', alpha=0.2)
        p2=plt.plot(NDVI2.index,NDVI2.T.mean(),color='red',linestyle='--')
        plt.fill_between(NDVI1.index, confiancesup[1], confianceinf[1], facecolor='red', alpha=0.2)
        p3=plt.plot(NDVI11.index,NDVI11.T.mean(),color='blue',linestyle='--')
        plt.fill_between(NDVI1.index, confiancesup[2], confianceinf[2], facecolor='blue', alpha=0.2)
        p4=plt.plot(NDVI22.index,NDVI22.T.mean(),color='red')
        plt.fill_between(NDVI1.index, confiancesup[3], confianceinf[3], facecolor='red', alpha=0.2)
        p5=plt.plot(NDVI33.index,NDVI33.T.mean(),color='green')
        plt.fill_between(NDVI1.index, confiancesup[4], confianceinf[4], facecolor='green', alpha=0.2)
        p6=plt.plot(NDVI44.index,NDVI44.T.mean(),color='pink')
        plt.fill_between(NDVI1.index, confiancesup[5], confianceinf[5], facecolor='pink', alpha=0.2)
        plt.ylabel("NDVI")
        plt.legend((p1[0],p2[0],p3[0],p4[0],p5[0],p6[0]),("Maize_Irr","Soybean_Irr","Maize_Nirr","Soybean_Nirr","Sorghum","Sunflower"))
        plt.setp(ax1.get_xticklabels(),visible=False)
        ax2 = plt.subplot(312)
        p1=plt.plot(asc_userfeature1.index,asc_userfeature1.T.mean(),color='blue')
        plt.fill_between(asc_userfeature1.index, confiancesup[6], confianceinf[6], facecolor='blue', alpha=0.2)
        plt.plot(asc_userfeature2.index,asc_userfeature2.T.mean(),color='red',linestyle='--')
        plt.fill_between(asc_userfeature1.index, confiancesup[7], confianceinf[7], facecolor='red', alpha=0.2)
        plt.plot(asc_userfeature11.index,asc_userfeature11.T.mean(),color='red',linestyle='--')
        plt.fill_between(asc_userfeature1.index, confiancesup[8], confianceinf[8], facecolor='blue', alpha=0.2)
        plt.plot(asc_userfeature22.index,asc_userfeature22.T.mean(),color='red')
        plt.fill_between(asc_userfeature1.index, confiancesup[9], confianceinf[9], facecolor='red', alpha=0.2)
        plt.plot(asc_userfeature33.index,asc_userfeature33.T.mean(),color='green')
        plt.fill_between(asc_userfeature1.index, confiancesup[10], confianceinf[10], facecolor='green', alpha=0.2)
        plt.plot(asc_userfeature44.index,asc_userfeature44.T.mean(),color='pink')
        plt.fill_between(asc_userfeature1.index, confiancesup[11], confianceinf[11], facecolor='pink', alpha=0.2)
        plt.ylabel("VH/VV")
        plt.setp(ax2.get_xticklabels(),visible=False)
        ax3 = plt.subplot(313)
        plt.bar(globals()["dfSAFR%s"% (tile)].index,globals()["dfSAFR%s"% (tile)].PRELIQ_Q,color='blue',width=1)
        plt.ylabel("rainfall (mm)")
        plt.setp(ax3.get_xticklabels(),rotation=90)
        plt.savefig(d["SAVE"]+"PLOT_NDVI_VV_VH_BV/NDVI%s%s.png"% (tile,date))
        
        
        
        
# =============================================================================
#     GEstion DATA TDJ add nom band + date
## =============================================================================
#    list_bd_drop=["ogc_fid",'region', 'labcroirr',"alt_band_0"]
#    sqlite_df('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/Samples_region_1_seed0_learn.sqlite','df2018')
##    df2018.to_csv('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/df2018TCJ.csv')
#    col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/df2018TCJ.csv",'df2018',list_bd_drop)
##    col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/tmp/TEST_ANALYSE_SIGNAL/DT_MAIZE_TCJ_O.csv",'dfTCJ',drop_band[0:4])
#    sqlite_df('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/Samples_region_1_seed4_learn.sqlite','dfr14')
##    dfr14.to_csv('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/dfr14.csv')
##    list_bd_drop=['ogc_fid', 'region', 'labcroirr']
##    col_sqlite('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R14_VV_VH/learningSamples/dfr14.csv','dfr14',list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt")
##    col_sqlite("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/2018_TCJ_S2/learningSamples/Samples_region_1_seed0_learn.sqlite",'df2018',list_bd_drop,"/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_TDJ2018.txt")
##    tile="2018" 
#    for p in polarisation:
#        SAR_process_db(label,dfr14,p)
#        
#    for ind in Indice[:-1]:
#        print (ind)
#        Optique_Process(label,dfr14,ind)
#    
#    for f in Indice[:-1]:
#        indexdate(globals()["df%s1"% f],-8,f.upper()+"1")
#        indexdate(globals()["df%s11"% f],-8,f.upper()+"11")
#
#
#    indexdate(dbdfasc_vv1,-8,'VVa1')
#    indexdate(dbdfasc_vh1,-8,'VHa1')
#    indexdate(dbdfasc_vv11,-8,'VVa11')
#    indexdate(dbdfasc_vh11,-8,'VHa11')
#    
#    indexdate(dbdfdes_vv1,-8,'VVd1')
#    indexdate(dbdfdes_vh1,-8,'VHd1')
#    indexdate(dbdfdes_vv11,-8,'VVd11')
#    indexdate(dbdfdes_vh11,-8,'VHd11')
#    
#    indexdate(dbdfuserfeature1,-8,"VH_VV1")
#    indexdate(dbdfuserfeature11,-8,"VH_VV11")
#
#    VV1=pd.concat([dbdfdes_vv1,dbdfasc_vv1])
#    indexdate(VV1,-8,"VV1")
#
#    VH1=pd.concat([dbdfdes_vh1,dbdfasc_vh1])
#    indexdate(VH1,-8,"VH1")
#
#    VV11=pd.concat([dbdfdes_vv11,dbdfasc_vv11])
#    indexdate(VV11,-8,"VV11")
#    
#    VH11=pd.concat([dbdfdes_vh11,dbdfasc_vh11])
#    indexdate(VH11,-8,"VH11")
#    
#    confianceinf1=[]
#    confiancesup1=[]
#    for i in indice[:-1]:
#        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["%s1"%i].shape[1]-1,loc=globals()["%s1"%i].T.mean(),scale=stats.sem(globals()["%s1"%i].T))
#        confianceinf1.append(globals()["_%s"% (i)])
#        confiancesup1.append(globals()["b_sup%s"% (i)])
#    
#    confianceinf11=[]
#    confiancesup11=[]
#    for i in indice[:-1]:
#        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["%s11"%i].shape[1]-1,loc=globals()["%s11"%i].T.mean(),scale=stats.sem(globals()["%s11"%i].T))
#        confianceinf11.append(globals()["_%s"% (i)])
#        confiancesup11.append(globals()["b_sup%s"% (i)])
#    
#    tab=["VV1","VH1","VV11","VH11","VH_VV1","VH_VV11"]
#    confianceinfSAR=[]
#    confiancesupSAR=[]
#    for i in tab:
#        globals()["_%s"% (i)],globals()["b_sup%s"% (i)]=stats.t.interval(0.95,globals()["%s"%i].shape[1]-1,loc=globals()["%s"%i].T.mean(),scale=stats.sem(globals()["%s"%i].T))
#        confianceinfSAR.append(globals()["_%s"% (i)])
#        confiancesupSAR.append(globals()["b_sup%s"% (i)])
##        
##
#    plt.figure(figsize=(13,10))
#    sns.set(style="darkgrid")
#    sns.set_context('paper')
#    ax1 = plt.subplot(411)
#    p1=plt.plot(NDVI1.index,NDVI1.T.mean(),color='blue')
#    plt.plot(NDVI11.index,NDVI11.T.mean(),color='blue',linestyle='--')
#    plt.plot(NDVI2.index,NDVI2.T.mean(),color='red',linestyle='--')
#    plt.plot(NDVI22.index,NDVI22.T.mean(),color='red')
#    plt.plot(NDVI33.index,NDVI33.T.mean(),color='green')
#    plt.plot(NDVI44.index,NDVI44.T.mean(),color='pink')
##    p2=plt.plot(NDVI1.index,NDVI11.T.mean(),color='red',linestyle='--')
##    plt.fill_between(NDVI1.index, confiancesup1[0], confianceinf1[0], facecolor='blue', alpha=0.2)
##    plt.fill_between(NDVI11.index, confiancesup11[0], confianceinf11[0], facecolor='red', alpha=0.2)
#    plt.ylabel("NDVI")
#    plt.xticks(size='large')
#    plt.yticks(size='large')
#    plt.setp(ax1.get_xticklabels(), visible=False)
#    ax2 = plt.subplot(412)
#    plt.plot(NDVI11.index,NDVI11.T.mean(),color='red',linestyle='--')
##    plt.plot(VH_VV11.index,VH_VV11.T.mean(),color='red',linestyle='--')
##    plt.fill_between(NDVI11.index, confiancesupSAR[4], confianceinfSAR[4], facecolor='blue', alpha=0.2)
##    plt.fill_between(VH_VV11.index, confiancesupSAR[5], confianceinfSAR[5], facecolor='red', alpha=0.2)
#    plt.ylabel("VH_VV en db")
#    plt.xticks(size='large')
#    plt.yticks(size='large')
#    plt.setp(ax2.get_xticklabels(), visible=False)   
#    ax3 = plt.subplot(413)
#    plt.plot(NDVI33.index,NDVI33.T.mean(),color='blue')
##    plt.plot(VV11.index,VV11.T.mean(),color='red',linestyle='--')
##    plt.fill_between(VV1.index, confiancesupSAR[0], confianceinfSAR[0], facecolor='blue', alpha=0.2)
##    plt.fill_between(VV11.index, confiancesupSAR[2], confianceinfSAR[2], facecolor='red', alpha=0.2)
#    plt.ylabel("VV en db")
#    plt.setp(ax3.get_xticklabels(), visible=False)    
#    
#    plt.plot(NDWI1.index,NDWI1.T.mean(),color="blue")
#    plt.plot(NDWI1.index,NDWI11.T.mean(),color='red',linestyle='--')
#    plt.fill_between(NDVI1.index, confiancesup1[1], confianceinf1[1], facecolor='blue', alpha=0.2)
#    plt.fill_between(NDVI11.index, confiancesup11[1], confianceinf11[1], facecolor='red', alpha=0.2)
#    plt.ylabel("NDWI")
#    plt.xticks(size='large')
#    plt.yticks(size='large')
#    plt.setp(ax2.get_xticklabels(), visible=True)
    
    
#    ax3 = plt.subplot(412)
#    plt.plot(VV1.index,VV1.T.mean(),color='blue')
#    plt.plot(VV11.index,VV11.T.mean(),color='red',linestyle='--')
#    plt.fill_between(VV1.index, confiancesupSAR[0], confianceinfSAR[0], facecolor='blue', alpha=0.2)
#    plt.fill_between(VV11.index, confiancesupSAR[2], confianceinfSAR[2], facecolor='red', alpha=0.2)
#    plt.ylabel("VV")
#    plt.setp(ax3.get_xticklabels(), visible=False)    
#    ax4 = plt.subplot(413)
##    plt.plot(VH_VV1.index,VH_VV1.T.mean(),color='blue')
##    plt.plot(VH_VV11.index,VH_VV11.T.mean(),color='red',linestyle='--')
##    plt.fill_between(VH_VV1.index, confiancesupSAR[4], confianceinfSAR[4], facecolor='blue', alpha=0.2)
##    plt.fill_between(VH_VV11.index, confiancesupSAR[5], confianceinfSAR[5], facecolor='red', alpha=0.2)
##    plt.ylabel("VH_VV")
##    plt.xticks(size='large')
##    plt.yticks(size='large')
##    plt.setp(ax4.get_xticklabels(), visible=False)
##
###    plt.setp(ax4.get_xticklabels(), visible=False)
###    ax5 = plt.subplot(615)
###    plt.plot(x4,y5,color='blue')
###    plt.plot(x4, y5bis,color='red',linestyle='--')
###    plt.ylabel("VH/VV")
###    plt.setp(ax5.get_xticklabels(),rotation=False)
##    plt.legend((p1[0],p2[0]),("Irrigué","Non Irrigué"))
#    ax6 = plt.subplot(414)
#    plt.bar(dfSAFRTCJ_O.index,dfSAFRTCJ_O.iloc[:,1],color='blue',width=1)
#    plt.ylabel("pluviométrie en mm")
#    plt.setp(ax6.get_xticklabels(),rotation=90)
#    plt.xticks(size='large')
#    plt.yticks(size='large')
#    plt.savefig(d["SAVE"]+"indices.png")
#    
#
#    sns.set(style="darkgrid")
#    sns.set_context('paper')
#    plt.plot(VV1,color='blue')
#    plt.plot(VVa1,color='red')
#    plt.xticks(rotation=90)
#    plt.show()
###        
#### =============================================================================
####        Calcule de la différence entre IRR et NIRR sur VV
#### =============================================================================
##    diffvv=VV1.T.mean()-VV11.iloc[:,0:4].T.mean()
##    plt.plot(diffvv)
##    diffvv=VV11.T.mean()-VV1.iloc[:,0:4].T.mean()
#    
#    
#    
#
#    
##    
#    dfnames=pd.read_csv("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/list_features_SAR.txt",sep=',', header=None) 
#    df1=dfnames.T
#    df1.columns=["band_name"]
#    colnames=list(df1.band_name.apply(lambda s: s[2:-1]))
#    BV=['TARN',"ADOUR"]
#    for bv in BV:
#        sql=sqlite3.connect("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/ANALYSE_SIGNAL_SAR/DATA_SQLITE/%s_Samples_2017.sqlite"%bv)
#        df=pd.read_sql_query("SELECT * FROM output", sql)
#        globals()["df%s"%bv]=df.groupby("originfid").mean()
#        labcrobvrr=globals()["df%s"%bv]["labcroirr"]
#        globals()["df%s"%bv].drop(columns=list_drop_bv,inplace=True)
#        globals()["df%s"% bv ]=globals()["df%s"%bv].T
#        globals()["df%s"% bv ]["band_names"]=colnames
#        globals()["df%s"% bv ]["date"] = globals()["df%s"% bv ].band_names.apply(lambda s: s[-8:])
#        globals()["df%s"% bv ].set_index("band_names",inplace=True)
#        globals()["df%s"% bv ]=globals()["df%s"% bv ].T
#        globals()["df%s"% bv ]["labcroirr"]= labcroirr
#        
#        for p in polarisation:
#            SAR_process_db(label,globals()["df%s"% bv],p)
#            for i in label :
#                indexdate(globals()["dbdf%s%s"% (p,i)],-8,'%s%s' % (p,i))
#    
#        for ind in indice:
#                print (ind)
#                Optique_Process(label,globals()["df%s"% bv],ind)
#                for i in label:
#                    indexdate(globals()["df%s%s"% (ind,i)],-8,ind.upper()+str(i))
#                    
#        confianceinf=[]
#        confiancesup=[]
#        for i in features:
#            for l in label:
#                print ("%s%s"%(i,l))
#                a="%s%s"%(i,l)
#                globals()["_%s%s"% (i,l)],globals()["b_sup%s%s"% (i,l)]=stats.t.interval(0.95,globals()["%s%s"%(i,l)].shape[1]-1,loc=globals()["%s%s"%(i,l)].T.mean(),scale=stats.sem(globals()["%s%s"%(i,l)].T))
#                confianceinf.append(globals()["_%s%s"% (i,l)])
#                confiancesup.append(globals()["b_sup%s%s"% (i,l)])
#
#        print (bv)    
#        plotconfi(NDVI1.index,asc_vv11.index,des_vv1.index,NDVI1,NDVI11,asc_vv1,asc_vv11,des_vv1,des_vv11,asc_vh1,asc_vh11,des_vh1,des_vh11,des_userfeature1,des_userfeature11,asc_userfeature1,asc_userfeature11,globals()["dfSAFR%s"% (tile)].index,globals()["dfSAFR%s"% (tile)].PRELIQ_Q,confiancesup,confianceinf)
#
##    plt.figure(figsize=(13,10))
##    sns.set(style="darkgrid")
#    sns.set_context('paper')
#    ax1 = plt.subplot(411)
#    p1=plt.plot(asc_userfeature1.index,asc_userfeature1.T.mean(),color='blue')
#    plt.fill_between(asc_userfeature1.index, sup[12], inf[12], facecolor='blue', alpha=0.2)
#    plt.plot(NDVI11.index,NDVI11.T.mean(),color='blue',linestyle='--')
#    plt.plot(NDVI2.index,NDVI2.T.mean(),color='red',linestyle='--')
#    plt.plot(NDVI22.index,NDVI22.T.mean(),color='red')
#    plt.plot(NDVI33.index,NDVI33.T.mean(),color='green')
#    plt.plot(NDVI44.index,NDVI44.T.mean(),color='pink')
#    

