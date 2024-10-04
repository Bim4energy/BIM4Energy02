import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import math

# Set Streamlit to use wide mode and a white theme
st.set_page_config(layout="wide", page_title="BIM4Energy Case Study Explorer")

# Custom style for white background in Streamlit
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the JSON data
try:
    with open('BIM4Energy_Variables_Cleaned.json') as file:
        data_variables = json.load(file)
    with open('cost.json') as file:
        data_cost = json.load(file)
except FileNotFoundError as e:
    st.error(f"The JSON file could not be found: {e}")
    st.stop()
except json.JSONDecodeError as e:
    st.error(f"There was an error decoding the JSON file: {e}")
    st.stop()

# Set style for Matplotlib to have a white background
plt.style.use("default")

# Title
st.title("BIM4Energy Case Study Explorer")

# Add the logo at the top of the sidebar
st.sidebar.image("logo.png", use_column_width=True)

# Input selections from the JSON file
st.sidebar.header("Select Case Study Parameters")
building_type = st.sidebar.selectbox("Select Building Type", data_variables.get("Case", ["No data"]))
city = st.sidebar.selectbox("Select City", data_variables.get("Cities", ["No data"]))
rotation = st.sidebar.selectbox("Select Rotation (degrees)", data_variables.get("Rotation", ["No data"]))
wall = st.sidebar.selectbox("Select Wall Insulation", data_variables.get("Wall", ["No data"]))
glazing = st.sidebar.selectbox("Select Glazing Type", data_variables.get("Glazing", ["No data"]))
photovoltaic = st.sidebar.selectbox("Select Photovoltaic Power", data_variables.get("Photovoltaic", ["No data"]), index=0)

# Sidebar additional elements
st.sidebar.header("Building Information")
gross_floor_area = st.sidebar.number_input("Gross Floor Area (m²)", min_value=50, value=100)  # Gross floor area from dropdown
number_of_floors = st.sidebar.number_input("Number of Floors", min_value=1, value=2)
building_age = st.sidebar.slider("Building Age (years)", 0, 100, 25)
occupants = st.sidebar.number_input("Number of Occupants", min_value=1, value=4)

# Investment and Energy Measures
st.sidebar.header("Investment and Energy Measures")
investment_cost = st.sidebar.number_input("Estimated Investment (€)", min_value=1000, value=50000)
improvement_percentage = st.sidebar.slider("Energy Improvement (%)", 0, 100, 25)

### Baseline and Selected Insulation Data ###
baseline_data = data_cost["No change"]
selected_insulation_data = data_cost[wall]

# Energy values from the JSON
baseline_energy_consumption = baseline_data["Energy consumption total (kWh)"]

# Get the energy savings (kWh/m²) from the JSON and calculate total savings
energy_savings_per_m2 = selected_insulation_data["Energy savings (kWh/m2)"]
total_energy_savings = energy_savings_per_m2 * gross_floor_area  # Savings based on the gross floor area

# Calculate the energy consumption for the selected insulation: Baseline - Total Savings
selected_energy_consumption = baseline_energy_consumption - total_energy_savings

# Cost difference calculation
cost_difference = selected_insulation_data["Total cost"] - baseline_data["Total cost"]

# Place everything in one row
compass_col, calc_col, graph_col1, graph_col2 = st.columns([0.2, 1, 1, 1])

# First column: Compass
with compass_col:
    fig, ax = plt.subplots(figsize=(1.5, 1.5))
    ax.set_aspect('equal')
    circle = plt.Circle((0, 0), 1, color='lightgrey', fill=True)
    ax.add_artist(circle)
    rotation_angle = int(rotation)
    ax.arrow(0, 0, 0.9 * math.cos(math.radians(rotation_angle)), 0.9 * math.sin(math.radians(rotation_angle)),
             head_width=0.1, head_length=0.1, fc='blue', ec='blue')
    ax.text(0, 1.1, 'N', ha='center', va='center', fontsize=12, color='black')
    ax.text(1.1, 0, 'E', ha='center', va='center', fontsize=12, color='black')
    ax.text(0, -1.1, 'S', ha='center', va='center', fontsize=12, color='black')
    ax.text(-1.1, 0, 'W', ha='center', va='center', fontsize=12, color='black')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')
    st.pyplot(fig)

# Second column: Calculations
with calc_col:
    st.subheader("Building Energy Calculations")
    st.write(f"**Gross Floor Area**: {gross_floor_area} m²")
    st.write(f"**Baseline Energy Consumption**: {baseline_energy_consumption:,.2f} kWh/year")
    st.write(f"**Selected Energy Consumption**: {selected_energy_consumption:,.2f} kWh/year")
    st.write(f"**Total Energy Savings**: {total_energy_savings:,.2f} kWh/year")
    st.write(f"**Total Cost for Selected Insulation**: {selected_insulation_data['Total cost']:,.2f} Euro")
    st.write(f"**Cost Difference from Baseline**: {cost_difference:,.2f} Euro")

# Third column: Energy Consumption Graph
with graph_col1:
    st.subheader("Energy Consumption Comparison (kWh/year)")
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Show baseline and selected values with the savings subtracted from baseline
    categories = ["Baseline", "Selected"]
    values = [baseline_energy_consumption, selected_energy_consumption]  # Subtract savings from baseline
    colors = ['gray', 'blue']
    
    # Plot baseline and selected values
    bars = ax.bar(categories, values, color=colors)
    
    # Adjust scale to show savings better (auto scaling the difference)
    ax.set_ylim([selected_energy_consumption * 0.98, baseline_energy_consumption * 1.02])  # Set limits to highlight difference
    
    # Add value annotations to each bar (for energy savings)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:,.2f} kWh', ha='center', va='bottom')
    
    # Add horizontal grid lines
    ax.yaxis.grid(True, linestyle='--', linewidth=0.7, color='grey')

    # Remove the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Set labels and title
    ax.set_title("Energy Consumption and Savings", fontsize=10)
    ax.set_ylabel("kWh/year", fontsize=8)
    
    # Render the chart
    st.pyplot(fig)

# Fourth column: Cost Comparison Graph (with value annotations)
with graph_col2:
    st.subheader("Cost Comparison (Euro)")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    cost_categories = ["Baseline", wall]
    cost_values = [baseline_data["Total cost"], selected_insulation_data["Total cost"]]
    bars = ax2.bar(cost_categories, cost_values, color=['gray', 'blue'])

    # Add value annotations to each bar
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:,.2f} €', ha='center', va='bottom')

    # Add horizontal grid lines
    ax2.yaxis.grid(True, linestyle='--', linewidth=0.7, color='grey')

    # Remove the right and top spines
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    # Set labels and title
    ax2.set_title("Cost Comparison", fontsize=10)
    ax2.set_ylabel("Euro", fontsize=8)

    # Render cost chart
    st.pyplot(fig2)
