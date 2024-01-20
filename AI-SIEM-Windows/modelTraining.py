import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import IsolationForest

# Load captured packets data
captured_packets_df = pd.read_csv('captured_packets.csv')

# Assuming you don't have a specific target column for supervised learning
captured_packets_features = captured_packets_df[['timestamp', 'source', 'destination', 'protocol', 'length']]

# Define preprocessing steps
numeric_features = ['length']
categorical_features = ['protocol']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Combine preprocessing with a model (use your actual anomaly detection model here)
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', IsolationForest(contamination='auto'))
])

# Train the model
model.fit(captured_packets_features)

# Predict anomalies in the training set
captured_packets_pred = model.predict(captured_packets_features)

# Print details of anomalies
anomalies_indices = captured_packets_pred == -1
anomalies_details = captured_packets_df[anomalies_indices]

print("Details of Anomalies:")
print(anomalies_details)
