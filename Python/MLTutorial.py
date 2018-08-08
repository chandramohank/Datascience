#Predict Price

import numpy as np
import pandas as pd
import sys,os
import seaborn as sns
import matplotlib.pyplot as plt
from dateutil.parser import parse

melbourne_file_path = "C:\\Learning\\MachineLearning\\Melbourne housing\\Melbourne_housing_FULL.csv"
melbourne_data = pd.read_csv(melbourne_file_path)

##Data Exploration
melbourne_data.describe()
melbourne_data.head()
melbourne_data.index
len(melbourne_data.index)
melbourne_data.columns
melbourne_data.shape
melbourne_data.dtypes

 melbourne_data.isna().any()
 melbourne_data.isnull().sum()


#PostCode VS Price
sns.boxplot(melbourne_data.Postcode,melbourne_data.Price) 

 
cor_matrix= melbourne_data.corr() 
cor_matrix["Price"].sort_values(ascending=False)

#Handle Missing Values
# Since Building area has most missing values (more than 70 % we are going to drop this column)
plt.scatter(x=melbourne_data.BuildingArea,y=melbourne_data.Price)
plt.scatter(x=melbourne_data.Landsize,y=melbourne_data.Price)
plt.scatter(x=melbourne_data.Distance,y=melbourne_data.Price)
plt.scatter(x=melbourne_data.YearBuilt,y=melbourne_data.Price)

melbourne_data["YearBuilt"]


SData = melbourne_data.copy()
SData["Year"]=pd.DatetimeIndex(melbourne_data["Date"],dayfirst=True).year
SData["Month"]=pd.DatetimeIndex(melbourne_data["Date"],dayfirst=True).month
sns.boxplot(SData.Year,SData.Price) 
sns.boxplot(SData.Month,SData.Price)

sns.boxplot(SData.Rooms,SData.Price)
sns.boxplot(SData.Year,SData.Rooms)

sns.boxplot(SData.Month,SData.Rooms)

SData["YearBuilt"].fillna(SData["YearBuilt"].mean())

sns.pairplot(SData.dropna(),vars=["Price","Rooms","Bedroom2","Bathroom","Car","YearBuilt"])
#From the above analysis we can drop YearBuilt as well

numVars = SData.select_dtypes(include=[np.number]).columns

catVars = [col for col in SData.columns if col not in numVars]



#Feature Selection


 

