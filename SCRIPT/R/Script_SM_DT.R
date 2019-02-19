library(stringr)
####TRAITEMENT DATA ADOUR####
setwd("/run/media/pageot/ADATA HD650/THESE/CLASSIFICATION/TRAITEMENT/SM_DT_STAT_ZONAL/DT_ADOUR_SM2017/")#on se place dans ce dossier
vec_fichiers = list.files(path=".", pattern=".csv")#on en liste les fichiers d'extension .csv
date=str_split(vec_fichiers,"DT_ADOUR", simplify= TRUE)
date=str_split(date[,2],".csv",simplify = TRUE)
date=as.vector(date[,1],mode = "any")
###LECTUE des fichers 

longueur_matrix=464
largeur_matrix=0
All_stat_mean=matrix(0,longueur_matrix,largeur_matrix)
for(i in 1:length(vec_fichiers)){
  contenu_fichier = read.csv(vec_fichiers[i],sep = ",",dec=".")
   All_stat_mean=cbind(All_stat_mean,contenu_fichier[,c(10,15:16)],stringsAsFactors =FALSE)
   OS_stat=All_stat_mean[1]
   selcol=grep("X_mean",names(All_stat_mean))
   All_stat_mean= subset(All_stat_mean,select = selcol)
   All_stat_mean= cbind(OS_stat,All_stat_mean)
}
# EN COURS
# for (i in 1:length(date)){
#   colnames(All_stat_mean)=paste0("mean",date[i])
#   
# }
#   

# date=c(date,OS_stat)
# All_stat_mean=rbind(date,All_stat_mean)

colnames(All_stat_mean)=c("DT_ADOUR","mean20170412","mean20170424","mean20170430",
                     "mean20170506","mean20170512","mean20170518",
                     "mean20170605","mean20170611","mean20170617",
                     "mean20170623","mean20170629","mean20170705",
                     "mean20170711","mean20170723","mean20170729",
                     "mean20170804","mean20170816","mean20170828") 

View (All_stat)
write.csv(All_stat_mean,"/run/media/pageot/ADATA HD650/THESE/CLASSIFICATION/TRAITEMENT/SM_DT_STAT_ZONAL/STAT_2017_AD.csv")
STAT_2017_AD=read.csv("/run/media/pageot/ADATA HD650/THESE/CLASSIFICATION/TRAITEMENT/SM_DT_STAT_ZONAL/STAT_2017_AD.csv", h=TRUE, sep=",", dec=".",stringsAsFactors = FALSE)
View (STAT_2017_AD)
STAT_2017_AD=na.omit(STAT_2017_AD)
STAT_2017_AD=STAT_2017_AD[-296,]##PROBLM INTROduction NA car entités sur zone sans data

#Préparation du jeux de données
SOJ=grep("SOJ",STAT_2017_AD$DT_ADOUR)
MIS=grep("MIS",STAT_2017_AD$DT_ADOUR)
MISAD2017=data.frame(STAT_2017_AD[MIS,c(2:20)])

MISNIRADOUR_ME17=data.frame(STAT_2017_AD[STAT_2017_AD$DT_ADOUR=="MISNIRR",c(2:20)])
MISADOUR_ME17 = data.frame(STAT_2017_AD[STAT_2017_AD$DT_ADOUR=="MISIRR",c(2:20)])
# MISNIRADOUR_SD17=data.frame(STAT_2017_AD[STAT_2017_AD$DT_ADOUR=="MISNIRR",c(2,4,6,8,10,12,14,16,18,20)])
# MISADOUR_SD17=data.frame(STAT_2017_AD[STAT_2017_AD$DT_ADOUR=="MISIRR",c(2,4,6,8,10,12,14,16,18,20)])
# SOJNIRADOUR_ME17=data.frame(STAT_2017_AD[STAT_2017_AD$DT_ADOUR=="SOJNIRR",c(2,3,5,7,9,11,13,15,17,19,21)])
# SOJADOUR_ME17 = data.frame(STAT_2017_AD[STAT_2017_AD$DT_ADOUR=="SOJIRR",c(2,3,5,7,9,11,13,15,17,19,21)])


