import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Create a dictionary of food name and prices
menu_itmes = {'Biriyani': 260,
              'Aloo Paratha': 30,
              'Chicken Bharta': 250,
              'Fish Finger': 70,
              'Momo': 120,
              'Cold Drink': 60}

# Creating list for weather conditions and locations
weather_conditions = ['Sunny', 'Clear', 'Overcast', 'Raining']
locations = ['Koramangala', 'HSR Layout', 'Indraninagar', 'Whitefield']

start_date = datetime.now() - timedelta(days=90) #Creating a startng point for our data

data = [] #Initialized the emptly list that'll eventually hold all the order dictionaries

counter_order_id = 100001

for day_offset in range(120):
    current_date = start_date + timedelta(days=day_offset)
    is_weekend = 1 if current_date.weekday() >= 5 else 0

    #Generating weather and volume patterns
    daily_weather = random.choices(weather_conditions, weights = [40, 30, 20, 10])[0] #Gets random weather conditiona and outputs the string value dur to the 0 index in the end
    base_orders = random.randint(180, 300) if is_weekend else random.randint(80, 150) #Generates random base order count for weekends and weekdays

    if daily_weather == 'Raining': #if the weather is rainy we increase the order count by 40%
        base_orders = int(base_orders * 1.4)

    #Now we create a loop that runs for every single order(number of base orders)
    for _ in range(base_orders):
        #We generate random time for every order
        hour = random.choices(list(range(11, 24)), weights=[1, 1, 3, 3, 1, 1, 1, 2, 4, 4, 4, 2, 1])[0]
        minute = random.randint(0, 59)
        order_time = current_date.replace(hour=hour, minute=minute, second=0)

        item = random.choice(list(menu_itmes.keys()))
        quantity = random.randint(1,4)

        #Rainy weather increase the chance of the order being biriyani
        if daily_weather == 'Raining' and  random.random() > 0.5:
            item = 'Biriyani'

        # Lets assemble the orders
        data.append({
            'order_id': f'ORD{counter_order_id}',
            'timestamp': order_time,
            'day_of_week': current_date.strftime('%A'),
            'is_weekend' : is_weekend,
            'weather' : daily_weather,
            'location': random.choice(locations),
            'item_name': item,
            'quantity': quantity,
            'item_price': menu_itmes[item],
            'total_price': menu_itmes[item] * quantity
        })

        counter_order_id += 1

# exporting data
df = pd.DataFrame(data)
df.to_csv('cloud_kitchen_orders.csv', index=False)





        
        


