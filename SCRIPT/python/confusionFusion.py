#!/usr/bin/python

import sys
import argparse
import numpy as np
def parseConfusionMatrices(csvPaths):
       	"""
	IN :
		csvPaths [string] : list of path to csv files
			ex : ["/path/to/file1.csv","/path/to/file2.csv"]
	OUT : 
		out [list of lists] : containing csv's coordinates

		ex : file1.csv
			#Reference labels (rows):11
			#Produced labels (columns):11,12
			14258,52

		     file2.csv
			#Reference labels (rows):12
			#Produced labels (columns):11,12
			38,9372

		out = [[12,[11,38]],[12,[12,9372]],[11,[11,14258]],[11,[12,52]]]
	"""
        out = []
        for csvPath in csvPaths:
                cpty = 0
                FileMat = open(csvPath,"r")
	        while 1:
		        data = FileMat.readline().rstrip('\n\r')
		        if data == "":
			        FileMat.close()
			        break
		        if data.count('#Reference labels (rows):')!=0:
			        ref = data.split(":")[-1].split(",")
		        elif data.count('#Produced labels (columns):')!=0:
			        prod = data.split(":")[-1].split(",")
		        else:
			        y = ref[cpty]
			        line = data.split(",")
			        cptx = 0
			        for val in line:
				        x = prod[cptx]
				        out.append([int(y),[int(x),float(val)]])
				        cptx+=1
		       	        cpty +=1
        return out

def parseRefLabels(csvPaths):
       	"""
	IN :
		csvPaths [string] : list of path to csv files
			ex : ["/path/to/file1.csv","/path/to/file2.csv"]
	OUT : 
		out [list of lists] : containing csv's coordinates

		ex : file1.csv
			#Reference labels (rows):11
			#Produced labels (columns):11,12
			14258,52

		     file2.csv
			#Reference labels (rows):12
			#Produced labels (columns):11,12
			38,9372

		out = [[12,[11,38]],[12,[12,9372]],[11,[11,14258]],[11,[12,52]]]
	"""
        out = []
        for csvPath in csvPaths:
                cpty = 0
                FileMat = open(csvPath,"r")
	        while 1:
		        data = FileMat.readline().rstrip('\n\r')
		        if data == "":
			        FileMat.close()
			        break
		        if data.count('#Reference labels (rows):')!=0:
			        ref = data.split(":")[-1].split(",")
		                out.append(ref)
        return out

def gen_confusionMatrix(csv_f,AllClass):
	"""
	
	IN:
		csv_f [list of list] : comes from confCoordinatesCSV function.
		AllClass [list of strings] : all class
	OUT : 
		confMat [numpy array] : generate a numpy array representing a confusion matrix
	"""
	NbClasses = len(AllClass)

	confMat = [[0]*NbClasses]*NbClasses
	confMat = np.asarray(confMat)
	row = 0
        AllClassLab = [int(i) for i in AllClass]
	for classRef in AllClassLab:
		flag = 0#in order to manage the case "this reference label was never classified"
		for classRef_csv in csv_f:
		 	if classRef_csv[0] == classRef:
				col = 0
				for classProd in AllClassLab:
					classProd_csv = classRef_csv[1]
					if classProd_csv[0] == classProd:
						confMat[row][col] = confMat[row][col] + classProd_csv[1]
					col+=1
				#row +=1
		row+=1
		#if flag == 0:
			#row+=1

	return confMat

def computeKappa(confMat):

	nbrGood = confMat.trace()
	nbrSample = confMat.sum()

	overallAccuracy  = float(nbrGood) / float(nbrSample)

	## the lucky rate.
	luckyRate = 0.
	for i in range(0, confMat.shape[0]):
		sum_ij = 0.
       		sum_ji = 0.
        	for j in range(0, confMat.shape[0]):
         		sum_ij += confMat[i][j]
                	sum_ji += confMat[j][i]
        	luckyRate += sum_ij * sum_ji

	# Kappa.
	if float((nbrSample*nbrSample)-luckyRate) != 0:
		kappa = float((overallAccuracy*nbrSample*nbrSample)-luckyRate)/float((nbrSample*nbrSample)-luckyRate)
	else :
		kappa = 1000

	return kappa

def computeOverallAccuracy(confMat):
        nbrGood = confMat.trace()
	nbrSample = confMat.sum()
	overallAccuracy  = float(nbrGood) / float(nbrSample)
        return overallAccuracy

def computeOverallAccuracyStats(csvPaths):
        i=0
        av=0.0
        std=0.0
        oas=[]
        for path in csvPaths:
                allClass = parseRefLabels([path])[0]
                confmat = gen_confusionMatrix(parseConfusionMatrices([path]),allClass)
                oas.append(computeOverallAccuracy(confmat))
        if len(oas) > 1:
                for oa in oas:
                        av+=oa
                av/=len(oas)
                for oa in oas:
                        std+=(av-oa)**2
                std=np.sqrt(std)
                std/=(len(oas)-1)
                return (av,std)
        else:
                return (oas[0],0.0)
        
def computeKappaStats(csvPaths):
        i=0
        av=0.0
        std=0.0
        oas=[]
        for path in csvPaths:
                allClass = parseRefLabels([path])[0]
                confmat = gen_confusionMatrix(parseConfusionMatrices([path]),allClass)
                oas.append(computeKappa(confmat))
        if len(oas) > 1:
                for oa in oas:
                        av+=oa
                av/=len(oas)
                for oa in oas:
                        std+=(av-oa)**2
                std=np.sqrt(std)
                std/=(len(oas)-1)
                return (av,std)
        else:
                return (oas[0],0.0)
        
