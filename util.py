import numpy as np
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews


def get_pricing_data(data):
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    annual_return = data2['% Change'].mean() * 252 * 100
    std_dev = np.std(data2['% Change']) * np.sqrt(252) * 100
    risk_adj_return = (annual_return / std_dev).round(2)
    return data2, annual_return, std_dev, risk_adj_return


def get_fundamental_data(ticker):
    fd = FundamentalData(output_format='pandas')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])

    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])

    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])

    return bs, is1, cf


def get_stock_news(ticker):
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    return df_news
