


## libraries
library(tiff)
library(raster)
library(rgdal)

## extraction
file_names=list.files('')#tiff names

substr(file_names, 1, 3)

shp_polygon <- shapefile('/run/media/pageot/ADATA HD650/THESE/CLASSIFICATION/TRAITEMENT/DT_CACG/DT_CACG_2017_WGS84.shp') #import shape
means=matrix(NA,ncol =length(file_names),nrow=length(shp_polygon$ID))


for(t in 1:(length(file_names))){
 
  
  tif<-raster(paste('C:/Users/Taeken/Desktop/base/',file_names, sep = "")) #import tiff
  extracted_data <- extract(tif,shp_polygon)#extract
  
  ## serie temp moyenne
  for(i in 1:length(extracted_data)){
    a=extracted_data[i]
    a=as.numeric(as.character(unlist(a[[1]])))
    means[i,t]=mean(a,na.rm = TRUE)
    
  }}

