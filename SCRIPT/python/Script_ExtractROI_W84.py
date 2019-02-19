# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 16:38:43 2019

@author: pageot
"""

# import os

# import otbApplication

# list_SM=os.listdir("/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/SRTM/")
# ExtractROI = otbApplication.Registry.CreateApplication("ExtractROI")
# Superimpose = otbApplication.Registry.CreateApplication("Superimpose")
# for i in list_SM:
#     ExtractROI.SetParameterString("in", "/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/SRTM/" + str(i))
#     ExtractROI.SetParameterString("mode","fit")  
#     ExtractROI.SetParameterString("mode.fit.im","/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/IMG_W84_31TCJ.tif")
#     ExtractROI.SetParameterString("out", i+"cutTCJ.tif")

#     ExtractROI.ExecuteAndWriteOutput()
#     os.system("mv SRTM_* SRTM_cut/")
# list_cut=os.listdir("/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/")
# for j in list_cut:
     
#     Superimpose.SetParameterString("inr","/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/IMG_W84_31TCJ.tif")
#     Superimpose.SetParameterString("inm", "/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/"+ str(j))  
#     Superimpose.SetParameterString("out", j+"resamp_10m.tif")
    
#     Superimpose.ExecuteAndWriteOutput()
    
# #
# #for i in list_SM:
# #    os.system("otbcli_ExtractROI -in %s -mode fit -mode.fit.im /datalocal/vboxshare/THESE/IMG_W84_31TCJ.tif -out %s_cutTCJ.tif"%(i))
# #   


import os
import otbApplication


ExtractROI = otbApplication.Registry.CreateApplication("ExtractROI")
Superimpose = otbApplication.Registry.CreateApplication("Superimpose")
list_IMG= os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/CARTES_DES_SOLS/GSM/Raster_all/")

for a in list_IMG:
    os.system("gdalwarp -t_srs EPSG:4326 -r near -of GTiff /datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/CARTES_DES_SOLS/GSM/Raster_all/%s -overwrite warp_W84_%s"%(a,a)) 
os.system('mv warp_W84* /datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/DATA_warp_w84/')

list_IMG_warp=os.listdir("/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/DATA_warp_w84/")
for i in list_IMG_warp:
    ExtractROI.SetParameterString("in", "/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/DATA_warp_w84/" + str(i))
    ExtractROI.SetParameterString("mode","fit")  
    ExtractROI.SetParameterString("mode.fit.im","/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/EMPRISE/Raster_ALL_W84.tif")
    ExtractROI.SetParameterString("out", i+"cut_all.tif")

    ExtractROI.ExecuteAndWriteOutput()
os.system("mv *cut_all.tif /datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/IMG_cut/")
# list_cut=os.listdir("/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/")
# for j in list_cut:
     
#     Superimpose.SetParameterString("inr","/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/IMG_W84_31TCJ.tif")
#     Superimpose.SetParameterString("inm", "/datalocal1/home/pageoty/THESE/DATA_IOTA/DATA_IMG/"+ str(j))  
#     Superimpose.SetParameterString("out", j+"resamp_10m.tif")
    
#     Superimpose.ExecuteAndWriteOutput()