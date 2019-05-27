#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:45:03 2019

@author: dahingerv
"""

import sqlite3
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns; sns.set()
import STAT_ZONAL_SPECRTE
from scipy import stats

#path = "/home/dahingerv/Documents/Iota/2017_S2/Loiret_2803/Results/learningSamples/Samples_region_1_seed0_learn.sqlite"
#path = "/home/dahingerv/Documents/Iota/2018_S2_saison/1504_Loiret/Results/learningSamples/Samples_region_1_seed0_learn.sqlite"
bande_NIR = '_b6' # '_b5' pour NDRE1 ou '_b6' pour NDRE2
bande_b8a = '_b8a'
indice_nom_graph = 'NDRE'
sqlite_df("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/STAT_CLASSIF/R24_TCJ_CUMUL_NDVI/learningSamples/Samples_region_1_seed4_learn.sqlite",'df_par_spectre')


#conn = sqlite3.connect(path)
#df_spectre = pd.read_sql_query("SELECT * FROM output", conn)
#
## Regrouper par parcelle
#df_par_spectre = df_spectre.groupby("originfid").mean()

# Garder la colonne irigation, puis la supprimer
irrig = df_par_spectre['irrigation']
df_par_spectre.drop(['irrigation'], axis='columns', inplace=True)

# Sélectionner les colonnes en fonction de l'indice souhaité, puis renommer les colonnes
df_NIR = df_par_spectre.filter(like=bande_NIR)
df_b8a = df_par_spectre.filter(like=bande_b8a)

df_NIR_col = df_NIR.rename(columns=lambda x: x[-4:])
df_b8a_col = df_b8a.rename(columns=lambda x: x[-4:])

# Calcul du NDRE
df_indice = (df_b8a_col - df_NIR_col)/(df_b8a_col + df_NIR_col)

# Faire la moyenne des mois
df_spectre_mois = df_indice.groupby(by=df_indice.columns, axis=1).mean()

# Faire le cumul date par date
df_cumul_spectre = df_spectre_mois.cumsum(axis=1)

# Ajouter la colonne irrigation
df_cumul_spectre['irrigation']=irrig

# Faire la moyenne des parcelles et les écart-types
df_cumul_mean = df_cumul_spectre.groupby("irrigation").mean().T
#df_cumul_std = df_cumul_spectre.groupby("irrigation").std().T

# Renommer les colonnes pour graphique
df_cumul_mean.columns = ["Mais_non_irrigue","Mais_irrigue"]
#df_cumul_std.columns = ["Mais_non_irrigue","Mais_irrigue"]

#Graphique
t = df_cumul_mean.index.values

X1 = df_cumul_mean["Mais_non_irrigue"]
X2 = df_cumul_mean["Mais_irrigue"]

sigma1 = df_cumul_std["Mais_non_irrigue"]
sigma2 = df_cumul_std["Mais_irrigue"]

fig, ax = plt.subplots()#(figsize=(10, 7))
ax.plot(t, X1,  label="Mais non irrigue", color='orange')
ax.plot(t, X2, label="Mais irrigue", color='blue')
ax.fill_between(t, X1+sigma1, X1-sigma1, facecolor='orange', alpha=0.2)
ax.fill_between(t, X2+sigma2, X2-sigma2, facecolor='blue', alpha=0.2)
ax.set_title(r'Cumul des NDRE (B8A et B5) en 2018')
ax.legend(loc='upper left')
ax.set_xlabel('Mois')
ax.set_ylabel('Cumul ndre moyen')
#plt.savefig("CUMULmensuel_ndre_B8A-B5_ecartType_2017.png")