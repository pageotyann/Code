#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 14:50:09 2019

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
from STAT_ZONAL_SPECRTE import *
from scipy import stats
from  PLOT_RESULT_CLASSIF import *
from ResultsUtils import *
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def get_interest_coeff(runs_coeff, nb_lab, f_interest="mean"):

    import collections
    nb_run = len(runs_coeff)

    # get all labels
    for run in runs_coeff:
        ref_labels = [label for label, value in list(run.items())]
    ref_labels = sorted(list(set(ref_labels)))
    # init
    coeff_buff = collections.OrderedDict()
    for ref_lab in ref_labels:
        coeff_buff[ref_lab] = []
    # fill-up
    for run in runs_coeff:
        for label, value in list(run.items()):
            coeff_buff[label].append(value)
    # Compute interest coeff
    coeff_out = collections.OrderedDict()
    for label, values in list(coeff_buff.items()):
        if f_interest.lower() == "mean":
            mean = np.mean(values)
            _, b_sup = stats.t.interval(0.95, nb_lab - 1,
                                        loc=np.mean(values),
                                        scale=stats.sem(values))
            if nb_run > 1:
                coeff_out[label] = "{:.3f} +- {:.3f}".format(mean, b_sup - mean)
    return coeff_out



if __name__ == "__main__":
    years='SEASON_TIME_2018' # nom du ficher comptenant l'ensemble des résultats # SEASON_TIME
    bv="ADOUR"
    d={}
    d["SAVE"]="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_SYNTH_CLASSIF/" # path où seront save les graphiques finaux 
    for b in [bv]: 
        step = []
        jobs=pd.DataFrame()
        KAPPA = []
        OA = []
        KAPPA_s = []
        OA_s = []
        Recall=pd.DataFrame()
        Prec=pd.DataFrame()
        Fscore=pd.DataFrame()
        for classif in os.listdir('/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/FILE_TXT_RESULAT/FIxe_seed/SHARK/'+years+'/'): # FIxe_seed/SHARK/'+years+''chemin où sont stocker les matrices de confusion géner avec le script Validation BV
            print (classif)
