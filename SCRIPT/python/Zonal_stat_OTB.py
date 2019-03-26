#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:48:40 2019

@author: pageot
"""

import os
import otbApplication







d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/"
d["DATA"]= d["data_file"]+"DONNES_SIG/SRTM/SRTM/SRTM_TILE/"
d["EXPO"]=d["data_file"]+"TRAITEMENT/SRTM/EXPO_TILE_SRTM/EXPO_RECLASS/"
d["vector"]=d["data_file"]+"TRAITEMENT/DATA_GROUND_2017/DT_2017_ALL/DT_ALL_2017_REGROUP_CLASS/DT_ALL_2017_W84_ER10_RECLASS.shp"
d["SM"]=d["data_file"]+"TRAITEMENT/SOIL_MOISTURE/"
d["SAFARN"]="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/DATA_METEO/"
label="LABCROIRR"
label1="labcroirr"


for i in os.listdir(d["SAFRAN"]):
    print (i)
    os.system("otbcli_PolygonClassStatistics -in %s%s -vec %s -field %s -out stat.xml"%(d["SAFRAN"],i,d["vector"],label))
    os.system("otbcli_SampleSelection -in %s%s -vec %s -field %s -instats stat.xml -strategy all -out SampleSelection.sqlite"%(d["SAFRAN"],i,d["vector"],label))
    os.system("otbcli_SampleExtraction -in %s%s -vec SampleSelection.sqlite -field %s -out %s_SampleExtraction.sqlite"%((d["SAFRAN"],i,label1,i)))
    os.system("mv stat.xml")
    os.system("mv SampleSelection.sqlite")
    

