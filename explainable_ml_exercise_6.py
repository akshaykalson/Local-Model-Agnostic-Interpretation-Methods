# -*- coding: utf-8 -*-
"""Explainable ML_exercise 6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zu2g4N_2RyTmuElA2lT02fZfQTBORi9q
"""

# Import necessary libraries

!pip install shap
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
import shap
import matplotlib.pyplot as plt
import numpy as np


# Read the chocolate data from flavors_of_cacao_2.csv
chocolate_data = pd.read_csv('flavors_of_cacao_new.csv')

# Rename the column to remove the newline character
chocolate_data.rename(columns={'Cocoa\nPercent': 'Cocoa Percent'}, inplace=True)

# Remove '%' symbol and convert 'Cocoa Percent' values to float
chocolate_data['Cocoa Percent'] = chocolate_data['Cocoa Percent'].str.rstrip('%').astype('float') / 100.0

# Encode categorical data using OneHotEncoder
# Assume 'Company' is a categorical column
categorical_columns = ['Company', 'bar_location', 'company_location', 'bean_type', 'country_of_bean_origin']
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
transformers = [('encoder', encoder, categorical_columns)]
preprocessor = ColumnTransformer(transformers, remainder='passthrough')

# Define the output: y>=3.5 -> y=1 else y=0
chocolate_data['Rating'] = chocolate_data['Rating'].apply(lambda x: 1 if x >= 3.5 else 0)

# Split the data into features (X) and target variable (y)
X = chocolate_data.drop(['Rating'], axis=1)
y = chocolate_data['Rating']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess the data using the defined transformer
X_train_preprocessed = preprocessor.fit_transform(X_train)
X_test_preprocessed = preprocessor.transform(X_test)

# Create the SVM model
svm_mdl = RandomForestClassifier(random_state=42)  # Use RandomForest as a surrogate model

# Fit the surrogate model on the training data
svm_mdl.fit(X_train_preprocessed, y_train)

# Make predictions on the training and testing data
y_train_pred = svm_mdl.predict(X_train_preprocessed)
y_test_pred = svm_mdl.predict(X_test_preprocessed)

# Print the mean_squared_error of train and test data
mse_train = mean_squared_error(y_train, y_train_pred)
mse_test = mean_squared_error(y_test, y_test_pred)
print(f"Mean Squared Error (Train): {mse_train}")
print(f"Mean Squared Error (Test): {mse_test}")

# Summarize the training data using k-means
# Assuming you want to cluster the X_train data into 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_train_preprocessed)

# Initialize your explainer using the surrogate model
explainer = shap.Explainer(svm_mdl, X_train_preprocessed, feature_names=preprocessor.get_feature_names_out())


# Assuming you have already defined and fitted the transformer on the training data
# preprocessor = ...

# Preprocess the entire test set using the defined transformer
X_test_preprocessed = preprocessor.transform(X_test)

# ... (previous code)

# Assuming you have already defined and fitted the transformer on the training data
# preprocessor = ...

# Preprocess the entire test set using the defined transformer
X_test_preprocessed = preprocessor.transform(X_test)

# Compute the SHAP values for the entire test set
shap_values = explainer.shap_values(X_test_preprocessed, check_additivity=False)

# Create a summary plot for the entire test set
shap.summary_plot(shap_values[1], X_test_preprocessed, feature_names=preprocessor.get_feature_names_out(), show=True)



# Assuming your dataset is a Pandas DataFrame named df
index_6_data = X.iloc[6, :]
print(index_6_data)