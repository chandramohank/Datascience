import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
import statsmodels.stats as stats
import seaborn as sns
import statsmodels.formula.api as smf

data = pd.read_csv("https://onlinecourses.science.psu.edu/stat501/sites/onlinecourses.science.psu.edu.stat501/files/data/wordrecall.txt",sep='\t',  lineterminator='\n')
data.head()
data_x=pd.DataFrame(data.time)
type(data_x)
data_y=pd.DataFrame(data.prop)
plt.plot(data.time,data.prop)
regr=linear_model.LinearRegression()
fitres=regr.fit(data_x,data_y)
visualizaer=ResidualsPlot(regr)
visualizaer.fit(data_x,data_y)

plt.plot(data_y,fitres._residues)
fitres.fit

sns.pairplot(data)
lm = smf.ols(formula="time~prop",data=data).fit()
print(lm.summary())

influence=lm.get_influence()   
resid_student=influence.resid_studentized_external
(cooks, p) = influence.cooks_distance
(dffits, p) = influence.dffits
leverage = influence.hat_matrix_diag 
sns.regplot(leverage, lm.resid_pearson,  fit_reg=False)
