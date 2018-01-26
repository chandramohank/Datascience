import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
h1bData = pd.read_csv("D:/Documents/Datascience/SAMPLEUSERDATA20161002/h1b_kaggle.csv")

#1. Is the number of petitions with Data Engineer job title increasing over time?
#2. Which part of the US has the most Hardware Engineer jobs?
#3. Which industry has the most number of Data Scientist positions? 
#4. Which employers file the most petitions each year?

h1bData.shape
h1bData.describe()
h1bData.isnull().any()
h1bData.isnull().sum()
h1bData.head()
#1. Is the number of petitions with Data Engineer job title increasing over time?

datEngineers =h1bData[h1bData["JOB_TITLE"]=="DATA ENGINEER"]
#datEngineers.groupby(['YEAR']).count().plot(kind="bar")
g = sns.countplot("YEAR",hue="JOB_TITLE", data=datEngineers)
ax=g.axes
for p in ax.patches:
   ax.annotate(format(p.get_height()),(p.get_x()+0.10,p.get_height()+0.25))              
               # plot data
fig, ax = plt.subplots(figsize=(15,7))
# use unstack()
h1bData.groupby(['YEAR','JOB_TITLE']).count().unstack().plot.bar(width=0.8,color='#f45c42')
               
#2. Which part of the US has the most Hardware Engineer jobs?

hardwareEngineers=h1bData[h1bData["JOB_TITLE"]=="HARDWARE ENGINEER"]
hardwareEngineers['WORKSITE'].value_counts()[:10].plot.bar(width=0.8,color='#f45c42')
#g = sns.countplot("WORKSITE", data=hardwareEngineers,order = hardwareEngineers['WORKSITE'].value_counts().index)
#for p in ax.patches:
#   ax.annotate(format(p.get_height()),(p.get_x()+0.10,p.get_height()+0.25))     

#3. Which industry has the most number of Data Scientist positions? 

dataScientists=h1bData[h1bData["JOB_TITLE"]=="DATA SCIENTIST"]

dataScientists["SOC_NAME"].value_counts()[:10].plot.barh(width=0.8,color='#f45c42')
#4. Which employers file the most petitions each year?
                  
certifiedEmployers=h1bData[h1bData[h1bData["CASE_STATUS"]=="CERTIFIED"].notnull()]    
certifiedEmployers["EMPLOYER_NAME"].value_counts()[:10].plot.barh(width=0.8,color='#f45c42')
certifiedEmployers[certifiedEmployers.EMPLOYER_NAME.notnull()].EMPLOYER_NAME.str.startswith("INFO")
test=certifiedEmployers[ certifiedEmployers["EMPLOYER_NAME"] like '%VALUE%']
                 

