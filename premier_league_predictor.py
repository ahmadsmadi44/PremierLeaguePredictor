from enhanced_prediction_logic import predict_match
import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
@st.cache
def load_data():
    data = pd.read_csv("matches.csv")
    return data

data = load_data()

# Title and description
st.title("Premier League Match Predictor")
st.write("Select two teams to compare and predict the outcome.")

# Dropdown menus for team selection
teams = data['team'].unique()
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", teams)

# Predict button
if st.button("Predict"):
    probabilities = predict_match(data, team1, team2)
    st.write(f"Match Prediction:")
    st.write(f"{probabilities['team1']} win probability: {probabilities['prob1']:.2%}")
    st.write(f"{probabilities['team2']} win probability: {probabilities['prob2']:.2%}")
