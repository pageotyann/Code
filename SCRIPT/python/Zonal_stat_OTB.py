#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:48:40 2019

@author: pageot
"""
import sqlite3
import argparse
import numpy as np
import pandas as pd
import os
import otbApplication




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Zonalstat programme. this programme allows to recover polyone statistic ')
    parser.add_argument('-outstat', dest='outstat')
    parser.add_argument('-vec', dest='vector',nargs='+',help='shapefile',required = True)
    parser.add_argument('-inp', dest='image',nargs='+',help="image where extract informtion",required = True)
    parser.add_argument('-lab',dest='label',nargs='+',help='Name of field',required = True)
    parser.add_argument('-pixel',dest='pixel', action='store_false') 
    args = parser.parse_args()
    print (args.vector)
    print (args.image)
    print(args.pixel)  


# Ajoute une fonction if si tu veux les statistiques au polygones
    for i in os.listdir("{}".format(str(args.image).strip("['']"))):
        print (i)
        os.system("otbcli_PolygonClassStatistics -in %s%s -vec %s -field %s -out stat.xml"%("{}".format(str(args.image).strip("['']")),i,"{}".format(str(args.vector).strip("['']")),"{}".format(str(args.label).strip("['']"))))
        os.system("otbcli_SampleSelection -in %s%s -vec %s -field %s -instats stat.xml -strategy all -out SampleSelection.sqlite"%("{}".format(str(args.image).strip("['']")),i,"{}".format(str(args.vector).strip("['']")),"{}".format(str(args.label).strip("['']"))))
        os.system("otbcli_SampleExtraction -in %s%s -vec SampleSelection.sqlite -field %s -out %s/SampleExtraction%s.sqlite"%("{}".format(str(args.image).strip("['']")),i,"{}".format(str(args.label).strip("['']")).lower(),"{}".format(str(args.outstat).strip("['']")),i))
#        os.system("rm stat.xml")
#        os.system("rm SampleSelection.sqlite")
        
    if args.pixel==True:
        for j in os.listdir("{}".format(str(args.outstat).strip("['']"))):
            if ".sqlite" in j:
                print (j)
                conn = sqlite3.connect("{}".format(str(args.outstat).strip("['']"))+j)
                df=pd.read_sql_query("SELECT * FROM output", conn)
                globals()["dfpar%s"%j[:-7]]=df.groupby("originfid").mean()
                globals()["dfpar%s"%j[:-7]].to_csv("{}".format(str(args.outstat).strip("['']"))+"%s.csv"%(j[:-7]))
            
            
            
            
