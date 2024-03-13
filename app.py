######################################################
# INIT
######################################################

# Import libraries and packages
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px

# In some style guides for Streamlit the below options improved appearance, so trying here
st.set_page_config(
    page_title="Used Vehicle DS Dashboard",
    page_icon="✅",
)

######################################################
# Read CSV and add features from /notebooks/EDA.ipynb
######################################################

# Init Dataframe
df = pd.read_csv('vehicles_us.csv')

# Convert 'date_posted' column to datetime
df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')

# Wipe NaNs from 'paint_color' column
df['paint_color'] = df['paint_color'].fillna('Unknown')

# Wipe NaNs from 'is_4wd' column and unify the boolean values to str  
df['is_4wd'] = df['is_4wd'].astype('str')
df['is_4wd'] = df['is_4wd'].where(df['is_4wd'] != 'nan', 'No')
df['is_4wd'] = df['is_4wd'].where(df['is_4wd'] != '1.0', 'Yes')

# Replacing 'model_year', 'cylinders', and 'odometer' with representative values (medians)
df['model_year'] = df['model_year'].fillna(df['model_year'].median())
df['cylinders'] = df['cylinders'].fillna(df['cylinders'].median())
df['odometer'] = df['odometer'].fillna(df['odometer'].median())

# We'll calculate the approximate vehicle age by subtracting the year it was posted from the model year of the car.
df['vehicle_age'] = df['date_posted'].dt.year - df['model_year']

# Create a dictionary of key-value pairs -- 'type': [price1, price2, price3, ...]
type_price_dict = {}
for vtype in df['type'].unique():
    type_price_dict[vtype] = df.query("type == @vtype")['price'].tolist()

######################################################
# STREAMLIT
######################################################

# Title!
st.title('2018-2019 Used Vehicle Advertisement Analysis')

# Section 1: Welcome
st.header('Welcome')
st.markdown('Welcome to this interactive exploratory analysis of used vehicle advertisements. The below data comprises over 50,000 cars advertised during 2018 and 2019.')
st.markdown('The sample graphs below will look (separately) at the age of the vehicles and vehicle price.')

# Section 2: Display Entire Dataframe
st.header('A Quick Look at the Data')
st.dataframe(df)

# Section 3: Display Histogram
st.header('Vehicle Age by Condition')
st.markdown('Double-click on model in legend to isolate that model')
type_fig1 = px.histogram(df, x='vehicle_age', color='condition')
st.write(type_fig1)

# Section 4: Display Scatterplot
st.header('Customizable-Sample Scatterplot of Vehicle Age Against Odometer')

# Create a slider widget for how many random samples to draw
samplemin = 1000
samplemax = 25000
nsamples = st.slider(
    label=f'Select between {samplemin} and {samplemax} samples',
    min_value=samplemin,
    max_value=samplemax,
    value = samplemin + 1000 if samplemin + 1000 < samplemax else samplemax,
    step=1000
)

# Placeholder for below graph
plot_placeholder = st.empty()

# Relating vehicle age to odometer. We should expect something of a linear relationship
fig1, ax1 = plt.subplots()
df.sample(nsamples).plot(
    x='vehicle_age', 
    y='odometer', 
    kind='scatter', 
    ax=ax1,
    alpha=0.2
)

# Log-scale to better see distribution at low end. Add labels
ax1.set_yscale('log')
ax1.set_title('Vehicle Mileage Somewhat Correlated to Vehicle Age')
ax1.set_xlabel('Age of Vehicle (Yrs)')
ax1.set_ylabel('Mileage (Log)')

# Render to placeholder
with plot_placeholder:
    st.pyplot(fig1)

# Section 5: Display Boxplot of Vehicle Prices by Vehicle Type
st.header('Customizable Boxplot Comparing Prices of Vehicle Type')
st.markdown('')

# Create a multiselect widget
types = st.multiselect(
    label='Select two to eight vehicle types to compare. The below graph will update based on your selections.',
    options=df['type'].unique(),
    default=['SUV', 'pickup'],
    placeholder='Choose up to 8 Unique Vehicle Types',
    max_selections=8
)

# Placeholder for below graph
plot_placeholder2 = st.empty()

# Create interactive plot
fig, ax = plt.subplots()
ax.boxplot([type_price_dict[k] for k in types] if len(types)>1 else [0], # If/Else to avoid passing empty list
            labels=types if len(types)>1 else ['']) # If/Else to avoid passing empty list
ax.set_ylim(0, 100000)
ax.set_ylabel('Price ($USD)')
ax.set_xlim(0, len(types)+1)

# Render to placeholder
with plot_placeholder2:
    if len(types)>1:
        st.pyplot(fig)