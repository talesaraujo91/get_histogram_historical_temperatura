import streamlit as st
from streamlit_navigation_bar import st_navbar
from getFromAPI import get_response
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Initialize session state variables
if 'cities' not in st.session_state:
    st.session_state.hist_data = []#get_response(-20.4297, -49.2711,"2024-08-21","2024-09-05")
    st.session_state.cities = pd.read_csv('worldcities.csv')

def plot_hist_chart(df):
    df.columns = ['datetime','temperature','humidity','preciptation','percentage']

    # Calculate the percentage frequency
    df['percentage'] = df['temperature'].value_counts(normalize=True) * 100

    # Add a slider for the number of bins
    bins = st.slider('Select number of bins', min_value=4, max_value=100, value=25)

    # Create the histogram
    fig = px.histogram(df, x='temperature', histnorm='percent',nbins=bins)

    # Calculate cumulative percentage
    df['cumulative_percentage'] = df['temperature'].rank(pct=True) * 100

    # Add cumulative percentage text to each bin
    fig.update_traces(texttemplate='%{y:.2f}%', textposition='inside')

    # Update layout for better visualization
    fig.update_layout(
        title='Temperature Histogram',
        xaxis_title='Temperature',
        yaxis_title='Frequency (%)'
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

def plot_hist_chart2(df,column,bins):
    df.columns = ['datetime','temperature','humidity','preciptation']#,'percentage','cumulative_percentage']

    # Add a slider for the number of bins
    #bins = st.slider('Select number of bins', min_value=4, max_value=500, value=25)

    # Calculate the histogram data
    hist, bin_edges = pd.cut(df[column], bins=bins, retbins=True, right=False)
    hist_counts = hist.value_counts().sort_index()

    # Calculate cumulative frequency
    cumulative_counts = hist_counts.cumsum()
    cumulative_percentage = cumulative_counts / cumulative_counts.max() * 100

    # Create the histogram plot
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=df[column],
        nbinsx=bins,
        histnorm='percent',
        name='Histogram'
    ))

    # Add cumulative percentage text to each bin
    
    #for i in range(len(bin_edges) - 1):
    #    fig.add_trace(go.Scatter(
    #        x=[(bin_edges[i] + bin_edges[i+1]) / 2],
    #        y=[hist_counts.iloc[i] / hist_counts.sum() * 100],
    #        text=f'{cumulative_percentage.iloc[i]:.2f}%',
    #        mode='text',
    #        showlegend=False
    #   ))

    # Update layout for better visualization
    fig.update_layout(
        title='Temperature Histogram with Cumulative Percentage',
        xaxis_title=column,
        yaxis_title='Frequency (%)',
        bargap=0.2
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

def st_navbar_config():
    pages = ["","","","","","","WEATHER HISTORICAL ANALYSIS","","","","",""]
    styles = {
        "nav": {
            "background-color": "rgb(255, 205, 17)",
            "justify-content": "left",
        },
        "span": {
            "color": "black",
            "padding": "14px",
        },
        "img": {
            "padding-right": "1px",
        },
        "active": {
            "background-color": "rgba(255, 205, 17, 0)",
        },
        "hover": {
            "background-color": "rgba(255, 205, 17, 0)",
        },
    }
    options = {
        "show_menu": True,
        "show_sidebar": True,
        "use_padding": False
    }
    page = st_navbar(pages,logo_path="images/Progress Rail Logo_Black.svg",styles=styles,options=options)

    st.write("") #Setting padding between the navigation bar and the page
#st_navbar_config()

with st.sidebar:
    st.sidebar.image("images/ProgressRail_Full Color_Logo.png", use_column_width=True)

    selected_country = st.selectbox('Country',st.session_state.cities['country'].unique())

    if selected_country:
        dfCities_Filtered = st.session_state.cities[st.session_state.cities['country']==selected_country]
    else:
        dfCities_Filtered = st.session_state.cities
    selected_city = st.selectbox('City',dfCities_Filtered['city'])

    city_data = st.session_state.cities[(st.session_state.cities['country'] == selected_country)& (st.session_state.cities['city'] == selected_city)]

    if not city_data.empty:
        lat = city_data.iloc[0]['lat']
        lng = city_data.iloc[0]['lng']
        population = city_data.iloc[0]['population']

    default_start_date = datetime.now() - timedelta(days=365)
    selected_start_date = st.date_input('Select start date', value=default_start_date)
    selected_end_date = st.date_input('Select end date')
        
if st.sidebar.button('Run Analysis'):
    st.write(population)
    st.write(selected_city)
    st.write(selected_country)
    st.write(selected_start_date)
    st.session_state.hist_data = get_response(lat,lng,selected_start_date,selected_end_date)
    st.write(st.session_state.hist_data)

st.session_state.hist_data.columns = ['datetime','temperature','humidity','preciptation']
st.write(st.session_state.hist_data)
bins = st.slider('Select number of bins', min_value=4, max_value=100, value=25)
plot_hist_chart2(st.session_state.hist_data,'temperature',bins)
plot_hist_chart2(st.session_state.hist_data,'humidity',bins)
plot_hist_chart2(st.session_state.hist_data,'preciptation',bins)