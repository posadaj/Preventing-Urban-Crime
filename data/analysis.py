""" Perform analysis on cleaned data. """

import csv, numpy

# Input data
reader = csv.reader(open("zipcode_2015_train_matrix.csv","rb"), delimiter=",") 
X_list = list(reader)
X=numpy.array(X_list).astype('float')


"""
# Linear reagression
from sklearn import linear_model
reg = linear_model.LinearRegression()
reg.fit(X, y)
w = reg.coef_
print( "Model w is {}".format(w) )
"""
