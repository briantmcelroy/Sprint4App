######################################################
# INIT
######################################################

# Import libraries and packages
import streamlit as st
import pandas as pd
import plotly.express as px

######################################################
# Read CSV and add features from /notebooks/EDA.ipynb
######################################################

# Init Dataframe
df = pd.read_csv('vehicles_us.csv')

# Convert 'date_posted' column to datetime
df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')

# Wipe NaNs from 'paint_color' column
df['paint_color'] = df['paint_color'].fillna(0)

# Wipe NaNs from 'is_4wd' column and unify the boolean values to str  
df['is_4wd'] = df['is_4wd'].astype('str')
df['is_4wd'] = df['is_4wd'].where(df['is_4wd'] != 'nan', 'No')
df['is_4wd'] = df['is_4wd'].where(df['is_4wd'] != '1.0', 'Yes')

# We'll calculate the approximate vehicle age by subtracting the year it was posted from the model year of the car.
df['vehicle_age'] = df['date_posted'].dt.year - df['model_year']

######################################################
# STREAMLIT DISPLAY
######################################################

# Title!
st.title('2018-2019 Used Vehicle Advertisement Analysis')

# Section 1: Welcome
st.header('Welcome')
st.markdown('Welcome to our interactive exploratory analysis of used vehicle advertisements. The below data comprises over 50,000 cars advertised during 2018 and 2019.')

# Section 2: Display Entire Dataframe
st.header('A Quick Look at the Data')
st.dataframe(df)

# Section 3: Display Histogram 1
st.header('Histogram of Vehicle Price by Type')
type_fig = px.histogram(df, x='price', color='type')
st.write(type_fig)
