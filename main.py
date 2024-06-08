import streamlit as st
import plotly.express as px
import yfinance as yf
from util import *
from dotenv import load_dotenv

load_dotenv()

st.title('Stock Dashboard')
st.sidebar.title('Options')
ticker = st.sidebar.text_input('Stock Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

submit = st.sidebar.button('Submit', type='primary', disabled=not ticker)

if submit:
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.index.empty:
        st.sidebar.warning('Please enter a valid Ticker Symbol')

    else:
        if ticker:
            fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
            st.plotly_chart(fig)

        pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

        with pricing_data:
            st.header('Price Movements')
            data2, annual_return, std_dev, risk_adj_return = get_pricing_data(data)
            st.write(data2)
            st.write('Annual Return: ', annual_return.round(2), '%')
            st.write('Standard Deviation: ', std_dev.round(2), '%')
            st.write('Risk Adj Return:', risk_adj_return.round(2))

        with fundamental_data:
            try:
                bs, is1, cf = get_fundamental_data(ticker)

                st.subheader('Balance Sheet')
                st.write(bs)

                st.subheader('Income Statement')
                st.write(is1)

                st.subheader('Cash Flow Statement')
                st.write(cf)

            except ValueError as e:
                st.info(e)

        with news:
            st.header(f'News of {ticker}')
            df_news = get_stock_news(ticker)
            for i in range(10):
                st.subheader(f'News {i+1}')
                st.write(df_news['published'][i])
                st.write(df_news['title'][i])
                st.write(df_news['summary'][i])
                title_sentiment = df_news['sentiment_title'][i]
                st.write(f'Title Sentiment {title_sentiment}')
                news_sentiment = df_news['sentiment_summary'][i]
                st.write(f'News Sentiment {news_sentiment}')
