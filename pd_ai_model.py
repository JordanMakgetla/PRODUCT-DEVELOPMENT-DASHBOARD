# -*- coding: utf-8 -*-
"""PD AI MODEL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1btnEL_WG2Ll1PTid7W1L9tYRuvKu4Inh
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset (replace the path if necessary)
df = pd.read_csv('large_product_sales_data.csv')

# Convert Date to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# 1. Extract Job Requests & Interactions (Analyzing interactions)
def interaction_summary(df):
    interaction_data = df.groupby('InteractionType').agg(
        total_interactions=('InteractionType', 'count'),
        conversion_rate=('Converted', 'mean')
    ).reset_index()
    return interaction_data

interaction_data = interaction_summary(df)
print("Interaction Summary:")
print(interaction_data)

# 2. Generate Statistical Summaries of the Data
def data_summary(df):
    return df.describe()

summary = data_summary(df)
print("\nStatistical Summary:")
print(summary)

# 3. Predictive Analytics (Forecasting Sales)
def predict_sales(df):
    # Prepare the data: Predict QuantitySold based on ProductType and MarketingStrategy
    df['ProductType'] = pd.Categorical(df['ProductType']).codes
    df['MarketingStrategy'] = pd.Categorical(df['MarketingStrategy']).codes
    X = df[['ProductType', 'MarketingStrategy']]  # Features
    y = df['QuantitySold']  # Target

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a simple linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

        # Forecast future sales (predict on test set)
    y_pred = model.predict(X_test)

    return model, X_test, y_test, y_pred

# Train the model and forecast sales
model, X_test, y_test, y_pred = predict_sales(df)
print("\nSales Forecasting Results:")
for i in range(len(y_pred)):
    print(f"Predicted: {y_pred[i]}, Actual: {y_test.iloc[i]}")

# Plot predicted vs actual sales
plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual Sales')
plt.scatter(range(len(y_pred)), y_pred, color='red', label='Predicted Sales')
plt.xlabel('Test Data Index')
plt.ylabel('Quantity Sold')
plt.legend()
plt.show()

# 4. Anomaly Detection
def detect_anomalies(df):
    # Use Isolation Forest for anomaly detection
    model = IsolationForest(contamination=0.1)  # Contamination is the proportion of anomalies
    df['Anomaly'] = model.fit_predict(df[['QuantitySold']])

    # Convert the anomaly output (-1 for anomaly, 1 for normal)
    df['Anomaly'] = df['Anomaly'].map({-1: True, 1: False})

    return df

# Detect anomalies in the dataset
df_with_anomalies = detect_anomalies(df)
print("\nDataset with Anomalies Detected:")
print(df_with_anomalies)

# Show the rows with anomalies
anomalies = df_with_anomalies[df_with_anomalies['Anomaly'] == True]
print("\nAnomalies:")
print(anomalies)







