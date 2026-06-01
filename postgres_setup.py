import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

print("Connecting to the database...")
#Connect to out Postgres SQL database by creating a sqlalchemy engine
engine = create_engine(os.getenv("DB"))

print("Loading CSV data...")
df = pd.read_csv('cloud_kitchen_orders.csv')

print('Creating Tables...')

with engine.connect() as conn:
    #Drop existing tables to start fresh
    conn.execute(text('DROP TABLE IF EXISTS "Order_Details" CASCADE;'))
    conn.execute(text("DROP TABLE IF EXISTS \"Orders\" CASCADE;"))

    #Create the order tables
    conn.execute(text('''
        CREATE TABLE "Orders"(
            order_id VARCHAR(50) PRIMARY KEY,
            timestamp TIMESTAMP,
            day_of_week VARCHAR(15),
            is_weekend INTEGER,
            weather VARCHAR(50),
            location VARCHAR(100)
            )
    '''))

    #Create the details table
    conn.execute(text('''
        CREATE TABLE "Order_Details"(
            detail_id SERIAL PRIMARY KEY,
            order_id VARCHAR(50) REFERENCES "Orders"(order_id),
            item_name VARCHAR(100),
            quantity INTEGER,
            item_price NUMERIC(10, 2),
            total_price NUMERIC(10, 2)
            )
    '''))

    #Commit changes to the db
    conn.commit()

# Insert the data
orders_df = df[['order_id','timestamp','day_of_week','is_weekend','weather','location']]
orders_df.to_sql('Orders', engine, if_exists='append', index=False)

# Extract and insert Order Details
details_df = df[['order_id', 'item_name', 'quantity', 'item_price', 'total_price']]
details_df.to_sql('Order_Details', engine, if_exists='append', index=False)

print("Success! Data is securely loaded into PostgreSQL.")
