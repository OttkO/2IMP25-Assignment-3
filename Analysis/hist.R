normalizeHist <- function(inVector, breaks) {
  myhist <- hist(inVector, breaks = breaks)
  multiplier <- myhist$counts / myhist$density
  mydensity <- density(inVector)
  mydensity$y <- mydensity$y * multiplier[1]
  
  plot(myhist)
  lines(mydensity)
}

augmentWithPoliteness <- function(rawData, titlePol, titleImp, bodyPol, bodyImp) {
  rawData$PoliteTitleCategory<-"Neutral"
  
  rawData$PoliteTitleCategory[rawData$PoliteTitle >= titlePol]<-"Polite"
  rawData$PoliteTitleCategory[rawData$PoliteTitle <= titleImp]<-"Impolite"
  
  rawData$PoliteBodyCategory<-"Neutral"
  rawData$PoliteBodyCategory[rawData$PoliteBody >= bodyPol]<-"Polite"
  rawData$PoliteBodyCategory[rawData$PoliteBody <= bodyImp]<-"Impolite"
  
  rawData$PoliteBodyCategory = as.factor(rawData$PoliteBodyCategory)
  rawData$PoliteTitleCategory = as.factor(rawData$PoliteTitleCategory)
  
  rawData
}

politeness = factor(c("Polite", "Neutral", "Impolite"))

doKruskalAndWilc <- function(soData) {
  kruskal.test(soData$ViewCount~soData$PoliteBodyCategory)
  wilcox.test(soData$Score[soData$PoliteBodyCategory=="Neutral"], soData$Score[soData$PoliteBodyCategory=="Impolite"], conf.int=T, paired=F)
}