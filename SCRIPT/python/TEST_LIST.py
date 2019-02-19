import os

a="EMP1.txt"
b="EMP2"
a2="/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/CARTES_SOIL_MOISTURE/Fp1_S1a/EMP1.txt"
b2="/datalocal/vboxshare/THESE/CLASSIFICATION/DONNES_SIG/CARTES_SOIL_MOISTURE/Fp2_S1a/EMP2"
#split("\n")

listdownload=open(a2,"r").read().split("\n")
listtrait=open(b2,"r").read().split("\n")
down=[]
work=[]
for d in listdownload:
	d=os.path.basename(d)
	d=''.join(d)
	d=d.replace ('.zip',"")
	down.append (d)
	#print d
for la in listtrait:### permet de supprimer les extensions des files 
	la=os.path.basename(la)
	la=''.join(la)
	la=la.replace ('.dim',"")
	work.append(la)## permet d'ecrit le resualt de la boucle dans une varaible de sorite defini plus haut.

	
file1=set(down)
file2=set(work)

result=file1.union(file2) - file1.intersection(file2)# permet de comparer les deux files et connaitre les manques
resualt=list(result)## converti la varaible set en list

print ("\n".join(resualt))# Ajoute un retour ligne 