MAISA_2017= apply(MISADOUR_ME17[,2:19],2,mean)
MAISNAD_2017=apply(MISNIRADOUR_ME17[,2:19],2,mean)
# MAISA_SD2017=apply(MISADOUR_SD17[,2:10],2,mean)
# MAISNAD_SD2017=apply(MISNIRADOUR_SD17 [,2:10],2,mean)
# SOJAIRA_2017=apply(SOJADOUR_ME17[,2:10],2,mean)
# SOJANIRRA_2017=apply(SOJNIRADOUR_ME17[,2:10],2,mean)

TEMPS=c(1:366)
TEMPSDD=c(102,114,120,126,132,138,156,162,168,174,180,186,192,204,210,216,220,240)
TEMPSD=c("2017/04/12","2017/04/24","2017/04/30",
         "2017/05/06","2017/05/12","2017/05/18",
         "2017/06/05","2017/06/11","2017/06/17",
         "2017/06/23","2017/06/29","2017/07/05",
         "2017/07/11","2017/07/23","2017/07/29",
         "2017/08/04","2017/08/16","2017/08/28")

##ALL PARCELLES##/
plot(TEMPS[1:18],SOJADOUR_ME17[3:20],type="l",ylim=c(0,200))
for (i in 2:137){lines(as.character(SOJADOUR_ME17[i,2:10]),type = "l",col="black")
  for (j in 1:200){lines(as.character(SOJNIRADOUR_ME17[j,2:10]),type="l",col="red")
  } 
}
###SOJA##
plot(TEMPS[1:18],SOJAIRA_2017,type="l",col="blue",ylim=c(0,200))
lines(as.character(SOJANIRRA_2017,type="l"))
##MAIS##
# plot(TEMPS[1:18],MAISA_2017,type="l",ylim=c(0,250),col="blue",xlab="date",ylab="soil moisture")
# lines(as.character(MAISNAD_2017,type="l",col="green"))
# points(MAISA_2017,col="blue",pch=16)
# points(MAISNAD_2017,col="black",pch = 16)

plot(TEMPSDD,MAISA_2017,pch=16,col ="blue",ylim=c(0,250))
points(TEMPSDD,MAISNAD_2017,pch=16,col="black")
lines(TEMPSDD,MAISA_2017,col="blue")
lines(TEMPSDD,MAISNAD_2017,col="black")
legend(x="bottomright",legend=c("MAIS Irrguées","MAIS Non Irriguées"),col=c("blue","black"),pch=16)
dev.print(png,filename="Specte_SM_MAIS_2017_AD.png", width=7, height=7,units="in",res = 600)

####BOXPLOT MAIS###

TEST=subset(STAT_2017_AD,select= 3:20)
##BOUCLE POUR LES BOXPLOT
for (i in 1:18){
  boxplot(TEST[,i][MIS]~STAT_2017_AD$DT_ADOUR[MIS],ylim=c(0,200),col=c("blue","green"))
  legend(x="bottomleft",legend = paste0("date = ",colnames(TEST[i])))
   dev.print(png,filename=paste0("SM_AD",colnames(TEST[i]),".png"), width=7, height=7,units="in",res = 600)
}

####TRAITEMENT DATA TARN####
setwd("/run/media/pageot/ADATA HD650/THESE/CLASSIFICATION/TRAITEMENT/SM_DT_STAT_ZONAL/DT_TARN_SM2017/")#on se place dans ce dossier
vec_fichiers = list.files(path=".", pattern=".csv")#on en liste les fichiers d'extension .csv
date=str_split(vec_fichiers,"DT_TARN", simplify= TRUE)
date=str_split(date[,2],".csv",simplify = TRUE)
date=as.vector(date[,1],mode = "any")

