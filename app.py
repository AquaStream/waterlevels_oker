import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load the pre-trained model from the pickle file
@st.cache_resource
def load_model():
    with open("random_forest_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

# Function to generate future dates
def generate_future_dates(days):
    base_date = datetime.today()
    date_list = [base_date + timedelta(days=x) for x in range(days)]
    return date_list

# Streamlit app
def main():
    st.title("Future Predictions Using Random Forest")

    # Load the model
    model = load_model()

    # User input for prediction duration
    st.sidebar.header("Prediction Settings")
    days_to_predict = st.sidebar.selectbox("Select Prediction Horizon:", [7, 10])

    # Generate future dates
    future_dates = generate_future_dates(days_to_predict)

    # Assuming your model needs some input features, create dummy input data
    # Replace this with actual data as required
    # Example: Assuming the model takes a single feature with a linear increase
    dummy_input_data = np.arange(days_to_predict).reshape(-1, 1)

    # Perform prediction
    predictions = model.predict(dummy_input_data)

    # Prepare the DataFrame for displaying
    prediction_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted Value': predictions
    })

    # Display predictions
    st.subheader(f"Predictions for the Next {days_to_predict} Days")
    st.dataframe(prediction_df)

    # Plotting the predictions
    st.subheader("Prediction Plot")
    fig, ax = plt.subplots()
    ax.plot(prediction_df['Date'], prediction_df['Predicted Value'], marker='o')
    ax.set_title(f"Predicted Values for the Next {days_to_predict} Days")
    ax.set_xlabel("Date")
    ax.set_ylabel("Predicted Value")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show plot
    st.pyplot(fig)

if __name__ == "__main__":
    main()
