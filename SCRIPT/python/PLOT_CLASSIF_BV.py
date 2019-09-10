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
    years='2018'
    d={}
    d["SAVE"]="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/PLOT/PLOT_SYNTH_CLASSIF/"

    for b in ["ADOUR","TARN"]: 
        step = []
        jobs=pd.DataFrame()
        KAPPA = []
        OA = []
        KAPPA_s = []
        OA_s = []
        Recall=pd.DataFrame()
        Prec=pd.DataFrame()
        Fscore=pd.DataFrame()
        for classif in os.listdir('/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/FILE_TXT_RESULAT/MAT_CONF_CSV_'+years+'/ASC/'):
            print (classif)
            nom=get_nomenclature("/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/nomenclature_T31TDJ.txt")
            pathNom="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/nomenclature_T31TDJ.txt"
            pathRes="/datalocal/vboxshare/THESE/CLASSIFICATION/RESULT/FILE_TXT_RESULAT/MAT_CONF_CSV_"+years+"/ASC/"+classif+"/"
            all_k = []
            all_oa = []
            all_p = []
            all_r = []
            all_f = []
            all_matrix = []
            for j in os.listdir(pathRes):
                    if ".csv" in j and "regularized" in j and b in j:
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
            f_mean = get_interest_coeff(all_f, nb_lab=len(labels_ref), f_interest="mean")
            p_mean_df=pd.DataFrame(p_mean.items())
            p_mean_df=p_mean_df[1].str.split(expand=True)
            p_mean_df.drop([1],axis=1,inplace=True)
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
        plt_classif_kappa(dfindice_bv,"Kappa","OA")
        plt.savefig(d["SAVE"]+"KAPPA_RUN_"+b+"_"+years+".png",dpi=600,bbox_inches='tight', pad_inches=0.5)
                
        df_names=["step","mean_fscore","std_fscore","mean_Recall","std_Recall","mean_Precision","std_Precision"]
        dfmetric=pd.concat([jobs,Fscore,Recall,Prec],axis=1)
        dfmetric.columns=df_names
        Classe=labels_ref*len(step)
        dfmetric["Classe"]=Classe  
        dfmetric.sort_values("step",inplace=True)
   

        for i in dfmetric[["mean_fscore","mean_Recall","mean_Precision"]]:
            print(i)
            var=i[5:]
            plt.figure(figsize=(20,20))
            sns.set(style="darkgrid")
            sns.set_context('paper')
            g = sns.FacetGrid(dfmetric, col="Classe", col_wrap=6, palette="Set1",height=5)# Gerer la color par run et +3 a modifier en focntion du nb de run 
            g.map_dataframe(errplot, "step", "mean_"+var, "std_"+var)
            g.savefig(d["SAVE"]+var+"_plot_classe_run_"+b+"_"+years+".png",dpi=600,bbox_inches='tight', pad_inches=0.5)

    

