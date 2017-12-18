library(ggplot2)
#install.packages("mice")

library(mice)
#install.packages("VIM")
library(VIM)
#detach(loanData)
trainData<-read.csv("E:/DataScience/Practice/Loan Prediction/train_u6lujuX_CVtuZ9i.csv")

testdata<-read.csv("E:/DataScience/Practice/Loan Prediction/test_Y3wMUE5_7gLdaTN.csv")
dim(trainData)
dim(testdata)
str(trainData)
str(testdata)

testdata$Loan_Status<-"N"
loanData<-rbind(trainData,testdata)
dim(loanData)
str(loanData)
colSums(is.na(loanData))

levels(loanData$Gender)

md.pattern(loanData)
matrixplot(loanData)
nhanes_aggr = aggr(loanData, col=mdc(1:2), numbers=TRUE, sortVars=TRUE, labels=names(loanData), cex.axis=.7, gap=3, ylab=c("Proportion of missingness","Missingness Pattern"))
barMiss(loanData)

shadow<-as.data.frame(abs(is.na(loanData)))
miss.shadow<-shadow[,which(unlist(lapply(shadow,sum))!=0)]
round(cor(miss.shadow),3)

numericData<-loanData[is.numeric(loanData),]

nums <- sapply(loanData, is.numeric)
numericnames<-names(loanData[nums])


for(i in seq(3,length(numericnames),3))
{
  res<- round(cor(loanData[,numericnames[(i-3):3]],miss.shadow,use = "pairwise.complete.obs"),3)
  print(res)
  rm(res)
}

res<- round(cor(loanData[,tail(numericnames,3)],miss.shadow,use = "pairwise.complete.obs"),3)
print(res)
rm(res)
#there is no strong correlationcbetween missing values

#apply mice
imputeddata<-mice(miss.shadow,m=5,maxit = 50,method = "pmm",seed = 500)
completedData<-complete(imputeddata)

round(cor(loanData[is.numeric(loanData),],miss.shadow,use = "pairwise.complete.obs"),3)

ggplot(trainData,aes(x=Loan_Status))+geom_bar()+facet_grid(.~Gender)
+ggtitle("Loan Status by Gender of the applicant")
ggplot(trainData,aes(x=Loan_Status))+geom_bar()+facet_grid(.~Married)
+ggtitle("Loan Status by Married of the applicant")
ggplot(trainData,aes(x=Loan_Status))+geom_bar()+facet_grid(.~Dependents)
+ggtitle("Loan Status by Dependents of the applicant")
ggplot(trainData,aes(x=Loan_Status))+geom_bar()+facet_grid(Education~Dependents)
+ggtitle("Loan Status by Education of the applicant")
ggplot(trainData,aes(x=Loan_Status))+geom_bar()+facet_grid(.~Self_Employed)
+ggtitle("Loan Status by Gender of the applicant")


#filling Missing values
#Married
#check the income
ggplot(loanData[loanData$ApplicantIncome<20000,],aes(ApplicantIncome,fill=Married))+geom_bar(position = "dodge")
+facet_grid(Gender~.)

ggplot(loanData[loanData$ApplicantIncome<20000,],aes(CoapplicantIncome,fill=Married))+geom_bar(position = "dodge")
+facet_grid(Gender~.)

#impute marital status as "No" when the coapplicant income is zero, and "Yes", otherwise.

loanData$Married[is.na(loanData$Married) & loanData$CoapplicantIncome==0]<-"No"
loanData$Married[is.na(loanData$Married)]<- "Yes"

#Gender and dependents
loanData[is.na(loanData$Gender) & is.na(loanData$Dependents),]

loanData$Dependents[is.na(loanData$Dependents) & loanData$Married=="No"]<- "0"
#use rpart to predict the number of dependents 
#for this population, using applicant income,coapplicant income, loan amount, 
#loan term and property area as predcitors.
names(loanData)
mm <- loanData[(loanData$Gender=="Male" & loanData$Married=="Yes"),c(3,4,6:9,11)]
mmtrain<-mm[!is.na(mm$Dependents),]
mmtest<- mm[is.na(mm$Dependents),]
library(rpart)
#install.packages("rattle")
install.packages("RGtk2", depen=T)
install.packages("RGtk2")
library(rattle)
depFit <- rpart(data=mmtrain,Dependents~.,xval=3)
fancyRpartPlot(depFit)

p<-predict(depFit,mmtrain,type="class")

loanData$Dependents[is.na(loanData$Dependents) & loanData$Gender=="Male" & loanData$Married == "Yes"]<- predict(depFit,newdata=mmtest,type="class")

#Now for missing genders:
gtrain<-loanData[!is.na(loanData$Gender),2:8]
gtest<-loanData[is.na(loanData$Gender),2:8]
genFit<-rpart(data=gtrain,Gender~.,xval=3)

p<-predict(genFit,gtrain,type="class")
acc<-sum(p==gtrain[,1])/length(p)
acc
loanData$Gender[is.na(loanData$Gender)]<-predict(genFit,gtest,type="class")
loanData$Self_Employed[is.na(loanData$Self_Employed)] <- "No"
library(car)
loanData$Credit_History<-recode(loanData$Credit_History,"NA=2")
