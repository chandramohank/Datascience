import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

n_alphas = 200
alphas = np.logspace(-10, -2, n_alphas)
diabetes = datasets.load_diabetes()
# Use only one feature
diabetes_X = diabetes.data[:, np.newaxis, 2]
# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]
# Split the targets into training/testing sets
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

regr = linear_model.RidgeCV(alphas)
regr.fit(diabetes_X_train,diabetes_y_train)
    # Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X_test)
    # The coefficients
print('Coefficients: \n', regr.coef_)
print('Coefficients: \n', regr.alpha_)
    # The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
    
    
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))
plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

np.logspace(2.0, 3.0, num=4)
np.ones(10)
