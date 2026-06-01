import streamlit as st
import pandas as pd
import joblib

# setup the page
st.set_page_config(page_title='Cloud Kitchen AI', page_icon= '🍜', layout='centered')

st.title = 'Cloud Kitchen Demand Forecaster'
st.markdown("""
Welcome to the AI demand forecaster. Set parameters bellow to predict
specific quantity of food required for a specific hour
""")

# Load the saved model and keep it in the cache memory for fast performance

@st.cache_resource
def load_model():
    return joblib.load('cloud_kitchen_model.pkl')

model = load_model()

st.divider()

# 3. Create the User Interface (Inputs)
st.subheader("Set the Scenario")

# Create two columns to make the UI look clean
col1, col2 = st.columns(2)

with col1:
    # Dropdown for the item
    selected_item = st.selectbox(
        "Menu Item",
        ["Chicken Biryani", "Chicken Bharta", "Paneer Butter Masala", "Rumali Roti", "Cold Drink"]
    )
    
    # Dropdown for the weather
    selected_weather = st.selectbox(
        "Weather Condition",
        ["Sunny", "Clear", "Overcast", "Raining"]
    )

with col2:
    # Slider for the time of day (11 AM to 11 PM)
    selected_hour = st.slider("Time of Day (Hour)", min_value=11, max_value=23, value=19)
    
    # Toggle for Weekend vs Weekday
    is_weekend_toggle = st.radio("Day Type", ["Weekday", "Weekend"])
    
# Convert the user's toggle choice into the 0 or 1 that the model expects
is_weekend_numeric = 1 if is_weekend_toggle == "Weekend" else 0

st.divider()

# 4. Make the Prediction
# We package the user's inputs into a DataFrame, exactly how we did in the training script
input_data = pd.DataFrame({
    'hour': [selected_hour],
    'is_weekend': [is_weekend_numeric],
    'weather': [selected_weather],
    'item_name': [selected_item]
})

# 5. Display the Results
# We create a big, bold button to trigger the AI
if st.button("Predict Demand", type="primary"):
    with st.spinner("AI is calculating..."):
        # The model predicts the value
        prediction = model.predict(input_data)
        
        # We round the prediction to the nearest whole number (you can't make 3.4 rotis)
        final_demand = int(round(prediction[0]))
        
        # Display the result beautifully
        st.success("Prediction Complete!")
        st.metric(
            label=f"Predicted Demand for {selected_item}", 
            value=f"{final_demand} Portions"
        )
        
        st.caption(f"Scenario: {selected_weather} | Hour: {selected_hour}:00 | {is_weekend_toggle}")