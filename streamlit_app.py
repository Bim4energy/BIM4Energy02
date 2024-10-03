import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# Set Streamlit to use wide mode
st.set_page_config(layout="wide")

# Load the JSON data
try:
    with open('BIM4Energy_Variables_Cleaned.json') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    st.error("The JSON file could not be found. Please check the file path.")
except json.JSONDecodeError:
    st.error("There was an error decoding the JSON file.")

# Set style for Matplotlib
plt.style.use("ggplot")

# Title
st.title("BIM4Energy Case Study Explorer")

# Add the logo at the top of the sidebar
st.sidebar.image("logo.png", use_column_width=True)

# Input selections from the JSON file
st.sidebar.header("Select Case Study Parameters")

# Handle missing keys with default values from the JSON
case_list = data.get("Case", ["No data"])
cities_list = data.get("Cities", ["No data"])
rotation_list = data.get("Rotation", ["No data"])
wall_list = data.get("Wall", ["No data"])
glazing_list = data.get("Glazing", ["No data"])
photovoltaic_list = data.get("Photovoltaic", ["No data"])

# Sidebar input elements
building_type = st.sidebar.selectbox("Select Building Type", case_list)
city = st.sidebar.selectbox("Select City", cities_list)
rotation = st.sidebar.selectbox("Select Rotation", rotation_list)
wall = st.sidebar.selectbox("Select Wall Insulation", wall_list)
glazing = st.sidebar.selectbox("Select Glazing Type", glazing_list)
# Set default value of photovoltaic to the first element from the JSON
photovoltaic = st.sidebar.selectbox("Select Photovoltaic Power", photovoltaic_list, index=0)

# Sidebar additional elements (mimicking the UI layout from Excel)
st.sidebar.header("Building Information")
gross_floor_area = st.sidebar.number_input("Gross Floor Area (m²)", min_value=50, value=100)
number_of_floors = st.sidebar.number_input("Number of Floors", min_value=1, value=2)
building_age = st.sidebar.slider("Building Age (years)", 0, 100, 25)
occupants = st.sidebar.number_input("Number of Occupants", min_value=1, value=4)

# Placeholder for other inputs (e.g., for investment or other assessments)
st.sidebar.header("Investment and Energy Measures")
investment_cost = st.sidebar.number_input("Estimated Investment (€)", min_value=1000, value=50000)
improvement_percentage = st.sidebar.slider("Energy Improvement (%)", 0, 100, 25)

### Dynamic Calculation Based on Inputs ###
# Base energy consumption values, for example, can be dependent on the building type and other parameters
energy_baseline = {
    "Heating": 8530 * (gross_floor_area / 100),  # Example: Adjust base consumption by floor area
    "Cooling": 3983 * (gross_floor_area / 100),
    "Interior Lighting": 3762 * (gross_floor_area / 100),
    "Interior Equipment": 2070 * (gross_floor_area / 100),
    "Water Systems": 1906 * (gross_floor_area / 100)
}

# Improved energy values based on user input for improvement percentage
energy_improved = {key: value * (1 - improvement_percentage / 100) for key, value in energy_baseline.items()}

# Show calculated results in the main area
st.write(f"Gross Floor Area: {gross_floor_area} m²")
st.write(f"Base Energy Consumption: {sum(energy_baseline.values()):,.2f} kWh/year")
st.write(f"Improved Energy Consumption: {sum(energy_improved.values()):,.2f} kWh/year")

# Layout for the main content
col1, col2 = st.columns([1, 3])

# Display energy consumption comparison based on the selected parameters
with col2:
    st.subheader("Energy Consumption Comparison (kWh/year)")
    
    # Prepare energy data for the graph
    energy_data = {
        "Base Case": sum(energy_baseline.values()),
        "Improved Case": sum(energy_improved.values())
    }
    
    energy_df = pd.DataFrame.from_dict(energy_data, orient='index', columns=["Energy Consumption (kWh)"])
    
    # Plot the energy consumption comparison
    fig, ax = plt.subplots()
    energy_df.plot(kind="bar", ax=ax, color=["#1f77b4", "#ff7f0e"])
    
    ax.set_ylabel("Energy Consumption (kWh/year)")
    ax.set_title("Energy Consumption Before and After Improvement")
    
    st.pyplot(fig)
