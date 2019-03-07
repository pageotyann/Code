#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:48:40 2019

@author: pageot
"""

import os
import otbApplication




#
#otbcli_PolygonClassStatistics -in IMG.tif -vec Vector.shp -field CODE -out stat.xml
#
#otbcli_SampleSelection -in IMG.tif -vec Vector.shp -field CODE -instats stat.xml -strategy all -out SampleSelection.sqlite
#
#otbcli_SampleExtraction -in IMG.tif -vec SampleSelection.sqlite -field code -out SampleExtraction.sqlite


d={}
d["data_file"]="/datalocal/vboxshare/THESE/CLASSIFICATION/"
d["DATA"]= d["data_file"]+"DONNES_SIG/SRTM/SRTM/SRTM_TILE/"
d["EXPO"]=d["data_file"]+"TRAITEMENT/SRTM/MASK_SRTM_TILE/"
d["vector"]=d["data_file"]+"TRAITEMENT/DATA_GROUND_2017/DT_2017_ALL/DT_ALL_2017_REGROUP_CLASS/DT_TCJ_2017_ER10_W84_NEW_CLASS.shp"
label="LABCROIRR"
label1="labcroirr"


for i in os.listdir(d["EXPO"]):
    print (i)
    os.system("otbcli_PolygonClassStatistics -in %s%s -vec %s -field %s -out stat.xml"%(d["EXPO"],i,d["vector"],label))
    os.system("otbcli_SampleSelection -in %s%s -vec %s -field %s -instats stat.xml -strategy all -out SampleSelection.sqlite"%(d["EXPO"],i,d["vector"],label))
    os.system("otbcli_SampleExtraction -in %s%s -vec SampleSelection.sqlite -field %s -out %s_SampleExtraction.sqlite"%((d["EXPO"],i,label1,i)))
    os.system("mv stat.xml")
    os.system("mv SampleSelection.sqlite")
    

