import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
best_rand_for_trn = joblib.load('best_model.pkl')

# Define the expected columns for the model
model_columns = [
    'Gender_F', 'Gender_M', 'Profession_Commercial associate', 'Profession_Pensioner',
    'Profession_State servant', 'Profession_Working', 'Location_Rural',
    'Location_Semi-Urban', 'Location_Urban', 'Expense Type 1_N', 'Expense Type 1_Y',
    'Expense Type 2_N', 'Expense Type 2_Y', 'Has Active Credit Card_Active',
    'Has Active Credit Card_Inactive', 'Has Active Credit Card_Unpossessed',
    'Property Location_Rural', 'Property Location_Semi-Urban',
    'Property Location_Urban', 'Income Stability_High',
    'Income Stability_Low', 'Age', 'Income (USD)',
    'Loan Amount Request (USD)', 'Current Loan Expenses (USD)',
    'Dependents', 'Credit Score', 'No. of Defaults', 'Property Age',
    'Property Type', 'Co-Applicant', 'Property Price'
]

# Helper function for one-hot encoding
def one_hot_encode(value, prefix, all_categories):
    return {f"{prefix}_{category}": 1 if value == category else 0 for category in all_categories}

# Function to prepare the input and make prediction
def predict_loan_sanction_amount(gender, profession, location, expense_type_1, expense_type_2, 
                                 credit_card_status, property_location, income_stability, 
                                 age, income, loan_amount_request, current_loan_expenses, 
                                 dependents, credit_score, no_of_defaults, property_age, 
                                 property_type, co_applicant, property_price):
    
    # Initialize an empty dictionary for input data
    input_data = {col: 0 for col in model_columns}
    
    # Map categorical inputs to one-hot encoded format
    gender_mapping = {'Female': 'F', 'Male': 'M'}
    input_data.update(one_hot_encode(gender_mapping[gender], 'Gender', ['F', 'M']))
    input_data.update(one_hot_encode(profession, 'Profession', ['Commercial associate', 'Pensioner', 'State servant', 'Working']))
    input_data.update(one_hot_encode(location, 'Location', ['Rural', 'Semi-Urban', 'Urban']))
    input_data.update(one_hot_encode(expense_type_1, 'Expense Type 1', ['N', 'Y']))
    input_data.update(one_hot_encode(expense_type_2, 'Expense Type 2', ['N', 'Y']))
    input_data.update(one_hot_encode(credit_card_status, 'Has Active Credit Card', ['Active', 'Inactive', 'Unpossessed']))
    input_data.update(one_hot_encode(property_location, 'Property Location', ['Rural', 'Semi-Urban', 'Urban']))
    input_data.update(one_hot_encode(income_stability, 'Income Stability', ['High', 'Low']))
    
    # Map numerical inputs
    input_data['Age'] = age
    input_data['Income (USD)'] = income
    input_data['Loan Amount Request (USD)'] = loan_amount_request
    input_data['Current Loan Expenses (USD)'] = current_loan_expenses
    input_data['Dependents'] = dependents
    input_data['Credit Score'] = credit_score
    input_data['No. of Defaults'] = no_of_defaults
    input_data['Property Age'] = property_age
    input_data['Property Type'] = property_type
    input_data['Co-Applicant'] = co_applicant
    input_data['Property Price'] = property_price
    
    # Convert the dictionary to a DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Ensure the DataFrame has all the necessary columns
    input_df = input_df.reindex(columns=model_columns, fill_value=0)
    
    # Make the prediction
    predicted_amount = best_rand_for_trn.predict(input_df)
    
    return predicted_amount[0]

# Streamlit app
st.title("Predicting Loan Amount")

# Create inputs for the user
gender = st.radio("Select Gender", ('Female', 'Male'))
age = st.slider("Select Age", min_value=18, max_value=65, value=30)
income_stability = st.radio("Income Stability", ['High', 'Low'])
income = st.slider("Income (USD)", min_value=400, max_value=122966, value=50000)
profession = st.radio("Select Profession", ['Commercial associate', 'Pensioner', 'State servant', 'Working'])
location = st.radio("Select your Location", ['Rural', 'Semi-Urban', 'Urban'])
dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, value=2)
credit_score = st.slider("Credit Score", min_value=580, max_value=900, value=700)
expense_type_1 = st.radio("Expense Type 1", ['N', 'Y'])
expense_type_2 = st.radio("Expense Type 2", ['N', 'Y'])
credit_card_status = st.radio("Credit Card Status", ['Active', 'Inactive', 'Unpossessed'])
current_loan_expenses = st.slider("Current Loan Expenses (USD)", min_value=100, max_value=3419, value=500)
no_of_defaults = st.number_input("Number of Defaults", min_value=0, max_value=10, value=0)
property_age = st.slider("Property Age", min_value=1, max_value=100, value=10)

# Descriptive options for property type
property_type_options = [
    ("Apartment", 0),
    ("Detached House", 1),
    ("Semi-Detached House", 2),
    ("Terraced House", 3),
    ("End of Terrace", 4),
    ("Cottage", 5)
]
property_type_label = st.selectbox("Property Type", options=[opt[0] for opt in property_type_options])
property_type = next(value for label, value in property_type_options if label == property_type_label)
property_location = st.radio("Property Location", ['Rural', 'Semi-Urban', 'Urban'])
co_applicant = st.selectbox("Co-Applicant", options=["No", "Yes"])
co_applicant_value = 1 if co_applicant == "Yes" else 0

property_price = st.slider("Property Price (USD)", min_value=10000, max_value=1077967, value=150000)
loan_amount_request = st.slider("Loan Amount Request (USD)", min_value=6048, max_value=621497, value=10000)


# Add a button to make predictions
if st.button("Predict Loan Sanction Amount"):
    predicted_amount = predict_loan_sanction_amount(
        gender, profession, location, expense_type_1, expense_type_2, 
        credit_card_status, property_location, income_stability, 
        age, income, loan_amount_request, current_loan_expenses, 
        dependents, credit_score, no_of_defaults, property_age, 
        property_type, co_applicant_value, property_price
    )
    
    st.success(f"Maximum Loan Amount for User (USD): ${predicted_amount:.2f}")