longueur_matrix=
largeur_matrix=0
All_stat_mean_TARN=matrix(0,longueur_matrix,largeur_matrix)
for(i in 1:length(vec_fichiers)){
  contenu_fichier = read.csv(vec_fichiers[i],sep = ",",dec=".")
  All_stat_mean_TARN=cbind(All_stat_mean_TARN,contenu_fichier[,c(10,15:16)],stringsAsFactors =FALSE)
  OS_stat=All_stat_mean_TARN[1]
  selcol=grep("X_mean",names(All_stat_mean_TARN))
  All_stat_mean_TARN= subset(All_stat_mean_TARN,select = selcol)
  All_stat_mean_TARN= cbind(OS_stat,All_stat_mean_TARN)
}








###ECAT TYEP####
lines(rep(TEMPS[1],2),c((MAISA_2017[1]+MAISA_SD2017[1]),(MAISA_2017[1]-MAISA_SD2017[1])))
lines(c(TEMPS[1]-0.1,TEMPS[1]+0.1),c((MAISA_2017[1]+MAISA_SD2017[1]),(MAISA_2017[1]+MAISA_SD2017[1])))
lines(c(TEMPS[1]-0.1,TEMPS[1]+0.1),c((MAISA_2017[1]-MAISA_SD2017[1]),(MAISA_2017[1]-MAISA_SD2017[1])))
lines(rep(TEMPS[2],2),c((MAISA_2017[2]+MAISA_SD2017[2]),(MAISA_2017[2]-MAISA_SD2017[2])))
lines(c(TEMPS[2]-0.1,TEMPS[2]+0.1),c((MAISA_2017[2]+MAISA_SD2017[2]),(MAISA_2017[2]+MAISA_SD2017[2])))
lines(c(TEMPS[2]-0.1,TEMPS[2]+0.1),c((MAISA_2017[2]-MAISA_SD2017[2]),(MAISA_2017[2]-MAISA_SD2017[2])))
lines(rep(TEMPS[3],2),c((MAISA_2017[3]+MAISA_SD2017[3]),(MAISA_2017[3]-MAISA_SD2017[3])))
lines(c(TEMPS[3]-0.1,TEMPS[3]+0.1),c((MAISA_2017[3]+MAISA_SD2017[3]),(MAISA_2017[3]+MAISA_SD2017[3])))
lines(c(TEMPS[3]-0.1,TEMPS[3]+0.1),c((MAISA_2017[3]-MAISA_SD2017[3]),(MAISA_2017[3]-MAISA_SD2017[3])))
lines(rep(TEMPS[4],2),c((MAISA_2017[4]+MAISA_SD2017[4]),(MAISA_2017[4]-MAISA_SD2017[4])))
lines(c(TEMPS[4]-0.1,TEMPS[4]+0.1),c((MAISA_2017[4]+MAISA_SD2017[4]),(MAISA_2017[4]+MAISA_SD2017[4])))
lines(c(TEMPS[4]-0.1,TEMPS[4]+0.1),c((MAISA_2017[4]-MAISA_SD2017[4]),(MAISA_2017[4]-MAISA_SD2017[4])))
lines(rep(TEMPS[5],2),c((MAISA_2017[5]+MAISA_SD2017[5]),(MAISA_2017[5]-MAISA_SD2017[5])))
lines(c(TEMPS[5]-0.1,TEMPS[5]+0.1),c((MAISA_2017[5]+MAISA_SD2017[5]),(MAISA_2017[5]+MAISA_SD2017[5])))
lines(c(TEMPS[5]-0.1,TEMPS[5]+0.1),c((MAISA_2017[5]-MAISA_SD2017[5]),(MAISA_2017[5]-MAISA_SD2017[5])))
lines(rep(TEMPS[6],2),c((MAISA_2017[6]+MAISA_SD2017[6]),(MAISA_2017[6]-MAISA_SD2017[6])))
lines(c(TEMPS[6]-0.1,TEMPS[6]+0.1),c((MAISA_2017[6]+MAISA_SD2017[6]),(MAISA_2017[6]+MAISA_SD2017[6])))
lines(c(TEMPS[6]-0.1,TEMPS[6]+0.1),c((MAISA_2017[6]-MAISA_SD2017[6]),(MAISA_2017[6]-MAISA_SD2017[6])))
lines(rep(TEMPS[7],2),c((MAISA_2017[7]+MAISA_SD2017[7]),(MAISA_2017[7]-MAISA_SD2017[7])))
lines(c(TEMPS[7]-0.1,TEMPS[7]+0.1),c((MAISA_2017[7]+MAISA_SD2017[7]),(MAISA_2017[7]+MAISA_SD2017[7])))
lines(c(TEMPS[7]-0.1,TEMPS[7]+0.1),c((MAISA_2017[7]-MAISA_SD2017[7]),(MAISA_2017[7]-MAISA_SD2017[7])))
lines(rep(TEMPS[8],2),c((MAISA_2017[8]+MAISA_SD2017[8]),(MAISA_2017[8]-MAISA_SD2017[8])))
lines(c(TEMPS[8]-0.1,TEMPS[8]+0.1),c((MAISA_2017[8]+MAISA_SD2017[8]),(MAISA_2017[8]+MAISA_SD2017[8])))
lines(c(TEMPS[8]-0.1,TEMPS[8]+0.1),c((MAISA_2017[8]-MAISA_SD2017[8]),(MAISA_2017[8]-MAISA_SD2017[8])))
lines(rep(TEMPS[9],2),c((MAISA_2017[9]+MAISA_SD2017[9]),(MAISA_2017[9]-MAISA_SD2017[9])))
lines(c(TEMPS[9]-0.1,TEMPS[9]+0.1),c((MAISA_2017[9]+MAISA_SD2017[9]),(MAISA_2017[9]+MAISA_SD2017[9])))
lines(c(TEMPS[9]-0.1,TEMPS[9]+0.1),c((MAISA_2017[9]-MAISA_SD2017[9]),(MAISA_2017[9]-MAISA_SD2017[9])))