def computePreByClass(confMat,AllClass):
	Pre = []#[(class,Pre),(...),()...()]

	for i in range(len(AllClass)):
		denom = 0
		for j in range(len(AllClass)):
			denom += confMat[j][i]
			if i == j:
				nom = confMat[j][i]
		if denom != 0:
			currentPre = float(nom)/float(denom)
		else :
			currentPre = 0.
		Pre.append((AllClass[i],currentPre))
	return Pre

def computeRecByClass(confMat,AllClass):
	Rec = []#[(class,rec),(...),()...()]
	for i in range(len(AllClass)):
		denom = 0
		for j in range(len(AllClass)):
			denom += confMat[i][j]
			if i == j:
				nom = confMat[i][j]
		if denom != 0 :
			currentRec = float(nom)/float(denom)
		else:
			currentRec = 0.
		Rec.append((AllClass[i],currentRec))
	return Rec

def computeFsByClass(Pre,Rec,AllClass):
	Fs = []
	for i in range(len(AllClass)):
		if float(Rec[i][1]+Pre[i][1]) != 0:
			Fs.append((AllClass[i],float(2*Rec[i][1]*Pre[i][1])/float(Rec[i][1]+Pre[i][1])))
		else:
			Fs.append((AllClass[i],0.0))
	return Fs

def writeResults(confMat,Fs,Rec,Pre,kappa,overallAccuracy,AllClass,pathOut):

       	allC = ""
	for i in range(len(AllClass)):
		if i<len(AllClass)-1:
			allC = allC+str(AllClass[i])+" "
		else:
			allC = allC+str(AllClass[i])
	csvFile = open(pathOut,"w")
	csvFile.write("#Reference labels (rows):"+allC+"\n")
	csvFile.write("#Produced labels (columns):"+allC+"\n")
	for i in range(len(confMat)):
		for j in range(len(confMat[i])):
			if j < len(confMat[i])-1:
				csvFile.write(str(confMat[i][j])+" ")
			else:
				csvFile.write(str(confMat[i][j])+"\n")
        csvFile.write("\n")
	for i in range(len(AllClass)):
		csvFile.write("Precision of class ["+str(AllClass[i])+"] vs all: "+str(Pre[i][1])+"\n")
		csvFile.write("Recall of class ["+str(AllClass[i])+"] vs all: "+str(Rec[i][1])+"\n")
		csvFile.write("F-score of class ["+str(AllClass[i])+"] vs all: "+str(Fs[i][1])+"\n\n")

	csvFile.write("Precision of the different classes: [")
	for i in range(len(AllClass)):
		if i < len(AllClass)-1:
			csvFile.write(str(Pre[i][1])+",")
		else:
			csvFile.write(str(Pre[i][1])+"]\n")
	csvFile.write("Recall of the different classes: [")
	for i in range(len(AllClass)):
		if i < len(AllClass)-1:
			csvFile.write(str(Rec[i][1])+",")
		else:
			csvFile.write(str(Rec[i][1])+"]\n")
	csvFile.write("F-score of the different classes: [")
	for i in range(len(AllClass)):
		if i < len(AllClass)-1:
			csvFile.write(str(Fs[i][1])+",")
		else:
			csvFile.write(str(Fs[i][1])+"]\n\n")
	csvFile.write("Kappa index: "+str(kappa[0])+"\n")
        csvFile.write("Kappa std: "+str(kappa[1])+"\n")
	csvFile.write("Overall accuracy index: "+str(overallAccuracy[0])+"\n")
        csvFile.write("Overall accuracy std: "+str(overallAccuracy[1]))
	csvFile.close()

def fuseVarImp(csvPaths,pathOut):
        FileMat = open(csvPaths[0],"r")
	data = FileMat.readline().rstrip('\n\r').split(" ")[:-1]
        arr=np.zeros((len(csvPaths),len(data)))
        for i,csvPath in enumerate(csvPaths):
                FileMat = open(csvPath,"r")
		data = FileMat.readline().rstrip('\n\r').split(" ")[:-1]
	        for j,d in enumerate(data):
                        arr[i,j]=float(d)
        outMean=np.mean(arr,axis=0)
        outStd=np.std(arr,axis=0)
        csvFile = open(pathOut,"w")
        for n in outMean.tolist():
                csvFile.write(str(n)+" ")
        csvFile.write("\n")
        for n in outStd.tolist():
                csvFile.write(str(n)+" ")
        csvFile.write("\n")

if __name__ == "__main__":

        parser = argparse.ArgumentParser(description = "This function merges confusion matrices or variable importance vectors from different runs")
	parser.add_argument("-il",nargs="+", help ="input list of .csv files",dest = "csvPaths",required=True)
	parser.add_argument("-out",help="Output path for result file", dest="pathOut",required=True)
	parser.add_argument("-t",help="Type of data [conf/varimp] (default is conf)", dest="t",required=True, default ="conf")
	args = parser.parse_args()

        if args.t == "confmat":
                allClass = parseRefLabels(args.csvPaths)[0]
                confmat = gen_confusionMatrix(parseConfusionMatrices(args.csvPaths),allClass)
                confmat = np.multiply(confmat,1/float(len(args.csvPaths)))
                OA = computeOverallAccuracyStats(args.csvPaths)
                kappa = computeKappaStats(args.csvPaths)
                Rec = computeRecByClass(confmat,allClass)
                Pre = computePreByClass(confmat,allClass)
                Fs = computeFsByClass(Pre,Rec,allClass)
                writeResults(confmat,Fs,Rec,Pre,kappa,OA,allClass,args.pathOut)
        elif args.t == "varimp":
                fuseVarImp(args.csvPaths,args.pathOut)
        else:
                print "Unknown option "+args.t

