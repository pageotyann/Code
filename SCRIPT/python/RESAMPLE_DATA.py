# -*- coding: utf-8 -*-
#. /datalocal/vboxshare/OTB-6.6.0-Linux64/otbenv.profile
"""
Created on Wed Jan 30 14:00:24 2019

@author: pageot
"""

#==============================================================================
#Script resampling les DATA exogènes 
#=============================================================================
import os
#os.system(". /datalocal/vboxshare/OTB-6.6.0-Linux64/otbenv.profile")
import otbApplication



d={}
d["image_name"] = "SENTINEL2A_20170705-105605-592_L2A_T31TCJ_D_V1-5" 
d['file_img']='/datalocal/vboxshare/THESE/NDVI_2017/file_dezip/'
d["datafile"]= "/datalocal/vboxshare/THESE/CLASSIFICATION/IMG_SAT/L_LST_MASKED/" 
d["199029"]=d["datafile"]+"199029/"
d["199030"]=d["datafile"]+"199030/"
d["img_ref"]="/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/DATA_TRAINING_SIECALC/"
d["B3_image"] =  d["image_name"] + "_FRE_B3.tif"  
d["B4_image"] =  d["image_name"] + "_FRE_B4.tif"  
d["B8A_image"] = d["image_name"] + "_FRE_B8A.tif"  
d["B11_image"] = d["image_name"] + "_FRE_B11.tif" 

d["output"]="/datalocal/vboxshare/THESE/CLASSIFICATION/IMG_SAT/L8_LST_MASKED_W84"

list_img=os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/IMG_SAT/L_LST_MASKED/")
list_emprise=os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/IMG_SAT/L_LST_MASKED/")
Superimpose = otbApplication.Registry.CreateApplication("Superimpose")
for j in list_emprise:
    list_img=os.listdir(d["datafile"] + j +"/")
    for i in list_img:
        Superimpose.SetParameterString("inr", "/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/DATA_TRAINING_SIECALC/SRTM_expo_W84.tif")
        Superimpose.SetParameterString("inm", str(d["datafile"]+j+"/"+ i))
        Superimpose.SetParameterString("out", "%s_resamp_10m.tif"%(i))
    
        print("Launching... Resampling")
# The following line execute the application
        Superimpose.ExecuteAndWriteOutput()
        print("End of Resampling \n")
os.system("mv LC08* /datalocal/vboxshare/THESE/CLASSIFICATION/IMG_SAT/L8_LST_MASKED_W84/")

    
    
    
    
#==============================================================================
# POur un seul img
#==============================================================================
#Superimpose = otbApplication.Registry.CreateApplication("Superimpose")
#Superimpose.SetParameterString("inr", str(d["file_img"] + d["image_name"]+"/"+ d["B4_image"]))
#Superimpose.SetParameterString("inm", str(d["datafile"] + "SRTM_expo_W84.tif"))
#Superimpose.SetParameterString("out", "SRTM_expo_resamp_10m.tif")
#
#print("Launching... Resampling")
## The following line execute the application
#Superimpose.ExecuteAndWriteOutput()
#os.system("mv SRTM* /datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/DATA_TRAINING_SIECALC/")
#print("End of Resampling \n")
## The following line execute the application


 
