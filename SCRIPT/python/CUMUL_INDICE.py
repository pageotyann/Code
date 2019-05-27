#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:45:03 2019

@author: dahingerv
"""



import numpy as np
import pandas as pd
import os
import otbApplication
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create cumul Indice')
	parser.add_argument('-out', dest='out')
	parser.add_argument('-inl', dest='inlist')
	parser.add_argument('-indice', dest='indice')
	parser.add_argument('-tile', dest='tile')
	parser.add_argument('-inp', dest='path',nargs='+',required = True)
	parser.add_argument('-time_vege',dest='vege', action='store_true') 
	args = parser.parse_args()

	print (args.vege)

	#Fichier texte avec labels des bandes par ordre
	#label_file = "/work/CESBIO/projects/Irrigation/dataExogene/T31TCJ/list_features.txt"

	#Mettre en forme le df
	df=pd.read_csv("{}".format(str(args.inlist).strip("['']")),sep=',', header=None)
	df1=df.T
	df1.columns=["band_name"]
	df1.index = np.arange(1, len(df1)+1)
	df1["band"] = df1.index
	df1["indice"] = df1.band_name.apply(lambda s: s[12:16])

	#Tableaux et liste avec les bandes NDVI
	indice = "{}".format(str(args.indice).strip("[]"))
	df_NDVI = df1[df1['indice'] == "{}".format(str(args.indice).strip("[]"))]
	band_NDVI = df_NDVI["band"].tolist()


	path_folder = "{}".format(str(args.path).strip("['']"))
	expres1 = []

	for i in band_NDVI:
		i= "im1b"+str(i)
		expres1.append(i) 
	expres1 = "+".join(str(x) for x in expres1)

	tile="{}".format(str(args.tile).strip("['']"))
	print (tile)
	print (path_folder)
	print (df_NDVI)
	print(indice)

	BMapp1 = otbApplication.Registry.CreateApplication("BandMath")
	BMapp1.SetParameterStringList("il",[path_folder +"Sentinel2_%s_Features.tif"%tile])
	BMapp1.SetParameterString("out",path_folder+"SUM_%s_%s.tif"% (tile,indice))
	BMapp1.SetParameterString("exp", expres1)
	BMapp1.ExecuteAndWriteOutput()  

	if args.vege == True:
		expres=[]
		for i in band_NDVI[8:-3]:
			i= "im1b"+str(i)
			expres.append(i) 
		expres = "+".join(str(x) for x in expres)

		tile="{}".format(str(args.tile).strip("['']"))

		BMapp1 = otbApplication.Registry.CreateApplication("BandMath")
		BMapp1.SetParameterStringList("il",[path_folder +"Sentinel2_%s_Features.tif"%tile])
		BMapp1.SetParameterString("out",path_folder+"SUM_%s_%s_time_vege.tif"% (tile,indice))
		BMapp1.SetParameterString("exp", expres)
		BMapp1.ExecuteAndWriteOutput() 
