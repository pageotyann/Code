#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:03:22 2019

@author: pageot
"""


import os
import otbApplication
import argparse
import numpy as np


#/datalocal/vboxshare/THESE/CLASSIFICATION/TEST_SCRIPT/list_features.txt
if __name__ == "__main__":
    # lier les channels du stack via la list des features 
    features=[]
    with open("/datalocal/vboxshare/THESE/CLASSIFICATION/TEST_SCRIPT/list_features.txt", "r") as res_file:
        for line in res_file:
            print(line.rstrip())
            features.append(line.rstrip())
    if "NDVI" in features:
        print(traceback.extract_stack()[-1][1])

    ExtractROI = otbApplication.Registry.CreateApplication("ExtractROI)
    nblignes = 0
    for line in fichier:
     nblignes += 1
 
# Génération du numéro de ligne à chercher
num = random.randint(1,nblignes)
 
# ligne à récupérer ici
         
self.texte = ligne