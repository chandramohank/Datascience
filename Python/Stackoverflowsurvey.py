#https://www.kaggle.com/ash316/the-stack-survey
#https://www.kaggle.com/stackoverflow/so-survey-2017/kernels

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def index_exists(ls, i):
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)

#surveyData = pd.read_csv("C:/Users/chandramohan/Downloads/survey_results_public.csv")
surveyData = pd.read_csv("E:/DataScience/Practice/Datascience/Python/stack-overflow-developer-survey-2017/survey_results_public.csv")
surveyData.head()
surveyData.shape
surveyData.columns

totals = []

width = 0.35
fig, ax = plt.subplots()
 
surveyData['Country'].value_counts()[:10].plot.bar(width=0.8,color='#f45c42')
for p in ax.patches:
    ax.annotate(format(p.get_height()),(p.get_x()+0.10,p.get_height()+0.25))
plt.xlabel('Country')
plt.ylabel('Count')
plt.show()

plt.subplots(figsize=(12,6))
students = surveyData[surveyData['Professional']=='Student']
ax=students['Country'].value_counts()[:10].plot.bar(width=0.8,color='#f45c42')
for p in ax.patches:
    ax.annotate(format(p.get_height()),(p.get_x()+0.10,p.get_height()+0.25))
    
#Most famous languages among students
    d=[]
    lst=[]
    students['HaveWorkedLanguage'].apply(lambda x:d.extend(str(x).split('; ')))
    lst=list(set(d))
    
    dict={}
    for i in lst:
        counts=students['HaveWorkedLanguage'].apply(lambda x: 'java' in str(x).split(';')).value_counts()
        if index_exists(counts,1):
            dict[i]=counts[1]
            
            
    del dict['nan']
    lang=pd.DataFrame(list(dict.items()))
    
    lang.columns=[['Language','Count']]
    lang= lang.sort_values(by=['Language'],ascending=[False])  
    plt.subplots(figsize=(12,6))
    #lang.set_index('Language',inplace=True)   
ax=    lang.sort_values(by=['Count'],ascending=[False]).head(10).plot.bar(width=0.8,color='#005544')
for p in ax.patches:
    ax.annotate(format(p.get_height()),(p.get_x()+0.10,p.get_height()+0.25))

    