#            classif="DES_F_3ind_SAFRAN_2017"
            nom=get_nomenclature("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/nomenclature_T31TDJ.txt") # Nomenclature utlisé dans Iota²
            pathNom="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/nomenclature_T31TDJ.txt"
            pathRes="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/FILE_TXT_RESULAT/FIxe_seed/SHARK/"+years+"/"+classif+"/" # FIxe_seed/SHARK/"+years+"/"+classif+"/" ¬ path où sont stocker les fichiers les matrices de confusion
            all_k = []
            all_oa = []
            all_p = []
            all_r = []
            all_f = []
            all_matrix = []
            for j in os.listdir(pathRes):
                    if ".csv" in j and "regularized" in j and b in j: # récupération uniquement des .csv et de matrices issues des classifiactiosn régularisés
                        print (j)
                        conf_mat_dic = parse_csv(pathRes+j)
                        kappa, oacc, p_dic, r_dic, f_dic = get_coeff(conf_mat_dic)
                        all_matrix.append(conf_mat_dic)
                        all_k.append(kappa)
                        all_oa.append(oacc)
                        all_p.append(p_dic)
                        all_r.append(r_dic)
                        all_f.append(f_dic)
            step.append(classif)
            conf_mat_dic = compute_interest_matrix(all_matrix, f_interest="mean")
            nom_dict = get_nomenclature("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/nomenclature_T31TDJ.txt")
            size_max, labels_prod, labels_ref = get_max_labels(conf_mat_dic, nom_dict)
            origin=pd.DataFrame({'step':classif},index=[0],dtype="category")
            origindup=pd.DataFrame(np.repeat(origin.values,len(labels_ref)),dtype="category")
            p_mean = get_interest_coeff(all_p, nb_lab=len(labels_ref), f_interest="mean")
            r_mean = get_interest_coeff(all_r, nb_lab=len(labels_ref), f_interest="mean")
            f_mean = get_interest_coeff(all_f, nb_lab=len(labels_ref), f_interest="mean") # Calcule d'une moyenne pondérer au nombre de classe et de run
            p_mean_df=pd.DataFrame(p_mean.items()) # Transformation en dataframe Pandas
            p_mean_df=p_mean_df[1].str.split(expand=True)
            p_mean_df.drop([1],axis=1,inplace=True) # suppression d'une colonne inutile 
            r_mean_df=pd.DataFrame(r_mean.items())
            r_mean_df=r_mean_df[1].str.split(expand=True)
            r_mean_df.drop([1],axis=1,inplace=True)
            f_mean_df=pd.DataFrame(f_mean.items())
            f_mean_df=f_mean_df[1].str.split(expand=True)
            f_mean_df.drop([1],axis=1,inplace=True)
            KAPPA.append(round(np.mean(all_k),3))
            OA.append(round(np.mean(all_oa),3))
            KAPPA_s.append(round(np.std(all_k),3))
            OA_s.append(round(np.std(all_oa),3))
            Recall=Recall.append(r_mean_df).astype(float)
            Recall.loc[Recall[0]<=0]=0
            Prec=Prec.append(p_mean_df).astype(float)
            Prec.loc[Prec[0]<=0]=0
            Fscore=Fscore.append(f_mean_df).astype(float)
            Fscore.loc[Fscore[0]<=0]=0
            jobs=jobs.append(origindup)
           
        dfindice_bv=pd.DataFrame([step,KAPPA,KAPPA_s,OA,OA_s],index=["step","mean_Kappa","std_Kappa","mean_OA","std_OA"])
        dfindice_bv=dfindice_bv.T
        dfindice_bv[["mean_Kappa","std_Kappa","mean_OA","std_OA"]]=dfindice_bv[["mean_Kappa","std_Kappa","mean_OA","std_OA"]].apply(pd.to_numeric)
        dfindice_bv.set_index("step",inplace=True)
        dfindice_bv.sort_index(inplace=True)
        plt_classif_kappa(dfindice_bv,"Kappa","OA") # Production du graphique
        plt.savefig(d["SAVE"]+"KAPPA_RUN_"+b+"_"+years+".png",dpi=600,bbox_inches='tight', pad_inches=0.5)
                
        df_names=["step","mean_fscore","std_fscore","mean_Recall","std_Recall","mean_Precision","std_Precision"]
        dfmetric=pd.concat([jobs,Fscore,Recall,Prec],axis=1)
        dfmetric.columns=df_names
        Classe=labels_ref*len(step)
        dfmetric["Classe"]=Classe  
        dfmetric.sort_values("step",inplace=True)
        dfMetric=pd.concat([dfmetric[dfmetric['Classe'] != "Sorghum"]])
#######"    Génération des barplot par métriques d'évaluation 

#        for i in dfMetric[["mean_fscore","mean_Recall","mean_Precision"]]:
#            print(i)
#            var=i[5:]
#            plt.figure(figsize=(20,20))
#            sns.set(style="darkgrid")
#            sns.set_context('paper')
#            g = sns.FacetGrid(dfMetric, col="Classe", col_wrap=6, palette="Set1",height=5,margin_titles=False,legend_out=False)# Gerer la color par run et +3 a modifier en focntion du nb de run 
#            g.map_dataframe(errplot, "step", "mean_"+var, "std_"+var)
#            g.savefig(d["SAVE"]+var+"_plot_classe_run_"+b+"_"+years+".png",dpi=600,bbox_inches='tight', pad_inches=0.5)

    plt.figure(figsize=(15,8)) 
    axes = plt.gca()
    ax1=plt.subplot(122)
    axes = plt.gca()
    for i,step in enumerate(dfindice_bv.index):
        x=list(dfMetric[dfMetric.index==0].mean_fscore)[i]
        y=list(dfMetric[dfMetric.index==2].mean_fscore)[i]
        stdx=list(dfMetric[dfMetric.index==0].std_fscore)[i]
        stdy=list(dfMetric[dfMetric.index==2].std_fscore)[i]
        if "2017" in step:
            p=plt.scatter(x,y,color="blue",marker="o")
            a=Ellipse((x,y),width=stdx,height=stdx,alpha=0.2,color="blue",zorder=5)
            axes.add_artist(a)
        else:
            b=plt.scatter(x,y,color="red")
            g=Ellipse((x,y),width=stdx,height=stdx,alpha=0.2,color="red",zorder=5)
            axes.add_artist(g)
        plt.plot([0.1,0.9],[0.1,0.9], 'r-', lw=1)
        plt.xlim(0.1,0.9)
        plt.ylim(0.1,0.9)
        plt.text(x+0.01,y+0.01,step,fontsize=9)
        plt.title("Comparaison of fscore between 2 classe")
        plt.xlabel("F_score Maize Irrigated")
        plt.ylabel("F_score Maize non irrigated")
        plt.legend((p,b),("2017","2018"))