lines(rep(TEMPS[1],2),c((MAISNAD_2017[1]+MAISNAD_SD2017[1]),(MAISNAD_2017[1]-MAISNAD_SD2017[1])))
lines(c(TEMPS[1]-0.1,TEMPS[1]+0.1),c((MAISNAD_2017[1]+MAISNAD_SD2017[1]),(MAISNAD_2017[1]+MAISNAD_SD2017[1])))
lines(c(TEMPS[1]-0.1,TEMPS[1]+0.1),c((MAISNAD_2017[1]-MAISNAD_SD2017[1]),(MAISNAD_2017[1]-MAISNAD_SD2017[1])))
lines(rep(TEMPS[2],2),c((MAISNAD_2017[2]+MAISNAD_SD2017[2]),(MAISNAD_2017[2]-MAISNAD_SD2017[2])))
lines(c(TEMPS[2]-0.1,TEMPS[2]+0.1),c((MAISNAD_2017[2]+MAISNAD_SD2017[2]),(MAISNAD_2017[2]+MAISNAD_SD2017[2])))
lines(c(TEMPS[2]-0.1,TEMPS[2]+0.1),c((MAISNAD_2017[2]-MAISNAD_SD2017[2]),(MAISNAD_2017[2]-MAISNAD_SD2017[2])))
lines(rep(TEMPS[3],2),c((MAISNAD_2017[3]+MAISNAD_SD2017[3]),(MAISNAD_2017[3]-MAISNAD_SD2017[3])))
lines(c(TEMPS[3]-0.1,TEMPS[3]+0.1),c((MAISNAD_2017[3]+MAISNAD_SD2017[3]),(MAISNAD_2017[3]+MAISNAD_SD2017[3])))
lines(c(TEMPS[3]-0.1,TEMPS[3]+0.1),c((MAISNAD_2017[3]-MAISNAD_SD2017[3]),(MAISNAD_2017[3]-MAISNAD_SD2017[3])))
lines(rep(TEMPS[4],2),c((MAISNAD_2017[4]+MAISNAD_SD2017[4]),(MAISNAD_2017[4]-MAISNAD_SD2017[4])))
lines(c(TEMPS[4]-0.1,TEMPS[4]+0.1),c((MAISNAD_2017[4]+MAISNAD_SD2017[4]),(MAISNAD_2017[4]+MAISNAD_SD2017[4])))
lines(c(TEMPS[4]-0.1,TEMPS[4]+0.1),c((MAISNAD_2017[4]-MAISNAD_SD2017[4]),(MAISNAD_2017[4]-MAISNAD_SD2017[4])))
lines(rep(TEMPS[5],2),c((MAISNAD_2017[5]+MAISNAD_SD2017[5]),(MAISNAD_2017[5]-MAISNAD_SD2017[5])))
lines(c(TEMPS[5]-0.1,TEMPS[5]+0.1),c((MAISNAD_2017[5]+MAISNAD_SD2017[5]),(MAISNAD_2017[5]+MAISNAD_SD2017[5])))
lines(c(TEMPS[5]-0.1,TEMPS[5]+0.1),c((MAISNAD_2017[5]-MAISNAD_SD2017[5]),(MAISNAD_2017[5]-MAISNAD_SD2017[5])))
lines(rep(TEMPS[6],2),c((MAISNAD_2017[6]+MAISNAD_SD2017[6]),(MAISNAD_2017[6]-MAISNAD_SD2017[6])))
lines(c(TEMPS[6]-0.1,TEMPS[6]+0.1),c((MAISNAD_2017[6]+MAISNAD_SD2017[6]),(MAISNAD_2017[6]+MAISNAD_SD2017[6])))
lines(c(TEMPS[6]-0.1,TEMPS[6]+0.1),c((MAISNAD_2017[6]-MAISNAD_SD2017[6]),(MAISNAD_2017[6]-MAISNAD_SD2017[6])))
lines(rep(TEMPS[7],2),c((MAISNAD_2017[7]+MAISNAD_SD2017[7]),(MAISNAD_2017[7]-MAISNAD_SD2017[7])))
lines(c(TEMPS[7]-0.1,TEMPS[7]+0.1),c((MAISNAD_2017[7]+MAISNAD_SD2017[7]),(MAISNAD_2017[7]+MAISNAD_SD2017[7])))
lines(c(TEMPS[7]-0.1,TEMPS[7]+0.1),c((MAISNAD_2017[7]-MAISNAD_SD2017[7]),(MAISNAD_2017[7]-MAISNAD_SD2017[7])))
lines(rep(TEMPS[8],2),c((MAISNAD_2017[8]+MAISNAD_SD2017[8]),(MAISNAD_2017[8]-MAISNAD_SD2017[8])))
lines(c(TEMPS[8]-0.1,TEMPS[8]+0.1),c((MAISNAD_2017[8]+MAISNAD_SD2017[8]),(MAISNAD_2017[8]+MAISNAD_SD2017[8])))
lines(c(TEMPS[8]-0.1,TEMPS[8]+0.1),c((MAISNAD_2017[8]-MAISNAD_SD2017[8]),(MAISNAD_2017[8]-MAISNAD_SD2017[8])))
lines(rep(TEMPS[9],2),c((MAISNAD_2017[9]+MAISNAD_SD2017[9]),(MAISNAD_2017[9]-MAISNAD_SD2017[9])))
lines(c(TEMPS[9]-0.1,TEMPS[9]+0.1),c((MAISNAD_2017[9]+MAISNAD_SD2017[9]),(MAISNAD_2017[9]+MAISNAD_SD2017[9])))
lines(c(TEMPS[9]-0.1,TEMPS[9]+0.1),c((MAISNAD_2017[9]-MAISNAD_SD2017[9]),(MAISNAD_2017[9]-MAISNAD_SD2017[9])))




