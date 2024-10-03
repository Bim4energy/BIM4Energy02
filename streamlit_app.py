import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Set wide mode
st.set_page_config(layout="wide", page_title="Energy Consumption Comparison", page_icon="⚡")

# Load CSS file for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply CSS
local_css("style.css")

# Example Energy Consumption Data
categories = ["Heating", "Cooling", "Lighting", "Equipment", "Water Systems"]
base_values = [8000, 3500, 3000, 2000, 1500]
improved_values = [7000, 3200, 2800, 1800, 1400]

# Title with custom font from CSS
st.markdown('<h1 class="title">Energy Consumption: Base vs. Improved</h1>', unsafe_allow_html=True)

# Setup seaborn style for plot
sns.set(style="whitegrid")

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))

# Create smooth line plots
sns.lineplot(x=categories, y=base_values, marker="o", label="Base Case", ax=ax, color="#FFC107", linewidth=2)
sns.lineplot(x=categories, y=improved_values, marker="o", label="Improved Case", ax=ax, color="#FF5722", linewidth=2)

# Set the title and labels
ax.set_xlabel("Energy Category", fontsize=14)
ax.set_ylabel("Energy Consumption (kWh/year)", fontsize=14)

# Customize legend
legend_labels = ['Base Case', 'Improved Case']
ax.legend(title="Scenarios", labels=legend_labels, title_fontsize='13', fontsize='11', loc='upper right')

# Customize grid and layout
plt.grid(True, which='both', linestyle='--', linewidth=0.7)

# Render the plot
st.pyplot(fig)