#        plt.legend((a,g),('Intervalle of 95%'))
    ax2=plt.subplot(121)
    axes = plt.gca()
    for i,step in enumerate(dfindice_bv.index):
        x=list(dfMetric[dfMetric.index==1].mean_fscore)[i]
        y=list(dfMetric[dfMetric.index==3].mean_fscore)[i]
        stdx=list(dfMetric[dfMetric.index==1].std_fscore)[i]
        stdy=list(dfMetric[dfMetric.index==3].std_fscore)[i]
        if "2017" in step:
            p=plt.scatter(x,y,color="blue")
            a=Ellipse((x,y),width=stdx,height=stdx,alpha=0.2,color="blue",zorder=5)
            axes.add_artist(a)
        else:
            b=plt.scatter(x,y,color="red")
            g=Ellipse((x,y),width=stdx,height=stdx,alpha=0.2,color="red",zorder=4)
            axes.add_artist(g)
        plt.plot([0.1,0.9],[0.1,0.9], 'r-', lw=1)
        plt.xlim(0.1,0.9)
        plt.ylim(0.1,0.9)
        plt.text(x+0.01,y+0.01,step,fontsize=9)
        plt.title("Comparaison of F-score between 2 classe")
        plt.xlabel("F-score Soybean Irrigated")
        plt.ylabel("F-score Soybean non irrigated")
        plt.legend((p,b),("2017","2018"))
#    ax3=plt.subplot(133)
#    axes = plt.gca()
#    for i,step in enumerate(dfindice_bv.index):
#        x=list(dfMetric[dfMetric.index==0].mean_Precision)[i]
#        y=list(dfMetric[dfMetric.index==2].mean_Precision)[i]
#        stdx=list(dfMetric[dfMetric.index==0].std_Precision)[i]
#        stdy=list(dfMetric[dfMetric.index==2].std_Precision)[i]
#        if "2017" in step:
#            p=plt.scatter(x,y,color="blue")
#            c=Ellipse((x,y),width=stdx,height=stdx,alpha=0.2,color="blue",zorder=5)
#            axes.add_artist(c)
#        else:
#            b=plt.scatter(x,y,color="red")
#            v=Ellipse((x,y),width=stdx,height=stdx,alpha=0.2,color="red",zorder=4)
#            axes.add_artist(v)
#        plt.plot([0.3,0.9],[0.3,0.9], 'r-', lw=1)
#        plt.xlim(0.3,0.9)
#        plt.ylim(0.3,0.9)
#        plt.text(x+0.01,y+0.01,step,fontsize=9)
#        plt.title("Comparaison of Accuracy between 2 classe")
#        plt.xlabel("Accuracy Maize Irrigated")
#        plt.ylabel("Accuracy Maize non irrigated")
#        plt.legend((p,b),("2017","2018"))
#    plt.savefig(d["SAVE"]+"scatter_Classe"+"_"+years+".svg",format="svg")
#    plt.show()
    plt.savefig(d["SAVE"]+"scatter_Classe_"+"_"+years+"_"+bv+".png",format="png",dpi=600,bbox_inches='tight', pad_inches=0.5)

