""" Perform analysis on cleaned data. """

import csv
import numpy as np
from sklearn import linear_model, preprocessing


# Input data
reader = csv.reader(open("zipcode_2015_train_matrix.csv","rb"), delimiter=",") 

# Extract X, y from csv
raw_data = np.array(list(reader)).astype('float')
_, cols = raw_data.shape
y = raw_data[:, cols-1]  
X = raw_data[:, 0:cols-1]  # Remove output y from X
X = X[:, :4]        # Remove time distribution of crimes data

# Standardize data
X = preprocessing.scale(X)

# Linear reagression
reg = linear_model.LinearRegression()
reg.fit(X, y)
w_reg = reg.coef_

# Ridge regression
ridge_reg = linear_model.Ridge( alpha = 0.5 )
ridge_reg.fit(X, y)
w_ridge_reg = ridge_reg.coef_

# Ridge regression with CV
ridge_reg_cv = linear_model.RidgeCV( alphas = [0.2, 0.5, 1, 10, 20] )
ridge_reg_cv.fit(X, y)
w_ridge_reg_cv = ridge_reg_cv.coef_
print(ridge_reg_cv.alpha_)

# Display results

# Init
np.set_printoptions(precision=3) # Reduce precision for displaying w
threshold = 10**-2               # Remove 0 valued parameters

# Threshold data
w_reg = w_reg*(w_reg>threshold)
w_ridge_reg = w_ridge_reg*(w_ridge_reg>threshold)
w_ridge_reg_cv = w_ridge_reg_cv*(w_ridge_reg_cv>threshold)


# Display model
print( "Model w_reg is          {}".format(w_reg) )
print( "Model w_ridge_reg is    {}".format(w_ridge_reg) )
print( "Model w_ridge_reg_cv is {}".format(w_ridge_reg_cv) )


