#!/usr/bin/python
#-*- coding: utf-8 -*-

# =========================================================================
#   Program:   iota2
#
#   Copyright (c) CESBIO. All rights reserved.
#
#   See LICENSE for details.
#
#   This software is distributed WITHOUT ANY WARRANTY; without even
#   the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the above copyright notices for more information.
#
# =========================================================================

import argparse
import sys
import os
import csv
import math
from osgeo import ogr
import vector_functions as vf

classes = []
def countByAtt(shpfile, field, storecsv="", val=None):

    ds = vf.openToRead(shpfile)
    fields = vf.getFields(shpfile)	
    layer = ds.GetLayer()
    if val is None:
        for feature in layer:
            cl =  feature.GetField(field)
            if cl not in classes:
                classes.append(cl)
    else:
        classes.append(val)      

    layerDfn = layer.GetLayerDefn()
    fieldTypeCode = layerDfn.GetFieldDefn(fields.index(field)).GetType()
    classes.sort()
        
    layer.ResetReading()
    totalarea = 0
    if "POLYGON" in vf.getGeomTypeFromFeat(shpfile):
        for feat in layer:
            geom = feat.GetGeometryRef()
            if geom:
                if not math.isnan(geom.GetArea()):
                    totalarea += geom.GetArea()

    stats = []        
    for cl in classes:
        if fieldTypeCode == 4:
            layer.SetAttributeFilter(field+" = \""+str(cl)+"\"")
            featureCount = layer.GetFeatureCount()
                        
            if "POLYGON" in vf.getGeomTypeFromFeat(shpfile):
                area = 0
                for feat in layer:
                    geom = feat.GetGeometryRef()
                    if geom:
                        area += geom.GetArea()
                partcl = area / totalarea * 100
                        
                if storecsv == "" or storecsv is None:
                    print "Class # %s: %s features and a total area of %s (rate : %s)"%(str(cl), \
                                                                                        str(featureCount),\
                                                                                        str(area), \
                                                                                        str(round(partcl,2)))
                stats.append([cl, featureCount, area, partcl])
            else:
                print "Class # %s: %s features"%(str(cl), \
                                                 str(featureCount))
                stats.append([cl, featureCount])                                        

            layer.ResetReading()
	else:
	    layer.SetAttributeFilter(field+" = "+str(cl))
   	    featureCount = layer.GetFeatureCount()
            
            if "POLYGON" in vf.getGeomTypeFromFeat(shpfile):
                area = 0
                for feat in layer:
                    geom = feat.GetGeometryRef()
                    if geom:
                        area += geom.GetArea()
                partcl = area / totalarea * 100
                if storecsv == "" or storecsv is None:
                    print "Class # %s: %s features and a total area of %s (rate : %s)"%(str(cl), \
                                                                                        str(featureCount),\
                                                                                        str(area),\
                                                                                        str(round(partcl,2)))
                    stats.append([cl, featureCount, area, partcl])
            else:
                print "Class # %s: %s features"%(str(cl), \
                                                 str(featureCount))
                
                stats.append([cl, featureCount])
                                
	    layer.ResetReading()

    if storecsv != "" and storecsv is not None:
        with open(storecsv, "w") as f:
            writer = csv.writer(f)
            writer.writerows(stats)
            
    return stats

if __name__ == "__main__":
    if len(sys.argv) == 1:
	prog = os.path.basename(sys.argv[0])
	print '      '+sys.argv[0]+' [options]' 
	print "     Help : ", prog, " --help"
	print "        or : ", prog, " -h"
	sys.exit(-1)  
    else:
	usage = "usage: %prog [options] "        
	parser = argparse.ArgumentParser(description = "This function allows to compute number of features and "\
                                         "total area of each value (or given value) of a given field")

	parser.add_argument("-shape", help = "path to a shapeFile (mandatory)", dest = "shape", required=True)
	parser.add_argument("-field", help = "data's field into shapeFile (mandatory)", dest = "field", required=True)
	parser.add_argument("-value", dest = "value", help = "value to field to search")
	parser.add_argument("-storecsv", dest = "storecsv", help = "csv file to store stats, if None : Verbose mode activate")        
	args = parser.parse_args()
	countByAtt(args.shape, args.field, args.storecsv, args.value)

