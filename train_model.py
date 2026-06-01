import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from dotenv import load_dotenv
import os
import joblib

load_dotenv()

# Connect to Database
print("1. Connecting to PostgreSQL...")
engine = create_engine(os.getenv('DB'))

# SQL Aggregation
print('2. Fetching and aggregating data...')

query = ("""
SELECT 
    EXTRACT(HOUR FROM o.timestamp) as hour,
    o.is_weekend,
    o.weather,
    d.item_name,
    SUM(d.quantity) as total_demand
FROM "Orders" o
JOIN "Order_Details" d ON o.order_id = d.order_id
GROUP BY 
    DATE(o.timestamp), 
    EXTRACT(HOUR FROM o.timestamp), 
    o.is_weekend, 
    o.weather, 
    d.item_name
""")

# Load into the pandas
df = pd.read_sql(query, engine)

print(f"Aggregated down to {len(df)} hourly demand records.")

# --Feature Engieering--
print("3. Preprocessing Data...")

# Define Features (X) and our Target (y)
X = df[['hour', 'is_weekend', 'weather', 'item_name']]
y = df['total_demand']
# Split into Training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=47)

# Use OneHotEncoder to convert data into binary columns
categorical_features = ['weather', 'item_name']
catagorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Telling script to apply column transformer only to columns weather and item name
preprocessor = ColumnTransformer(transformers=[('cat', catagorical_transformer, categorical_features)], remainder='passthrough')

# - Model Training
print('4. Training the Random forest model...')

#Create a pipeline to convert preprocessing and modelling into a singel step
model_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', RandomForestRegressor(n_estimators=100, random_state=47))])

# Train the model
model_pipeline.fit(X_train, y_train)

# - Evaluate model performance
prediction = model_pipeline.predict(X_test)

# calculate the accuracy
mae = mean_absolute_error(y_test, prediction)
r2 = r2_score(y_test, prediction)

print('-'*33)
print(f'Mean absoulute error: {mae:.2f}')
print(f'Model R squared: {r2:.2f}')
print('-'*33)

# Making a live prediction:
print('-----------Live Prediction test-----------')
target_df = pd.DataFrame({
    'hour': [19], # 7 PM
    'is_weekend': [1], # Saturday
    'weather': ['Raining'],
    'item_name': ['Biryani']
})

demand_prediction = model_pipeline.predict(target_df)
print(f'Predicted Demand for Biriyani on a Rainy Saturday at 7PM: {int(demand_prediction[0])} quantity')

##-- Saving the model as .pkl file
print('Model ready for deployment...')

joblib.dump(model_pipeline, 'cloud_kitchen_model.pkl')

print('Success the model is saved successfully!')


