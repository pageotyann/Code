#!/usr/bin/python
# coding: utf-8
# source /datalocal/vboxshare/OTB-6.6.0-Linux64/otbenv.profile
# 

import os
import otbApplication
import zipfile
import csv


images = []
imagefile = "/datalocal/vboxshare/THESE/NDVI_2017/images2.txt"
file = open(imagefile, "rb")
try:
    #
    # Création du ''lecteur'' CSV.
    #
    reader = csv.reader(file)
    print(reader)
    #
    # Le ''lecteur'' est itérable, et peut être utilisé
    # dans une boucle ''for'' pour extraire les
    # lignes une par une.
    #
    for row in reader:
		images.append(row[0])
finally:
    #
    # Fermeture du fichier source
    #
    file.close()
print images

#images =["SENTINEL2A_20170612-104258-592_L2A_T31TCJ_D.zip", "SENTINEL2A_20170622-104021-457_L2A_T31TCJ_D.zip"]
for i in images : 
	zip_ref = zipfile.ZipFile(i, 'r')
	zip_ref.extractall()
	zip_ref.close()
	print (i)
	os.system ("mv *_V1* file_dezip/")

Images_nan_zip= os.listdir("/datalocal/vboxshare/THESE/NDVI_2017/file_dezip")	
print (Images_nan_zip)

#list (ensembe des ficiers sans l'extension.zip)	
for j in Images_nan_zip: 
	path_img=os.path.basename(j)
	print path_img

	d={}
	d["dataset_folder"] = "/datalocal/vboxshare/THESE/NDVI_2017/file_dezip/"

	d["image_name"] = path_img  
	d["input_path"] = d["dataset_folder"]+d["image_name"] +"/"
	d["B4_image"] =  d["image_name"] + "_FRE_B4.tif"  
	d["B8_image"] = d["image_name"] + "_FRE_B8.tif" 
	d["B3_image"] = d["image_name"] + "_FRE_B3.tif" 
	d["coulds_mask"] = "MASKS/" + d["image_name"] + "_CLM_R1.tif"
	print  d["coulds_mask"]
	print d["input_path"] + d["coulds_mask"]
	print d["input_path"] + d["B4_image"]
	###Aplliquer mask 

    #cahine en mémore les autres bandes avec concat
	App= otbApplication.Registry.CreateApplication("ConcatenateImages")
	App.SetParameterStringList("il",[str(d["input_path"] + d["B4_image"])])
	App.SetParameterString("out","B4_image.tif")
	App.Execute()

	App2 = otbApplication.Registry.CreateApplication("ConcatenateImages")
	App2.SetParameterStringList("il",[str(d["input_path"] + d["B8_image"])])
	App2.SetParameterString("out","B8_image.tif")
	App2.Execute()

	App3 = otbApplication.Registry.CreateApplication("ConcatenateImages")
	App3.SetParameterStringList("il",[str (d["input_path"] + d["B3_image"])])
	App3.SetParameterString("out", "B3_image.tif")
	App3.Execute()

   #Création du mask nuage en binaire
	application1 = otbApplication.Registry.CreateApplication("BandMath")
	application1.SetParameterStringList("il",[str(d["input_path"] + d["coulds_mask"])])
	application1.SetParameterString("out", "maskname.tif")
   	#application1.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
	application1.SetParameterString("exp", 'im1b1 > 1 ? im1b1 = 0 : im1b1 = 1')
  
	
 
   # The following line execute the application1
	application1.Execute()
	print("conversion Mask\n")

   	#Application mask B4 

	application2 = otbApplication.Registry.CreateApplication("BandMath")

	application2.AddImageToParameterInputImageList("il",application1.GetParameterOutputImage("out")) 
	application2.AddImageToParameterInputImageList("il",App.GetParameterOutputImage("out"))
	application2.SetParameterString("out", "B4_image_M.tif")
   	#application2.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
	application2.SetParameterString("exp", "(im1b1*im2b1)")
   	
	application2.Execute()

   	#Application mask sur B8

	application3 = otbApplication.Registry.CreateApplication("BandMath")

	application3.AddImageToParameterInputImageList("il",application1.GetParameterOutputImage("out"))
	application3.AddImageToParameterInputImageList("il",App2.GetParameterOutputImage("out"))
	application3.SetParameterString("out","B8_image_M.tif")
	application3.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
	application3.SetParameterString("exp", "(im1b1*im2b1)")
	application3.Execute()

	#Application mask sur B3

	application5 = otbApplication.Registry.CreateApplication("BandMath")

	application5.AddImageToParameterInputImageList("il",application1.GetParameterOutputImage("out"))
	application5.AddImageToParameterInputImageList("il",App3.GetParameterOutputImage("out"))
	application5.SetParameterString("out","B3_image_M.tif")
	#application5.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
	application5.SetParameterString("exp", "(im1b1*im2b1)")
	application5.Execute()

   	########### Application 2 : NDVI Calculation
    #
    # Create the necessary OTB Applications
	application4 = otbApplication.Registry.CreateApplication("BandMath")
    
    # ---
    # FILL THE GAP 2 : In-memory connection:
    #                  declare the application1 output as the application2
    #                  input (input name "il", StringList type)
    #        
    # Example:
	application4.AddImageToParameterInputImageList("il",application2.GetParameterOutputImage("out"))
	application4.AddImageToParameterInputImageList("il",application3.GetParameterOutputImage("out"))
    #
    # END OF GAP 
    # ---
    
    # Declare the input list : the first element is declared alone (im1 = Red-B4
	application4.SetParameterString("out", "NDVI_%s.tif"%(path_img))
   	#application4.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
  

    # ---
    # FILL THE GAP 3 : Complete the BandMath expression 
    #        
    # Example:  
	application4.SetParameterString("exp", "(im2b1-im1b1)/(im2b1+im1b1)")
   	# 
    # END OF GAP 
    # ---
    # The following line execute the application
    #print("Launching... BandMath : Water Mask by using NDVI")
	application4.ExecuteAndWriteOutput()
	os.system("mv *NDVI_S* /datalocal/vboxshare/THESE/NDVI_2017")
    #print("End of BandMath NDVI \n")

	###CREATION IMG_FAUSSE COLOR


	App4 = otbApplication.Registry.CreateApplication("ConcatenateImages")
	App4.AddImageToParameterInputImageList("il",application3.GetParameterOutputImage("out"))
	App4.AddImageToParameterInputImageList("il",application2.GetParameterOutputImage("out"))
	App4.AddImageToParameterInputImageList("il",application5.GetParameterOutputImage("out"))
	App4.SetParameterString("out", "IMG_F_COLOR_%s.tif"%(path_img))
	App4.ExecuteAndWriteOutput()

	os.system("mv *NDVI_S* /datalocal/vboxshare/THESE/NDVI_2017")
	os.system("mv *IMG_F* /datalocal/vboxshare/THESE/NDVI_2017")