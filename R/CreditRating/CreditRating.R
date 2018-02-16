#https://rstudio-pubs-static.s3.amazonaws.com/225209_df0130c5a0614790b6365676b9372c07.html
#https://ocw.mit.edu/courses/sloan-school-of-management/15-062-data-mining-spring-2003/assignments/GermanCredit.pdf
#install.packages("DT")
#install.packages("knitr")
#install.packages("Information")
#install.packages("ClustOfVar")
#install.packages("ape")
#install.packages("caret")
library(DT)
library(knitr) 
library(Information) 
library(ClustOfVar) 
library(ape)
library(caret)
library(stats)

source("E:/DataScience/Practice/Datascience/R/CreditRating/userdefinedfunctions.R")

cdata<-read.table("E:/DataScience/Practice/Datasets/german.data.txt", h=F, sep="")

#cdata<-read.table("D:/Documents/Datascience/Datasets/CreditRating/german.data.txt", h=F, sep="")

# Update column Names
colnames(cdata) <- c("chk_ac_status_1",
                     "duration_month_2", "credit_history_3", "purpose_4",
                     "credit_amount_5","savings_ac_bond_6","p_employment_since_7", 
                     "instalment_pct_8", "personal_status_9","other_debtors_or_grantors_10", 
                     "present_residence_since_11","property_type_12","age_in_yrs_13",
                     "other_instalment_type_14", "housing_type_15", 
                     "number_cards_this_bank_16","job_17","no_people_liable_for_mntnance_18",
                     "telephone_19", "foreign_worker_20", 
                     "good_bad_21")

# Read a numeric copy: Numeric data for Neural network & Lasso

cdatanum<-read.table("E:/DataScience/Practice/Datasets/german.data-numeric.txt", h=F, sep="") 
#cdatanum<-read.table("D:/Documents/Datascience/Datasets/CreditRating/german.data-numeric.txt", h=F, sep="") 
cdatanum <- as.data.frame(sapply(cdatanum, as.numeric ))

#cdata<-read.table("ftp://ftp.ics.uci.edu/pub/machine-learning-databases/statlog/german/german.data", h=F, sep="")

cdata$duration_month_2  <- as.numeric(cdata$duration_month_2)
cdata$credit_amount_5   <-  as.numeric(cdata$credit_amount_5 )
cdata$instalment_pct_8 <-  as.numeric(cdata$instalment_pct_8)
cdata$present_residence_since_11 <-  as.numeric(cdata$present_residence_since_11)
cdata$age_in_yrs_13        <-  as.numeric(cdata$age_in_yrs_13)
cdata$number_cards_this_bank_16    <-  as.numeric(cdata$number_cards_this_bank_16)
cdata$no_people_liable_for_mntnance_18 <-  as.numeric(cdata$no_people_liable_for_mntnance_18)

cdata$good_bad_21<-as.factor(ifelse(cdata$good_bad_21 == 1, "Good", "Bad"))
pct(cdata$good_bad_21)

cdata$good_bad_21<-as.numeric(ifelse(cdata$good_bad_21 == "Good", 0, 1))
IV <- Information::create_infotables(data=cdata, NULL, y="good_bad_21", 10)
IV$Summary$IV <- round(IV$Summary$IV*100,2)

IV$Tables

var_list_1 <- IV$Summary[IV$Summary$IV > 2,] # 15 variables
cdata_reduced_1 <- cdata[, c(var_list_1$Variable,"good_bad_21")] #16 variables

factors <- sapply(cdata_reduced_1,is.factor)
vars_quali <- cdata_reduced_1[,factors]
vars_quanti<-cdata_reduced_1[,!factors]

tree <- hclustvar(X.quanti = vars_quanti,X.quali = vars_quali[,c(-12)])
plot(tree, main="variable clustering")
rect.hclust(tree, k=10,  border = 1:10) # draw dendogram 
summary(tree)

summary.phylo(as.phylo(tree))
plot(as.phylo(tree),type = "fan",tip.color = hsv(runif(15, 0.65,  0.95), 1, 1, 0.7),
     edge.color = hsv(runif(10, 0.65, 0.75), 1, 1, 0.7), 
     edge.width = runif(20,  0.5, 3), use.edge.length = TRUE, col = "gray80")
  
stab<-stability(tree,B=50) 
boxplot(stab$matCR)

part<-cutreevar(tree,10)
print(part)
summary(part)

kfit<-kmeansvar(X.quanti = vars_quanti, X.quali = vars_quali[,-c(12)], init=10,
                iter.max = 150, nstart = 1, matsim = TRUE)
summary(kfit)

keep<- c(1:8,12,13,21)
cdata_reduced_2 <- cdata[,keep]
str(cdata_reduced_2)

div_part <- sort(sample(nrow(cdata_reduced_2), nrow(cdata_reduced_2)*.6))
train<-cdata_reduced_2[div_part,]
pct(train$good_bad_21)
test<-cdata_reduced_2[-div_part,] # rest of the 30% data goes here
pct(test$good_bad_21)
#Stratified Random Sampling

div_part_1 <- createDataPartition(y=cdata_reduced_2$good_bad_21, p = 0.7, list = F)
train_1 <- cdata_reduced_2[div_part_1,]
test_1 <- cdata_reduced_2[-div_part_1,] # rest of the 30% data goes here

# For neural network we would need contious data
# Sampling for Neural Network - It can be used for other modeling as well
div_part_2 <- createDataPartition(y = cdatanum[,25], p = 0.7, list = F)

# Training Sample for Neural Network
train_num <- cdatanum[div_part_2,] # 70% here

# Test Sample for Neural Network
test_num <- cdatanum[-div_part_2,] # rest of the 30% data goes here

m1 <- glm(good_bad_21~.,data=train_1,family=binomial())
m1 <- step(m1)
summary(m1)

