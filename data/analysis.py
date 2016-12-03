""" Perform analysis on cleaned data. """

import csv
import numpy as np
from sklearn import linear_model, preprocessing, metrics


# Input data
reader = csv.reader(open("zipcode_2015_train_matrix.csv","rb"), delimiter=",") 

# Extract X, y from data
raw_data = np.array(list(reader)).astype('float')
_, cols = raw_data.shape

# Standardize data
X = preprocessing.scale(raw_data)
y = X[:, cols-1]  
X = X[:, 0:cols-1]  # Remove output y from X

# Only consider certain features
#X = X[:, :4]        # Remove time distribution of crimes data
#X = X[:, 4:]

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

# Lasso
reg_lasso = linear_model.Lasso( alpha = 1 )
reg_lasso.fit(X, y)
w_lasso = reg_lasso.coef_

# Display results

# Init
np.set_printoptions(precision=3) # Reduce precision for displaying w
"""
threshold = 10**-3               # Remove 0 valued parameters

# Threshold data

w_reg = w_reg*(w_reg>threshold)
w_ridge_reg = w_ridge_reg*(w_ridge_reg>threshold)
w_ridge_reg_cv = w_ridge_reg_cv*(w_ridge_reg_cv>threshold)
"""


# Display model
print( "Model w_reg is          {}".format(w_reg) )
print( "Model w_ridge_reg is    {}".format(w_ridge_reg) )
print( "Model w_ridge_reg_cv is {}".format(w_ridge_reg_cv) )
print( "Model w_lasso is        {}".format(w_lasso) )



# Calculate E_in
score_cv = metrics.mean_absolute_error(y, np.dot(X, w_ridge_reg_cv) ) 

# Dispaly E_in
print( "Model w_ridge_reg_cv E_in: {}".format(score_cv) )
print( np.dot(X, w_ridge_reg_cv) )

