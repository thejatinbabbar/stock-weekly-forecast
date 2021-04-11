import streamlit as st

import yfinance as yf

from fbprophet import Prophet
from fbprophet.plot import plot_plotly

from datetime import date
from plotly import graph_objs

st.title('Stocks Weekly Forecast')

st.subheader('Enter the stock ticker:')
ticker = st.text_input('example: GOOG')
ticket = ticker.upper()

# load data from yahoo finance
def load_data(ticker):
    start = "2020-01-01"
    today = date.today().strftime("%Y-%m-%d")
    data = yf.download(ticker, start, today)
    data.reset_index(inplace=True)
    return data

# Plot raw data
def plot_raw_data():
    fig = graph_objs.Figure()
    fig.add_trace(graph_objs.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(graph_objs.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    
def get_forecast(data):
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    
    return model, forecast


if len(ticker)>0:
    data_load_state = st.text('Loading data...')
    data = load_data(ticker)
    if data.empty:
        data_load_state.text(f'No ticker named {ticker}')
        ticker = ''
    else:
        data_load_state.text('Loading data... done!')

        st.subheader(f'Company: {yf.Ticker(ticker).info["longName"]}')
        st.write(data.head())

        plot_raw_data()

        # prepare data for forecasting
        df_train = data[['Date','Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        # train and forecast
        model, forecast = get_forecast(df_train)

        st.subheader('Forecast')
        
        # plot forecast
        st.write(f'Forecast plot for the next week')
        fig = plot_plotly(model, forecast)
        st.plotly_chart(fig)