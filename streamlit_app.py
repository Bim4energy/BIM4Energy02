import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import json  # Add the missing import for json

# Set Streamlit to use wide mode with a custom theme
st.set_page_config(layout="wide", page_title="BIM4Energy Explorer", page_icon="⚡", initial_sidebar_state='expanded')

# Load JSON data
# Make sure the file path is correct
try:
    with open('BIM4Energy_Variables_Cleaned.json') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    st.error("The JSON file could not be found. Please check the file path.")
except json.JSONDecodeError:
    st.error("There was an error decoding the JSON file.")

# Define custom styles using st.markdown for modern look
st.markdown("""
    <style>
        body {
            height: 100vh;
            margin: 0;
            padding: 0;
        }
        .main-container {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            height: 100vh;  /* Full viewport height */
        }
        .top-row {
            display: flex;
            justify-content: space-between;
            height: 20vh;  /* Top row takes 20% of the viewport height */
        }
        .left-container, .right-container {
            width: 48%;  /* Split the columns */
        }
        .compass-container {
            height: 100%;
            padding: 8px;
            background-color: #EFF5FF;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .energy-data {
            height: 100%;
            background-color: #EDF2F7;
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.08);
        }
        .energy-graph-container {
            height: 70vh;  /* Graph takes 70% of the viewport height */
            padding: 8px;
            border-radius: 12px;
            background-color: #F8F9FC;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .title-header {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 32px;
            font-weight: bold;
            color: #2D3748;
            margin-bottom: 16px;
        }
        .sub-header {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 18px;
            color: #4A5568;
        }
    </style>
""", unsafe_allow_html=True)

# Title with modern styling
st.markdown('<h1 class="title-header">BIM4Energy Case Study Explorer</h1>', unsafe_allow_html=True)

# Sidebar design
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.header("Select Case Study Parameters")

# Input selections from JSON
building_type = st.sidebar.selectbox("Select Building Type", data.get("Case", ["No data"]))
city = st.sidebar.selectbox("Select City", data.get("Cities", ["No data"]))
rotation = st.sidebar.selectbox("Select Rotation (degrees)", data.get("Rotation", ["No data"]))
wall = st.sidebar.selectbox("Select Wall Insulation", data.get("Wall", ["No data"]))
glazing = st.sidebar.selectbox("Select Glazing Type", data.get("Glazing", ["No data"]))
photovoltaic = st.sidebar.selectbox("Select Photovoltaic Power", data.get("Photovoltaic", ["No data"]))

# Sidebar additional elements
st.sidebar.header("Building Information")
gross_floor_area = st.sidebar.number_input("Gross Floor Area (m²)", min_value=50, value=100)
number_of_floors = st.sidebar.number_input("Number of Floors", min_value=1, value=2)
building_age = st.sidebar.slider("Building Age (years)", 0, 100, 25)
occupants = st.sidebar.number_input("Number of Occupants", min_value=1, value=4)

st.sidebar.header("Investment and Energy Measures")
investment_cost = st.sidebar.number_input("Estimated Investment (€)", min_value=1000, value=50000)
improvement_percentage = st.sidebar.slider("Energy Improvement (%)", 0, 100, 25)

# Dynamic Calculation Based on Inputs (Placeholder logic)
energy_baseline = {
    "Heating": 8000 * (gross_floor_area / 100) * (1 + 0.1 * wall.index(wall)),
    "Cooling": 3500 * (gross_floor_area / 100) * (1 + 0.08 * wall.index(wall)),
    "Lighting": 3000 * (gross_floor_area / 100),
    "Equipment": 2000 * (gross_floor_area / 100),
    "Water Systems": 1500 * (gross_floor_area / 100)
}

energy_improved = {key: value * (1 - improvement_percentage / 100) for key, value in energy_baseline.items()}

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Top row with compass and energy data
st.markdown('<div class="top-row">', unsafe_allow_html=True)

# Left column: Compass Visualization
st.markdown('<div class="left-container">', unsafe_allow_html=True)
st.markdown('<div class="compass-container">', unsafe_allow_html=True)
st.markdown('<h3 class="sub-header">Orientation (Rotation to North)</h3>', unsafe_allow_html=True)

fig_compass, ax_compass = plt.subplots(figsize=(2, 2))  # Reduced size for compass
ax_compass.set_aspect('equal')
circle = plt.Circle((0, 0), 1, color='lightgrey', fill=True)
ax_compass.add_artist(circle)

rotation_angle = int(rotation)
arrow_length = 0.9
ax_compass.arrow(0, 0, arrow_length * math.cos(math.radians(rotation_angle)),
                 arrow_length * math.sin(math.radians(rotation_angle)),
                 head_width=0.1, head_length=0.1, fc='blue', ec='blue')

ax_compass.text(0, 1.1, 'N', ha='center', va='center', fontsize=12, color='black')
ax_compass.text(1.1, 0, 'E', ha='center', va='center', fontsize=12, color='black')
ax_compass.text(0, -1.1, 'S', ha='center', va='center', fontsize=12, color='black')
ax_compass.text(-1.1, 0, 'W', ha='center', va='center', fontsize=12, color='black')

ax_compass.set_xlim(-1.2, 1.2)
ax_compass.set_ylim(-1.2, 1.2)
ax_compass.axis('off')
st.pyplot(fig_compass)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Right column: Energy Consumption Results
st.markdown('<div class="right-container">', unsafe_allow_html=True)
st.markdown(f"""
    <div class="energy-data">
        <p><b>Gross Floor Area:</b> {gross_floor_area} m²</p>
        <p><b>Base Energy Consumption:</b> {sum(energy_baseline.values()):,.2f} kWh/year</p>
        <p><b>Improved Energy Consumption:</b> {sum(energy_improved.values()):,.2f} kWh/year</p>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Energy graph section
st.markdown('<div class="energy-graph-container">', unsafe_allow_html=True)
categories = ["Heating", "Cooling", "Lighting", "Equipment", "Water Systems"]
base_values = list(energy_baseline.values())
improved_values = list(energy_improved.values())

sns.set_style("whitegrid")
fig_energy, ax_energy = plt.subplots(figsize=(6, 3))  # Adjusted size to fit the graph area
sns.lineplot(x=categories, y=base_values, marker='o', label="Base Case", ax=ax_energy,
