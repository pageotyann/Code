#!/usr/bin/python
# coding: utf-8

# 

import os
import csv
import gdal
import argparse


def fusion_sm(empriseA,empriseB):
	for i in empriseA:
		date=i[0:8]
		for j in empriseB :
			date2=j[0:8]
			if date==date2:
				print ("processing en cours")
				os.system("gdal_merge.py -o SM_%s.tif %s/%s %s/%s -n 0.0"%(date,PATHA,i,PATHB,j))
			else : 
				print ("pas de Fusion")

	os.system("mv SM* %s"%(outpath))

def fusion_sm4(empriseA,empriseB,empriseC,empriseD):
    for i in empriseA:
        date=i[0:8]
        for j in empriseB:
            date2=j[0:8]
            for k in empriseC:
                date3=k[0:8]
                for l in empriseD:
                    date4=l[0:8]
                    if date==date2:
                        if date==date3:
                            if date==date4:
                                if date2==date3:
                                    if date2==date4:
                                        if date3==date4:
                                            os.system("gdal_merge.py -o SM_%s.tif %s/%s %s/%s %s/%s %s/%s -n 0.0"%(date,PATHA,i,PATHB,j,PATHC,k,PATHD,l))
                                        else:
                                            print ("pas de fusing")
#    os.system("mv SM* %s"%(outpath))

if __name__ == '__main__':
 	# parser = argparse.ArgumentParser(description='Process some integers.')
 	# parser.add_argument('-out', dest='out',mandatory=True)
 	# parser.add_argument('-in', dest='path',nargs='+')
 	# args = parser.parse_args()
 	# print args.path
 	# print args.out
 	d={}
 	d["dataset_folder"] = "/datalocal/vboxshare/THESE/CLASSIFICATION/IMG_SAT/L_LST_MASKED/"
 	d["empriseA"]= d["dataset_folder"] + "198029" +"/"
 	d["empriseB"]= d["dataset_folder"] + "198030" +"/"
 	outpath = "/datalocal/vboxshare/THESE/CLASSIFICATION/IMG_SAT/"	
 	
 	PATHA=d["empriseA"]
 	PATHB=d["empriseB"]	
 	empriseA = os.listdir(PATHA)
 	empriseB = os.listdir(PATHB)
 	fusion_sm(empriseA,empriseB)
  

#if __name__ == '__main__':
#	# parser = argparse.ArgumentParser(description='Process some integers.')
#	# parser.add_argument('-out', dest='out',mandatory=True)
#	# parser.add_argument('-in', dest='path',nargs='+')
#	# args = parser.parse_args()
#	# print args.path
#	# print args.out
#	d={}
#	d["dataset_folder"] = "/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/CARTES_SOIL_MOISTURE/"
#	d["empriseA"]= d["dataset_folder"] + "Fp1_S1a" +"/"
#	d["empriseB"]= d["dataset_folder"] + "Fp2_S1a" +"/"
#
#	outpath = "/datalocal/vboxshare/THESE/CLASSIFICATION/TRAITEMENT/SOIL_MOISTURE/"	
#	
#	PATHA=d["empriseA"]
#	PATHB=d["empriseB"]	
#
#	empriseA = os.listdir(PATHA)
#	empriseB = os.listdir(PATHB)
#
#	fusion_sm(empriseA,empriseB)
 
 