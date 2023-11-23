import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

#1st data: current month
M_DATA_URL = 'https://github.com/waikho/st_ICI/raw/main/ICI_mth.csv'
df1 = pd.read_csv(M_DATA_URL)

#display
st.subheader('Weekly Price for Current Month')
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
st.subheader('Historical Monthly Levels')
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

#Select month-range using st.select_slider to calculate MoM change
#st.select_slider can select any data type, including str

# Convert df2 index to list and convert to string format for slider
#dates = df2.index.strftime('%Y-%m').tolist()
dates = df2.index.tolist()

# Convert Timestamp objects to string and format them to show only year and month
formatted_dates = [timestamp.strftime('%Y-%m') for timestamp in dates]


st.subheader('Month-on-Month Price Changes')
MoM_start, MoM_end = st.select_slider('Select the month to show MoM change:', 
                                      options=formatted_dates[-12:],
                                      value=(formatted_dates[-2],formatted_dates[-1]))

idx_from = formatted_dates.index(MoM_start)
idx_to = formatted_dates.index(MoM_end)

#st.write('From index: ', idx_from)
#st.write('To index: ', idx_to)

df_diff = pd.DataFrame((df2.iloc[idx_to] - df2.iloc[idx_from]))

st.write(df2.iloc[[idx_from, idx_to]])

# Assuming df_diff is your DataFrame and it has been reset its index
df_diff.reset_index(inplace=True)
df_diff.columns = ['index', 'value']

fig, ax = plt.subplots()
bars = ax.bar(df_diff['index'], df_diff['value'], 
              color=['red' if x < 0 else 'blue' for x in df_diff['value']])  # color bars based on value

# annotate bars
for bar in bars:
    y_val = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, y_val, round(y_val, 2), 
             va='bottom' if y_val < 0 else 'top', color='black')

st.pyplot(fig)

#df_diff.reset_index(inplace=True)
#st.write(df2.iloc[idx_to] - df2.iloc[idx_from])
#st.bar_chart(df2.iloc[idx_to] - df2.iloc[idx_from])
#st.bar_chart(df_diff)
#st.write(df_diff)
#st.bar_chart(df_diff, x=df_diff.index)
#import matplotlib.pyplot as plt

# Assuming df_diff is your DataFrame and it has been reset its index
#df_diff.reset_index(inplace=True)
#df_diff.columns = ['index', 'value']

#fig, ax = plt.subplots()
#ax.bar(df_diff['index'], df_diff['value'])
#plt.xticks(rotation=90)  # Optional: only if x-labels are too long

#st.pyplot(fig)

