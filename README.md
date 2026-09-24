# Predictive Microeconomic Forecasting Using Open Financial Data and AI-Driven Insights

## 📌 Project Overview

**Predictive Microeconomic Forecasting Using Open Financial Data and AI-Driven Insights** is a full-stack predictive analytics system designed to help businesses understand financial and economic factors that may affect their business performance.

The system combines **financial data, business information, location-based factors, machine learning, and time-series forecasting** to generate predictions and insights related to revenue, expenses, profit, demand, inflation, and business conditions.

The project is developed using **Python Flask as the backend**, machine learning models for prediction, **SQLite for data storage**, and **JavaScript-based visualizations** for presenting financial and location-based insights.

---

## 🎯 Objectives

* Analyze financial and business-related data.
* Forecast future financial trends using machine learning.
* Predict expected revenue, expenses, and profit.
* Analyze inflation and demand trends using time-series forecasting.
* Consider location-based factors in business analysis.
* Store business inputs and prediction results in a database.
* Provide understandable data-driven insights to support business planning.

---

## 🚀 Key Features

### 1. Business Data Analysis

Users can provide business-related information such as:

* Business type
* Investment/budget
* Business goals
* Latitude
* Longitude

### 2. Financial Forecasting

The system analyzes business inputs and predicts:

* Expected Revenue
* Expected Expenses
* Expected Profit
* Business financial trends

### 3. Demand Analysis

Business type, budget, and location-related factors are considered to estimate potential demand.

### 4. Inflation Forecasting

Historical financial data is analyzed using time-series forecasting to estimate future inflation trends.

### 5. Location-Based Analysis

Latitude and longitude are used to incorporate location-related factors into business analysis and visualization.

### 6. Database Management

Business information and prediction results are stored using **SQLite**.

### 7. Interactive Visualization

Forecasting and location-related results can be represented using:

* Chart.js
* Leaflet

### 8. AI-Driven Insights

The system converts prediction results into understandable business insights such as:

* Financial outlook
* Expense-related factors
* Demand conditions
* Potential business risks

---

## 🛠️ Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS

### Machine Learning

* Scikit-learn
* Regression Models
* Time-Series Forecasting
* Statsmodels

### Database

* SQLite

### Visualization

* Chart.js
* Leaflet

### Data Processing

* Pandas
* NumPy

---

## 🏗️ System Architecture

```text
                User
                  │
                  ▼
        ┌──────────────────┐
        │    Frontend      │
        │ HTML/CSS/JS      │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │   Flask Backend  │
        │   Python         │
        └────────┬─────────┘
                 │
        ┌────────┼─────────┐
        ▼        ▼         ▼
   ┌────────┐ ┌────────┐ ┌──────────────┐
   │Database│ │   ML   │ │ Time-Series  │
   │ SQLite │ │Models  │ │ Forecasting  │
   └────────┘ └────────┘ └──────────────┘
        │        │         │
        └────────┼─────────┘
                 ▼
        ┌──────────────────┐
        │ Predictions &    │
        │ AI-Driven        │
        │ Insights         │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Charts & Maps    │
        │ Chart.js/Leaflet │
        └──────────────────┘
```

---

## 📂 Project Structure

```text
predictive-microeconomic-forecasting/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── schema.sql
│   │
│   ├── ml/
│   │   ├── regression_model.py
│   │   ├── time_series_model.py
│   │   ├── demand_model.py
│   │   └── location_logic.py
│   │
│   └── data/
│       └── sample_financial_data.csv
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/predictive-microeconomic-forecasting.git
```

### 2. Open the Project

```bash
cd predictive-microeconomic-forecasting
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 6. Run the Flask Application

```bash
cd backend
python app.py
```

The backend will run locally at:

```text
http://127.0.0.1:5000
```

---

## 🔌 Backend Endpoints

| Endpoint              | Method | Purpose                                 |
| --------------------- | ------ | --------------------------------------- |
| `/predict`            | POST   | Generate business financial predictions |
| `/inflation-forecast` | GET    | Generate inflation forecast             |
| `/history`            | GET    | Retrieve stored prediction history      |

---

## 📊 Example Prediction Flow

```text
Business Information
        ↓
Location Information
        ↓
Financial & Economic Analysis
        ↓
Demand Estimation
        ↓
ML Prediction
        ↓
Revenue / Expenses / Profit
        ↓
Time-Series Forecasting
        ↓
Inflation & Demand Trends
        ↓
AI-Driven Business Insights
```

---

## 🧠 Machine Learning Approach

The project uses machine learning and statistical forecasting techniques for different prediction tasks.

### Regression

Regression is used to estimate financial values such as:

* Revenue
* Expenses
* Profit

based on business-related input factors.

### Time-Series Forecasting

Historical financial data is used to identify trends and forecast future values such as inflation.

---

## 🗄️ Database

The system uses **SQLite** to store:

* Business information
* Location information
* Budget
* Business goals
* Predicted revenue
* Predicted expenses
* Predicted profit
* Prediction timestamps

---

## 🔐 Data & Privacy

The project is designed to run locally and does not require external financial APIs.

Sample/open financial data can be used for development and demonstration purposes.

Do not commit passwords, API keys, `.env` files, or other sensitive information to the repository.

---

## 🔮 Future Enhancements

* Integration with verified open financial datasets.
* More advanced forecasting models.
* Business-specific prediction models.
* Improved location-based economic analysis.
* Model performance comparison using MAE, RMSE, and R².
* Real-time financial data integration.
* Advanced business risk analysis.
* Deployment as a cloud-based application.

---

## 🎓 Academic Project

This project is developed as a **Final Year Project** demonstrating the integration of:

**Web Development + Backend Development + Database Management + Machine Learning + Time-Series Forecasting + Data Visualization**

---

## 👩‍💻 Author

**Abhinaya B**



