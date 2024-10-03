import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Set Streamlit to use wide mode with a custom theme
st.set_page_config(layout="wide", page_title="BIM4Energy Explorer", page_icon="⚡")

# Load JSON (Mocked for the example)
# Add your JSON loading code here

# Define custom styles using st.markdown for modern look
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #F0F2F6;
        }
        .main-container {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .energy-graph-container {
            padding: 16px;
            border-radius: 12px;
            background-color: #F8F9FC;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .compass-container {
            padding: 16px;
            border-radius: 12px;
            background-color: #EFF5FF;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .title-header {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 32px;
            font-weight: bold;
            color: #2D3748;
        }
        .sub-header {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 18px;
            color: #4A5568;
        }
        .energy-data {
            background-color: #EDF2F7;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.08);
        }
        .result-card {
            background-color: #FFFFFF;
            border-radius: 8px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.08);
            padding: 16px;
            margin-top: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Title with modern styling
st.markdown('<h1 class="title-header">BIM4Energy Case Study Explorer</h1>', unsafe_allow_html=True)

# Sidebar design
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.header("Select Case Study Parameters")

# Input selections (Mocked data for illustration)
building_type = st.sidebar.selectbox("Select Building Type", ["Single Family", "Residential Block"])
city = st.sidebar.selectbox("Select City", ["Amsterdam", "Berlin", "Paris"])
rotation = st.sidebar.selectbox("Select Rotation (degrees)", [0, 45, 90, 180])
wall = st.sidebar.selectbox("Select Wall Insulation", ["No Change", "50mm Insulation", "100mm Insulation"])
glazing = st.sidebar.selectbox("Select Glazing Type", ["Double Glazing", "Triple Glazing"])
photovoltaic = st.sidebar.selectbox("Select Photovoltaic Power", ["No Change", "5kW", "10kW"])

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
    "Heating": 8000 * (gross_floor_area / 100) * (1 + 0.1 * wall_list.index(wall)),
    "Cooling": 3500 * (gross_floor_area / 100) * (1 + 0.08 * wall_list.index(wall)),
    "Lighting": 3000 * (gross_floor_area / 100),
    "Equipment": 2000 * (gross_floor_area / 100),
    "Water Systems": 1500 * (gross_floor_area / 100)
}

energy_improved = {key: value * (1 - improvement_percentage / 100) for key, value in energy_baseline.items()}

st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<h2 class="sub-header">Energy Consumption Results</h2>', unsafe_allow_html=True)

# Energy data summary cards
st.markdown(f"""
    <div class="energy-data">
        <p><b>Gross Floor Area:</b> {gross_floor_area} m²</p>
        <p><b>Base Energy Consumption:</b> {sum(energy_baseline.values()):,.2f} kWh/year</p>
        <p><b>Improved Energy Consumption:</b> {sum(energy_improved.values()):,.2f} kWh/year</p>
    </div>
""", unsafe_allow_html=True)

### Energy Consumption Line Chart ###
st.markdown('<div class="energy-graph-container">', unsafe_allow_html=True)
categories = ["Heating", "Cooling", "Lighting", "Equipment", "Water Systems"]
base_values = list(energy_baseline.values())
improved_values = list(energy_improved.values())

sns.set_style("whitegrid")
fig, ax = plt.subplots()
sns.lineplot(x=categories, y=base_values, marker='o', label="Base Case", ax=ax, color="#007ACC")
sns.lineplot(x=categories, y=improved_values, marker='o', label="Improved Case", ax=ax, color="#FF8800")

ax.set_ylabel("Energy Consumption (kWh/year)")
ax.set_title("Energy Consumption Before and After Improvement")
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

### Compass Rotation Visualization ###
st.markdown('<div class="compass-container">', unsafe_allow_html=True)
st.markdown('<h3 class="sub-header">Orientation (Rotation to North)</h3>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(3, 3))
ax.set_aspect('equal')
circle = plt.Circle((0, 0), 1, color='lightgrey', fill=True)
ax.add_artist(circle)

rotation_angle = int(rotation)
arrow_length = 0.9
ax.arrow(0, 0, arrow_length * math.cos(math.radians(rotation_angle)),
         arrow_length * math.sin(math.radians(rotation_angle)),
         head_width=0.1, head_length=0.1, fc='blue', ec='blue')

ax.text(0, 1.1, 'N', ha='center', va='center', fontsize=12, color='black')
ax.text(1.1, 0, 'E', ha='center', va='center', fontsize=12, color='black')
ax.text(0, -1.1, 'S', ha='center', va='center', fontsize=12, color='black')
ax.text(-1.1, 0, 'W', ha='center', va='center', fontsize=12, color='black')

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.axis('off')
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
