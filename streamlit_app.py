import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import os

# Set Streamlit to use wide mode (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Debug: Check the current working directory
st.write("Current directory:", os.getcwd())
st.write("Expected file path:", os.path.abspath('BIM4Energy_Variables_Cleaned.json'))

# Load the JSON data
try:
    with open('BIM4Energy_Variables_Cleaned.json') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    st.error("The JSON file could not be found. Please check the file path.")
except json.JSONDecodeError:
    st.error("There was an error decoding the JSON file.")

# Set style for Seaborn
sns.set(style="whitegrid")

# Title
st.title("BIM4Energy Case Study Explorer")

# Input selections from the JSON file
st.sidebar.header("Select Case Study Parameters")

# Handle missing keys with default values
building_type = st.sidebar.selectbox("Select building type", data.get("Case", ["No data"]))
city = st.sidebar.selectbox("Select city", data.get("Cities", ["No data"]))
rotation = st.sidebar.selectbox("Select rotation", data.get("Rotation", ["No data"]))
wall = st.sidebar.selectbox("Select wall insulation", data.get("Wall", ["No data"]))
glazing = st.sidebar.selectbox("Select glazing type", data.get("Glazing", ["No data"]))
photovoltaic = st.sidebar.selectbox("Select photovoltaic power", data.get("Photovoltaic", ["No data"]))

# Example calculation based on the photovoltaic value (for testing)
try:
    photovoltaic_result = float(photovoltaic.split()[0]) * 2 if photovoltaic else 0
except (ValueError, IndexError):
    photovoltaic_result = 0
    st.error("Error parsing the photovoltaic value.")

# Show result in main area
st.write(f"Photovoltaic value (multiplied by 2): {photovoltaic_result} kW")

# Layout for the main content
col1, col2 = st.columns([1, 3])

# Placeholder image to represent the building
with col1:
    st.image("logo.png", caption="Example building")

# Dummy data for energy consumption graph
energy_data = {
    "Base Case": {"Heating": 120, "Cooling": 60, "Other": 40},
    "Improved": {"Heating": 100, "Cooling": 50, "Other": 30}
}

# Display energy consumption bar chart
with col2:
    st.subheader("Energy consumption (kWh/m²/y)")
    energy_df = pd.DataFrame(energy_data).T
    fig, ax = plt.subplots()
    energy_df.plot(kind="bar", stacked=True, ax=ax, color=sns.color_palette("muted"))

    # Ensure the figure is being rendered
    st.write(fig)

    ax.set_ylabel("Energy Consumption (kWh/m²/y)")
    ax.set_title("Energy Consumption by Type")
    st.pyplot(fig)
