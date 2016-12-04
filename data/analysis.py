""" Perform analysis on cleaned data. """

import csv, sys
import numpy as np
from sklearn import linear_model, preprocessing, metrics


def main( fname ):
    # Input data
    reader = csv.reader( open(fname,"rb"), delimiter="," ) 

    # Extract X, y from data
    raw_data = np.array(list(reader)).astype('float')
    _, cols = raw_data.shape

    # Standardize data
    X = preprocessing.scale(raw_data)
    y = X[:, cols-1]  
    X = X[:, 0:cols-1]  # Remove output y from X

    # Only consider certain features
    added_features = 4
    X = X[:, :added_features]        # Remove time distribution columns
    #X = X[:, added_features:]        # Only show time distribution columns

    # Linear reagression
    reg = linear_model.LinearRegression()
    reg.fit(X, y)
    w_reg = reg.coef_

    # Ridge regression with CV
    ridge_reg_cv = linear_model.RidgeCV( alphas = [0.2, 0.5, 1, 10, 20] )
    ridge_reg_cv.fit(X, y)
    w_ridge_reg_cv = ridge_reg_cv.coef_

    # Lasso
    # TODO: Cross-validation
    reg_lasso = linear_model.Lasso( alpha = 1 )
    reg_lasso.fit(X, y)
    w_lasso = reg_lasso.coef_

    # Display results

    # Init
    np.set_printoptions(precision=3) # Reduce precision for displaying w

    """
    # Threshold data
    threshold = 10**-3               # Remove 0 valued parameters
    w_reg = w_reg*(w_reg>threshold)
    w_ridge_reg_cv = w_ridge_reg_cv*(w_ridge_reg_cv>threshold)
    """

    # Display model
    print( "Model w_reg is          {}".format(w_reg) )
    print( "Model w_ridge_reg_cv is {}".format(w_ridge_reg_cv) )
    print( "Model w_lasso is        {}".format(w_lasso) )


    # Read y_test to evaluate models
    reader   = csv.reader(open("zipcode_2015_test_matrix.csv","rb"), delimiter=",")
    raw_data = np.array(list(reader)).astype('float')
    _, cols  = raw_data.shape
    y_test   = raw_data[:,cols-1]

    # Display stats for error
    score_reg_in  = metrics.mean_absolute_error(y, np.dot(X, w_reg) ) 
    score_reg_out = metrics.mean_absolute_error(y_test, np.dot(X, w_reg) ) 

    score_rr_cv_in  = metrics.mean_absolute_error(y, np.dot(X, w_ridge_reg_cv) ) 
    score_rr_cv_out = metrics.mean_absolute_error(y_test, np.dot(X, w_ridge_reg_cv) )

    score_lasso_in  = metrics.mean_absolute_error(y, np.dot(X, w_lasso) ) 
    score_lasso_out = metrics.mean_absolute_error(y_test, np.dot(X, w_lasso) ) 

    # Dispaly E_in
    print( "\n{}\t {}\t {}\t".format("Model", "E_in", "E_out") )
    print( "regression  {}  {}".format( score_reg_in, score_reg_out ) )
    print( "ridge_reg_cv  {}  {}".format( score_rr_cv_in, score_rr_cv_out ) )
    print( "lasso  {}  {}".format( score_lasso_in, score_lasso_out ) )

if __name__ == '__main__':
    # Perform analysis on training data set

    # Program expects a filename to perform analysis
    if len(sys.argv) != 2:
        print("Error: Incorrect input")
        sys.exit()

    # Extract filename
    fname = sys.argv[1]
    print("Filename is "+fname)
    main( fname )