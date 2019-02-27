#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 10:08:55 2019

@author: pageot
"""


import os
import otbApplication

d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/"
d["GSM"]=d["data_file"]+"DONNES_SIG/CARTES_DES_SOLS/GSM/Raster_all/"
d["TILE"]=d["data_file"]+"TRAITEMENT/DATA_GROUND_2017/DPI_2017/IMG_NDVI_2017_TILES/"

list_IMG= os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/CARTES_DES_SOLS/GSM/Raster_all/")
list_tile=os.listdir(d["TILE"])
for i in list_IMG:
    print (i)
    for j in list_tile:
        tile=os.path.basename(j)[-16:-11]
        print(tile)
        Superimpose = otbApplication.Registry.CreateApplication("Superimpose")
        Superimpose.SetParameterString('inm',"/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/CARTES_DES_SOLS/GSM/Raster_all/"+i)
        Superimpose.SetParameterString('inr',d["TILE"]+ j)
        Superimpose.SetParameterInt('interpolator.bco.radius',2)
        Superimpose.SetParameterString("out",d["data_file"]+"TRAITEMENT/DATA_SOIL/GSM_TILES/%s_%s"%(tile,i))
        Superimpose.ExecuteAndWriteOutput()

