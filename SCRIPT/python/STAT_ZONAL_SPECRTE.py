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
import numpy as np 
import seaborn as sns


conn = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/STAT_POLY/Samples_region_1_seed4_learn.sqlite')
df=pd.read_sql_query("SELECT * FROM output", conn)
dfpar=df.groupby("originfid").mean()
a=pd.DataFrame(dfpar.loc[1]).T

STASRTM = sqlite3.connect('/datalocal/vboxshare/THESE/CLASSIFICATION/SRTM_TCJ_SLP_SampleExtraction.sqlite')
df=pd.read_sql_query("SELECT * FROM output", STASRTM)

dfpar=df.groupby("originfid").mean()

dflab=dfpar.groupby("labcroirr").mean()
dflabst=dfpar.groupby("labcroirr").std()
