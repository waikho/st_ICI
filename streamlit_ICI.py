import streamlit as st
import pandas as pd
import plotly.express as px

#1st data: current month
M_DATA_URL = 'https://github.com/waikho/st_ICI/raw/main/ICI_mth.csv'
df1 = pd.read_csv(M_DATA_URL)

#display
st.subheader('Weekly price for the current month')
df1

#2nd data: past years
Y_DATA_URL = 'https://github.com/waikho/st_ICI/raw/main/ICI_prices.csv'
df2 = pd.read_csv(Y_DATA_URL)
df2.dropna(inplace=True)
df2['Date'] = pd.to_datetime(df2['Date'], format='%Y-%m')#.dt.to_period('M')
df2.set_index('Date', inplace=True)
df2.sort_index(inplace=True)
for col in df2.columns:
    df2[col] = pd.to_numeric(df2[col], errors='coerce')

#select which ICI price to plot
# Get a list of the dataframe's columns
options = df2.columns.tolist()

# Use the multiselect widget to select columns to plot
columns_to_plot = st.multiselect('Select columns to plot:', options, default=options)

# Check if any columns have been selected
if columns_to_plot:

    # Create a new dataframe that contains only the selected columns
    df_to_plot = df2[columns_to_plot]

    # Plot the selected columns
    #st.line_chart(df_to_plot, height=480)

    # Assuming columns_to_plot is a list of column names
    fig = px.line(df_to_plot, x=df_to_plot.index, y=columns_to_plot)

    # Update hover behavior
    fig.update_traces(mode='lines', hovertemplate=None)
    fig.update_layout(hovermode="x unified")

    st.plotly_chart(fig)

else:
    st.write("No columns selected.")