import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
import statsmodels.stats as stats
import seaborn as sns
import statsmodels.formula.api as smf
import numpy as np


data = pd.read_csv("https://onlinecourses.science.psu.edu/stat501/sites/onlinecourses.science.psu.edu.stat501/files/data/wordrecall.txt",sep='\t',  lineterminator='\n')
data.head()
data_x=pd.DataFrame(data.time)
type(data_x)
data_y=pd.DataFrame(data.prop)
plt.plot(data.time,data.prop)
regr=linear_model.LinearRegression()
fitres=regr.fit(data_x,data_y)

#plot to see the linearity
sns.residplot(x="time",y="prop",data=data, lowess=True, color="g")
sns.lmplot(x="time",y="prop",data=data)
sns.pairplot(data)

lm = smf.ols(formula="time~prop",data=data).fit()
print(lm.summary())

#residual Plot
plt.figure()
lm.resid.plot.density()
plt.show()
print('Residual mean:', np.mean(lm.resid))
influence=lm.get_influence()   
resid_student=influence.resid_studentized_external
(cooks, p) = influence.cooks_distance
(dffits, p) = influence.dffits
leverage = influence.hat_matrix_diag 
sns.regplot(leverage, lm.resid_pearson,  fit_reg=False)

