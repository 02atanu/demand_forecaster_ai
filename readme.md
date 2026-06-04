# 🍜 Cloud Kitchen Demand Forecaster

[[Streamlit App] <-- Click Here!](https://ai-forcaster.streamlit.app/)

## 📌 The Business Problem
In the high volume cloud kitchen industry (especially in tech hubs like Bangalore), predicting inventory is a constant battle. Prep too little, and you lose revenue to stockouts during a dinner rush. Prep too much, and profits are eaten alive by food waste. 

This project is an **end-to-end data pipeline and machine learning model** designed to predict the exact hourly inventory needs for a local restaurant network based on weather, time of day, day of the week, and location.

## 🛠️ System Architecture & Tech Stack
This project moves from raw logic simulation to a production-grade database, and finally into a predictive front-end application.

* **Data Simulation:** `Python`, `NumPy`
* **Relational Database:** `PostgreSQL`, `SQLAlchemy`
* **Machine Learning:** `Scikit-Learn` (Random Forest Regressor, Pipelines, OneHotEncoding), `Pandas`
* **Front-End Web App:** `Streamlit`, `Pandas`

**Data Flow:**
`Mock Data Generator` ➔ `PostgreSQL Normalized Tables` ➔ `SQL JOINs & Aggregation` ➔ `Scikit-Learn Model (.pkl)` ➔ `Streamlit UI`

## 🧠 Engineering Decisions & Machine Learning

### 1. Database Normalization (PostgreSQL)
Instead of feeding flat CSV files directly into a Pandas dataframe, the simulated data (13,000+ orders) was normalized into two strictly typed SQL tables: `Orders` (metadata) and `Order_Details` (financials/items). Aggregation for the ML model was handled using raw SQL `JOIN` and `GROUP BY` queries to mimic efficient, production-level database querying.

### 2. Model Selection: Random Forest
A `RandomForestRegressor` was chosen over basic Linear Regression because human behavior isn't linear. The impact of a rainstorm on delivery volumes at 7 PM is vastly different than at 9 AM, and decision trees natively capture these intersecting conditional rules. The model uses a Scikit-Learn `Pipeline` and `ColumnTransformer` to handle dynamic categorical encoding seamlessly.

### 3. Model Performance & Feature Engineering Lessons
* **Baseline Model (Time + Weather):** Achieved a **Mean Absolute Error (MAE) of 3.13** and an **$R^2$ of 0.49**. In the context of restaurant prep, an MAE of ~3 items per hour is highly operational, actively preventing major stockouts while keeping waste minimal. The 0.49 $R^2$ reflects the heavy baseline randomness of human hunger.
* **The "Failed" Experiment (Adding Location):** I attempted to make the model hyper-local by adding delivery zones (Indiranagar, Koramangala, etc.). 
    * *The Result:* The MAE mathematically improved to **1.73**, but the $R^2$ score plummeted to **-0.07**. 
    * *The Lesson:* Because the mock delivery locations were generated using pure random distributions without a built-in volume weight, there was zero actual correlation between location and demand. The model tried to memorize this noise during training and failed on the test set. It was a perfect, real-world lesson: **you cannot force a model to learn a signal that doesn't exist.** It highlighted the dangers of overfitting and the importance of checking multiple metrics, not just MAE.


