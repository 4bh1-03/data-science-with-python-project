import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


count = st_autorefresh(interval=15*1000, limit=None, key="crypto_refresh")
#Adding webpage title and icon
st.set_page_config(
    page_title="Interactive Crypto Dashboard",
    page_icon="📈",
    layout="wide"
)


st.title("Interactive Cryptocurrency Dashboard")
st.markdown("""
This dashboard allows you to analyze real-time market data for popular cryptocurrencies. 
Select a coin from the dropdown to get started. The data is fetched live from the CoinGecko API.
""")

# ------------------------------------------------------------------- Defining reqd functions -------------------------------------------------------------------

# 1. Data fetching using CoinGecko API
@st.cache_data(ttl=600) # Here we are using Streamlit's caching to avoid re-fetching data on every interaction. Cache data for 600 seconds(10 minutes)
def fetch_crypto_data(coin_id, days):
    # Fetches market data for a given cryptocurrency
    st.info(f"Fetching latest data for {coin_id.title()}...")
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    try:
        response = requests.get(url) #This uses the requests library to send an HTTP GET request to the CoinGecko API and stores the server's response in the 'response'.
        response.raise_for_status() #This is used to raise any errors returned by the API.
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# 2. Data Processing -> Converting raw JSON data into python dataframe
def process_data(raw_data):
    if not raw_data:
        return pd.DataFrame()

    df = pd.DataFrame(raw_data['prices'], columns=['timestamp', 'price'])
    df['volume'] = [vol[1] for vol in raw_data['total_volumes']]
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    
    return df

# 3. Sidebar for User Input ---
st.sidebar.header("Dashboard Controls")

COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "DOGE": "dogecoin",
    "XRP": "ripple",
    "XRP": "ripple",
    "TETH": "tether",
    "BNB":"binancecoin",
    "SOL":"solana",
    "USDC":"usd-coin",
    "STETH":"staked-ether",
    "TRON":"tron",
    "CARD":"cardano",
    "WSTE":"wrapped-steth",
    "CHAI":"chainlink",
    "PI":"pi-network"
}
selected_coin_name = st.sidebar.selectbox(
    "Select a Cryptocurrency",
    options=list(COIN_MAP.keys()),
    index=0 # Default coin set to bitcoin (BTC)
)
selected_coin_id = COIN_MAP[selected_coin_name]

# ------------------------------------------------------------------- Main Logic -------------------------------------------------------------------

DAYS = 60 # Time period ~ 2 months

# Fetch and process data based on user selection
raw_data = fetch_crypto_data(selected_coin_id, DAYS)

if raw_data:
    df = process_data(raw_data)

    if not df.empty:
        # Display Latest price, 24hr trading volume and the data points fetched for a selected coin
        st.subheader(f"Key Metrics for {selected_coin_name}")
        latest_price = df['price'][-1]
        prev_price = df['price'][-2]
        price_change = latest_price - prev_price
        price_change_pct = (price_change / prev_price) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric(
            label="Latest Price (USD)",
            value=f"${latest_price:,.2f}",
            delta=f"${price_change:,.2f} ({price_change_pct:.2f}%)"
        )
        col2.metric(
            label=f"24h Trading Volume (USD)",
            value=f"${df['volume'][-1]:,.0f}"
        )
        col3.metric(
            label="Data Points Fetched",
            value=f"{len(df)}"
        )
        
        # Plotting Interactive plots using Plotly
        st.subheader(f"Price Trend Over the Last {DAYS} Days")

        # Price Trend Chart with Rangeslider
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=df.index, 
            y=df['price'], 
            mode='lines', 
            name='Price',
            line=dict(color='royalblue', width=2),
            hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Price</b>: $%{y:,.2f}<extra></extra>' # Template for data to be displayed on hovering over the graph
        ))
        
        fig_price.update_layout(
            title=f'{selected_coin_name} Price Trend',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            xaxis_rangeslider_visible=True, # This adds the horizontal slider
            template='plotly_white',
            hovermode='x unified'
        )
        st.plotly_chart(fig_price, use_container_width=True)

        # Trading Volume Chart with Rangeslider
        st.subheader(f"Daily Trading Volume")
        fig_volume = go.Figure()
        fig_volume.add_trace(go.Bar(
            x=df.index,
            y=df['volume'],
            name='Volume',
            marker_color='lightseagreen',
            hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Volume</b>: $%{y:,.0f}<extra></extra>' # Template for data to be displayed on hovering over the graph
        ))
        fig_volume.update_layout(
            title=f'{selected_coin_name} Trading Volume',
            xaxis_title='Date',
            yaxis_title='Volume (USD)',
            xaxis_rangeslider_visible=True,
            template='plotly_white',
            hovermode='x unified'
        )
        st.plotly_chart(fig_volume, use_container_width=True)

        # Price Distribution Histogram with Rangeslider
        st.subheader("Price Distribution")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df['price'],
            name='Price Distribution',
            marker_color='mediumpurple',
            hovertemplate='<b>Price Range</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>' # Template for data to be displayed on hovering over the graph
        ))
        fig_hist.update_layout(
            title=f'{selected_coin_name} Price Distribution',
            xaxis_title='Price (USD)',
            yaxis_title='Frequency',
            xaxis_rangeslider_visible=True,
            template='plotly_white'
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    else:
        st.warning("Could not process the fetched data.")
else:
    st.error("Failed to fetch data from the API. Please try again later.")

# Footer
st.markdown("---")
st.markdown(f"Data sourced from [CoinGecko](https://www.coingecko.com/). Dashboard built with Streamlit. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.write(f"Auto-refresh count: {count}")