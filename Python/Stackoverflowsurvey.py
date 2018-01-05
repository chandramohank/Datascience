#https://www.kaggle.com/ash316/the-stack-survey
#https://www.kaggle.com/stackoverflow/so-survey-2017/kernels

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
surveyData = pd.read_csv("C:/Users/chandramohan/Downloads/survey_results_public.csv")
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