# =============================================================================
# Barplot recall and Acccuracy
## =============================================================================
#    df2017SAFRAN=dfMetric[dfMetric.step.isin(['DES_F_2017','3ind_2017','DES_F_3ind_2017','DES_F_3ind_SAFRAN_2017'])]
#    maize2017=df2017SAFRAN[df2017SAFRAN.index.isin([1,3, 0, 2])]
#    maize2017.set_index(['Classe'],inplace=True)
##    maize2017.sort_index(by=["Classe"],inplace=True)
#    # si soybean modifier les index avec 1&3
##    df2017SAFRAN.plot(kind="bar",x="Classe",y=["mean_Recall","mean_Precision"])
#    df2018SAFRAN=dfMetric[dfMetric.step.isin(['DES_F_2018','3ind_2018','DES_F_3ind_2018','DES_F_3ind_SAFRAN_2018'])]
#    maize2018=df2018SAFRAN[df2018SAFRAN.index.isin([1,3,0,2])]
##    maize2018.sort_index(by=["Classe"],inplace=True)
#    maize2018.set_index(['Classe'],inplace=True)
##    name=set(tuple(maize2017["Classe"]))
#    for i in set(zip(maize2017.step,maize2018.step)):
#        print(i)
#        plt.figure(figsize=(12,5)) 
#        x1=plt.subplot(121)
#        barWidth = 0.3
#        bars1 = maize2017[maize2017.step==i[0]]["mean_Recall"]
#        print (bars1)
#        bars2 = maize2017[maize2017.step==i[0]]["mean_Precision"]
#        yer1 = maize2017[maize2017.step==i[0]]['std_Recall']
#        yer2 = maize2017[maize2017.step==i[0]]['std_Precision']
#        r1 = np.arange(len(bars1))
#        r2 = [x + barWidth for x in r1]
#        plt.bar(r1, bars1, width = barWidth, color = 'orange', edgecolor = 'black', yerr=yer1, capsize=5, label='Recall')
#        plt.bar(r2, bars2, width = barWidth, color = 'royalblue', edgecolor = 'black', yerr=yer2, capsize=5, label='Precision')
#        plt.xticks([r + barWidth - 0.1 for r in range(len(bars2))], maize2017.index,rotation=90) # fixer problème du nom de l'axe"
#        plt.ylabel('value')
#        plt.ylim(0,1)
#        plt.title(str(i[0]))
#        plt.legend()
#        x2=plt.subplot(122)
#        bars1 = maize2018[maize2018.step==i[1]]["mean_Recall"]
#        bars2 = maize2018[maize2018.step==i[1]]["mean_Precision"]
#        yer1 = maize2018[maize2018.step==i[1]]['std_Recall']
#        yer2 = maize2018[maize2018.step==i[1]]['std_Precision']
#        r1 = np.arange(len(bars1))
#        r2 = [x + barWidth for x in r1]
#        plt.bar(r1, bars1, width = barWidth, color = 'orange', edgecolor = 'black', yerr=yer1, capsize=5, label='Recall')
#        plt.bar(r2, bars2, width = barWidth, color = 'royalblue', edgecolor = 'black', yerr=yer2, capsize=5, label='Precision')
#        plt.xticks([r + barWidth - 0.1 for r in range(len(bars2))], maize2018.index,rotation=90)
#        plt.ylabel('value')
#        plt.ylim(0,1)
#        plt.title(str(i[1]))
#        plt.legend()
#        plt.savefig(d["SAVE"]+"barplot_Recall_Accura_crops irrigated"+"_"+years+i[0]+"_"+bv+".png",format="png",dpi=600,bbox_inches='tight', pad_inches=0.5)
#    
# =============================================================================
#     SEASON_TIME
# =============================================================================
    plt.figure(figsize=(10,7)) 
    a=dfMetric[dfMetric.index==0]
    b=dfMetric[dfMetric.index==2]
    plt.plot(a.step,a["mean_fscore"],color='blue',label='Irr')
    plt.fill_between(a.step,a["mean_fscore"]+a["std_fscore"],a["mean_fscore"]-a["std_fscore"],alpha=0.2,color='blue')
    plt.plot(b.step,b["mean_fscore"],color='red',label='non Irr')
    plt.fill_between(a.step,b["mean_fscore"]+b["std_fscore"],b["mean_fscore"]-b["std_fscore"],alpha=0.2,color='red')
    plt.xticks(rotation=45)
    plt.ylim(0.1,0.9)
    plt.ylabel("F_score")
    plt.title(str(bv)+"_"+str(years))
    plt.legend()
    plt.savefig(d["SAVE"]+"fscore_maize"+"_"+years+"_"+bv+".png",format="png",dpi=600,bbox_inches='tight', pad_inches=0.5)
