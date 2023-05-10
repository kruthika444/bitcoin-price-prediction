import pandas as pd
import cryptocompare
import datetime as dt
import plotly.graph_objs as go
import yfinance as yf
import plotly
import plotly.express as px
import requests
import re
from datetime import date
from numerize import numerize
from plotly.subplots import make_subplots
from datetime import timedelta
from bs4 import BeautifulSoup
from datetime import datetime
import json

yf.pdr_override()


def btc_price():
  stock = 'BTC-INR'
  df = yf.download(tickers=stock, period='1d')
  df = pd.DataFrame(df)
  df = df.reset_index(drop=True)
  return df


#print(btc_price())

stock = 'BTC-INR'
df = yf.download(tickers=stock, period='2y')
df = pd.DataFrame(df)


# df
def graph_candle_stick():

  fig = go.Figure(data=[
    go.Candlestick(x=df.index,
                   open=df['Open'],
                   high=df['High'],
                   low=df['Low'],
                   close=df['Close'])
  ])
  fig.update_layout(title='BITCOIN - CANDLESTICK',
                    title_x=0.5,
                    yaxis_title='Stock Price (INR per Shares)')
  fig.update_xaxes(
    rangeselector_bgcolor='#000',
    rangeselector_activecolor='#ea8b19',
    rangeslider_visible=True,
    rangeselector=dict(buttons=list([
      dict(count=7, label="7d", step="day", stepmode="backward"),
      dict(count=30, label="1mo", step="day", stepmode="backward"),
      dict(count=6, label="6mo", step="month", stepmode="todate"),
      dict(count=1, label="1y", step="year", stepmode="backward"),
      dict(step="all")
    ])))
  fig.update_layout(template='plotly_dark',
                    yaxis_title='BTC Stock',
                    xaxis_title='Date',
                    plot_bgcolor='rgb(17, 17, 17)')
  fig.update_xaxes(linecolor='#ea8b19',
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_yaxes(linecolor='#ea8b19',
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_layout(spikedistance=1000,
                    hoverdistance=100,
                    xaxis_rangeslider_visible=False)
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def graph_normal():
  fig = px.area(df,
                x=df.index,
                y=df.Close,
                hover_data=["Open", "Low", "High", 'Close'],
                color_discrete_sequence=px.colors.qualitative.Vivid)
  fig.update_layout(title='BITCOIN',
                    title_x=0.5,
                    yaxis_title='Stock Price (INR per Shares)')
  fig.update_xaxes(
    rangeselector_bgcolor='#000',
    rangeselector_activecolor='#ea8b19',
    rangeslider_visible=False,
    rangeselector=dict(buttons=list([
      dict(count=7, label="7d", step="day", stepmode="backward"),
      dict(count=30, label="1mo", step="day", stepmode="backward"),
      dict(count=6, label="6mo", step="month", stepmode="todate"),
      dict(count=1, label="1y", step="year", stepmode="backward"),
      dict(step="all")
    ])))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(
      bgcolor="black",
      font=dict(
        family=
        "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
        size=18)))
  fig.update_layout(template='plotly_dark')
  fig.update_traces(mode="lines")
  fig.update_xaxes(linecolor='#ea8b19',
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_yaxes(linecolor='#ea8b19',
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_layout(spikedistance=1000, hoverdistance=100)
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def past_btc():
  stock = 'BTC-INR'
  df = yf.download(tickers=stock, period='15d')
  df = pd.DataFrame(df)
  df["Date"] = df.index
  df.drop(["Adj Close"], axis=1)
  df = df.reset_index(drop=True)
  df['Date'] = df['Date'].dt.date
  df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
  df["Day"] = df.apply(lambda row: row.Date.day_name(), axis=1)
  df.sort_values(by='Date', ascending=False, inplace=True)
  df['Date'] = pd.to_datetime(df.Date)
  df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
  df = df.loc[:, ["Date", "Day", "Open", "High", "Low", "Close", "Volume"]]
  df["Open"] = df.apply(lambda row: numerize.numerize(row.Open), axis=1)
  df["High"] = df.apply(lambda row: numerize.numerize(row.High), axis=1)
  df["Low"] = df.apply(lambda row: numerize.numerize(row.Low), axis=1)
  df["Close"] = df.apply(lambda row: numerize.numerize(row.Close), axis=1)
  df["Volume"] = df.apply(lambda row: numerize.numerize(row.Volume), axis=1)
  return df


fin = pd.read_csv('final-all.csv')
fin = fin.drop('Unnamed: 0', axis=1)
fin['date'] = pd.to_datetime(fin['date'])
today = date.today().strftime('%Y/%m/%d')
result = fin[(fin['date'] > today)]
dd = fin[(fin['date'] <= today)]


def tmro_price():
  return float(result['price'].values[0])


def today_price():
  return float(dd['price'].values[-1])


def pred_graph():
  fig = go.Figure()
  fig.add_trace(
    go.Scatter(x=dd.date,
               y=dd.price,
               name='past',
               hovertemplate='Price: %{y:.2f}' + '<br>Date: %{x}',
               line=dict(color='#ea8b19', width=2)))

  fig.add_trace(
    go.Scatter(x=result.date,
               y=result.price,
               name='future',
               hovertemplate='Price: %{y:.2f}' + '<br>Date: %{x}',
               line=dict(color='white', width=3, dash='solid')))
  fig.update_traces(mode="markers+lines")

  fig.update_xaxes(linecolor='#ea8b19',
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_yaxes(linecolor='#ea8b19',
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_layout(spikedistance=1000, hoverdistance=100)
  fig.update_layout(plot_bgcolor='rgb(17, 17, 17)',
                    hoverlabel=dict(font_size=16))
  fig.update_layout(title='Predicted Prices',
                    title_x=0.5,
                    xaxis_title="Date",
                    yaxis_title="Close Price",
                    legend_title="Data")
  fig.update_layout(template='plotly_dark', yaxis_range=[0, 3500000])
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def pred_week():
  df = result
  df['date'] = df['date'].dt.date
  df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
  df["Day"] = df.apply(lambda row: row.date.day_name(), axis=1)
  df = df.loc[:, ["date", "Day", "price"]]
  df['date'] = pd.to_datetime(df.date)
  df['date'] = df['date'].dt.strftime('%d-%m-%Y')

  return df.head(7)


def senti_graph():
  df2 = pd.read_csv("2020-2013-FINALL.csv")
  df = pd.read_csv("2020-2023-BTC-FOR-SENTI.csv")
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  fig.add_trace(
    go.Bar(x=df2.Date,
           y=df2.Score,
           name="Sentiment Analysis",
           marker=dict(color='orange', line=dict(color='orange', width=2))),
    secondary_y=False,
  )
  fig.add_trace(
    go.Scatter(x=df.Date,
               y=df.Close,
               name="Bitcoin Close",
               line=dict(color='white', width=2)),
    secondary_y=True,
  )
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_layout(title=dict(text="Price and Sentiment movement",
                               font=dict(size=25)),
                    title_x=0.5)
  fig.update_xaxes(linecolor='#ea8b19',
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_yaxes(linecolor='#ea8b19',
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_xaxes(title_text="Date")
  fig.update_yaxes(title_text="Sentiment", secondary_y=False)
  fig.update_yaxes(title_text="Close Price", secondary_y=True)
  fig.update_layout(legend=dict(
    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_xaxes(
    rangeselector_bgcolor='#000',
    rangeselector_activecolor='#ea8b19',
    rangeslider_visible=False,
    rangeselector=dict(buttons=list([
      dict(count=1, label="1mo", step="month", stepmode="backward"),
      dict(count=3, label="3mo", step="month", stepmode="todate"),
      dict(count=6, label="6mo", step="month", stepmode="backward"),
      dict(count=1, label="1Y", step="year", stepmode="backward"),
      dict(step="all")
    ])))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  fig.update_layout(template='plotly_dark',
                    plot_bgcolor='rgb(17, 17, 17)',
                    hoverlabel=dict(font_size=16))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def twt_plot():
  temp = pd.read_csv('BAR-PLOT-TWT-COUNT.csv')
  fig = px.bar(temp,
               x="Sentiment",
               y="Tweet",
               color='Sentiment',
               color_discrete_sequence=px.colors.diverging.Spectral)
  fig.update_layout(plot_bgcolor='rgb(17, 17, 17)',
                    hoverlabel=dict(font_size=16, font=dict(color='white')))
  fig.update_layout(title=dict(text="TWEET CATEGORIES", font=dict(size=23)))
  fig.update_layout(xaxis_title="Sentiments",
                    yaxis_title="Tweet Count",
                    legend_title=None)
  fig.update_xaxes(linecolor='#ea8b19', gridcolor='rgb(17, 17, 17)')
  fig.update_yaxes(linecolor='#ea8b19', gridcolor='rgb(17, 17, 17)')
  fig.update_layout(template='plotly_dark',
                    legend=dict(orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1))
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def twt_year_plot():
  ed = pd.read_csv('YEAR-TWT-COUNT.csv')
  fig = px.bar(ed,
               x='Sentiment',
               y=["2020", "2021", "2022", "2023"],
               color_discrete_sequence=px.colors.diverging.Spectral)
  fig.update_layout(plot_bgcolor='rgb(17, 17, 17)',
                    hoverlabel=dict(font_size=16, font=dict(color='white')))
  fig.update_layout(title=dict(text="YEAR WISE TWEETS", font=dict(size=23)))
  fig.update_xaxes(linecolor='#ea8b19', gridcolor='rgb(17, 17, 17)')
  fig.update_yaxes(linecolor='#ea8b19', gridcolor='rgb(17, 17, 17)')
  fig.update_layout(xaxis_title="Sentiments",
                    yaxis_title="Tweet Count",
                    legend_title=None)
  fig.update_layout(template='plotly_dark',
                    legend=dict(orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1))
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def positive_pie():
  pos = pd.read_csv('POSITIVE-TWT.csv')
  fig = px.pie(pos,
               values='count',
               names='words',
               height=575,
               color_discrete_sequence=px.colors.diverging.Spectral)
  fig.update_layout(title=dict(text="UNIQUE POSITIVE WORDS",
                               font=dict(size=25)),
                    title_x=0.5)
  fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.4))
  fig.update_layout(template='plotly_dark',
                    legend={'itemsizing': 'constant'},
                    hoverlabel=dict(font_size=20))
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def negative_pie():
  neg = pd.read_csv('NEGATIVE-TWT.csv')
  fig = px.pie(neg,
               values='count',
               names='words',
               height=575,
               color_discrete_sequence=px.colors.diverging.Spectral)
  fig.update_layout(template='plotly_dark',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3),
                    hoverlabel=dict(font_size=20))
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_layout(title=dict(text="UNIQUE NEGATIVE WORDS",
                               font=dict(size=25)),
                    title_x=0.5)
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def crypto_graph(stock):
  df = pd.DataFrame(
    yf.download('BTC-USD', period='30d', interval='1h')['Close'])
  df2 = pd.DataFrame(
    yf.download(stock + '-USD', period='30d', interval='1h')['Close'])
  fig = make_subplots(specs=[[{"secondary_y": True}]])

  fig.add_trace(
    go.Scatter(x=df2.index,
               y=df2.Close,
               name="Bitcoin",
               line=dict(color='Orange', width=2)),
    secondary_y=False,
  )
  fig.add_trace(
    go.Scatter(x=df.index,
               y=df.Close,
               name=stock,
               line=dict(color='white', width=2)),
    secondary_y=True,
  )
  fig.update_layout(title_text="BTC againt " + stock, title_x=0.5)
  fig.update_xaxes(title_text="Date")
  fig.update_yaxes(title_text="Close Price", secondary_y=False)
  fig.update_xaxes(
    rangeselector_bgcolor='#000',
    rangeselector_activecolor='#ea8b19',
    rangeslider_visible=False,
    rangeselector=dict(buttons=list([
      dict(count=1, label="1d", step="day", stepmode="backward"),
      dict(count=5, label="5d", step="day", stepmode="backward"),
      dict(count=15, label="15d", step="day", stepmode="todate"),
      dict(count=25, label="25d", step="day", stepmode="backward"),
      dict(step="all")
    ])))
  fig.update_xaxes(linecolor='#ea8b19',
                   showticklabels=True,
                   showline=True,
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_yaxes(linecolor='#ea8b19',
                   showticklabels=False,
                   showline=True,
                   secondary_y=False,
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_yaxes(linecolor='#ea8b19',
                   showticklabels=False,
                   showline=False,
                   secondary_y=True,
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_layout(spikedistance=1000,
                    hoverdistance=100,
                    hovermode="x unified",
                    hoverlabel=dict(font_size=16))
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_layout(template='plotly_dark',
                    legend=dict(orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def BTC_crypto():
  fig = go.Figure()
  fig.add_trace(
    go.Scatter(x=df.index,
               y=df.Close,
               name="Bitcoin Close",
               line=dict(color='Orange', width=2)), )
  fig.update_layout(title_text="Bitcoin Price", title_x=0.5)
  fig.update_xaxes(title_text="Date")
  fig.update_yaxes(title_text="Close Price")
  fig.update_xaxes(
    rangeselector_bgcolor='#000',
    rangeselector_activecolor='#ea8b19',
    rangeslider_visible=False,
    rangeselector=dict(buttons=list([
      dict(count=1, label="1d", step="day", stepmode="backward"),
      dict(count=5, label="5d", step="day", stepmode="backward"),
      dict(count=15, label="15d", step="day", stepmode="todate"),
      dict(count=25, label="25d", step="day", stepmode="backward"),
      dict(step="all")
    ])))
  fig.update_layout(font=dict(
    family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    size=15))
  fig.update_xaxes(linecolor='#ea8b19',
                   showticklabels=True,
                   showline=True,
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_yaxes(linecolor='#ea8b19',
                   showticklabels=False,
                   showline=True,
                   gridcolor='rgb(17, 17, 17)',
                   showspikes=True,
                   spikecolor="#ea8b19",
                   spikethickness=1)
  fig.update_layout(spikedistance=1000,
                    hoverdistance=100,
                    hovermode="x unified",
                    hoverlabel=dict(font_size=16))
  fig.update_layout(
    plot_bgcolor='rgb(17, 17, 17)',
    hoverlabel=dict(font=dict(
      family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
      size=18)))
  fig.update_layout(template='plotly_dark',
                    showlegend=True,
                    legend=dict(orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1))

  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def crypto_coins():
  top_n = 100
  url = 'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym=USD'
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  dic = json.loads(soup.prettify())  # convert from json to dictionary

  data = dic['Data']
  n_records = len(data)
  coin = []
  Name = []
  price = []
  marketcap = []
  mc = []
  cs = []
  change = []
  for i in range(n_records):
    d = data[i]
    #print(d['CoinInfo']['Name'])
    try:
      coin.append(d['RAW']['USD']['FROMSYMBOL'])
      Name.append(d['CoinInfo']['FullName'])
      price.append(round(d['RAW']['USD']['PRICE'], 4))
      marketcap.append(d['DISPLAY']['USD']['MKTCAP'])
      mc.append(d['RAW']['USD']['CIRCULATINGSUPPLYMKTCAP'])
      cs.append(d['DISPLAY']['USD']['CIRCULATINGSUPPLY'])
      change.append(d['DISPLAY']['USD']['CHANGEPCTDAY'])
    #coin,Name, price, mktcap= d['RAW']['USD']['FROMSYMBOL'], d['CoinInfo']['FullName']   ,d['RAW']['USD']['PRICE'], d['RAW']['USD']['MKTCAP'],d['CoinInfo']['Url']
    except:
      None
  dict = {
    'Coin': coin,
    'Name': Name,
    'Price': price,
    'Market Cap': marketcap,
    'MC': mc,
    'Circulating Supply': cs,
    'Change %': change
  }
  df = pd.DataFrame(dict)
  df["Circulating Supply"] = df.apply(
    lambda row: row['Circulating Supply'].split(' ')[1], axis=1)
  df = df.sort_values(by=['MC'], ascending=False)
  df = df.drop(['MC'], axis=1)
  rd = pd.read_csv('files_path.csv', index_col=[0])
  coin = pd.merge(df, rd, on='Coin', how='left')
  coin.rename(columns={'images': ''}, inplace=True)
  coin = coin.loc[:, [
    "", "Coin", "Name", 'Price', 'Market Cap', 'Circulating Supply', 'Change %'
  ]]
  coin = coin.fillna('no.jpg')
  return coin


def scrape(date, number=5):
  # StoringInfo variables
  name, marketCap, price, circulatingSupply, symbol = [], [], [], [], []
  # URL to scrape
  url = 'https://coinmarketcap.com/historical/' + date
  # Request a website
  webpage = requests.get(url)
  # parse the text
  soup = BeautifulSoup(webpage.text, 'html.parser')

  # Get table row element
  tr = soup.find_all('tr', attrs={'class': 'cmc-table-row'})

  count = 0

  for row in tr:
    if count == number:
      break
    else:
      count += 1

      # Store name of the crypto currency
      name_col = row.find(
        'td',
        attrs={
          'class':
          'cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name'
        })
      cryptoname = name_col.find('a',
                                 attrs={
                                   'class':
                                   'cmc-table__column-name--name cmc-link'
                                 }).text.strip()

      # Market cap
      marketcap = row.find(
        'td',
        attrs={
          'class':
          'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'
        }).text.strip()

      # Price
      crytoprice = row.find(
        'td',
        attrs={
          'class':
          'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'
        }).text.strip()

      # Circulating supply and symbol
      circulatingSupplySymbol = row.find(
        'td',
        attrs={
          'class':
          'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply'
        }).text.strip()
      supply = circulatingSupplySymbol.split(' ')[0]
      sym = circulatingSupplySymbol.split(' ')[1]
      # append the data
      name.append(cryptoname)
      marketCap.append(marketcap)
      price.append(crytoprice)
      circulatingSupply.append(supply)
      symbol.append(sym)
  return name, marketCap, price, circulatingSupply, symbol


def trend_crypto():
  today = date.today()
  yesterday = str(today - timedelta(days=1))
  day = ''.join(filter(str.isdigit, yesterday))
  day = day + '/'
  td = pd.DataFrame()
  name, marketCap, price, circulatingSupply, symbol = scrape(day, number=5)
  td['Name'] = name
  td['MarketCap'] = marketCap
  td['Price'] = price
  td['CirculatingSupply'] = circulatingSupply
  td['Symbol'] = symbol
  rd = pd.read_csv('files_path.csv', index_col=[0])
  rd.rename(columns={'Coin': 'Symbol'}, inplace=True)

  yu = pd.merge(td, rd, on='Symbol', how='left')
  yu = yu.fillna('nan')
  yu.rename(columns={'images': ''}, inplace=True)
  yu['rank'] = range(1, 1 + len(yu))
  yu["CirculatingSupply"] = yu.apply(
    lambda row: re.sub(",", "", row.CirculatingSupply), axis=1)
  yu["Circulating Supply"] = yu.apply(
    lambda row: numerize.numerize(int(row.CirculatingSupply)), axis=1)
  yu["MarketCap"] = yu.apply(lambda row: re.sub(",", "", row.MarketCap),
                             axis=1)
  yu["Market Cap"] = yu.apply(lambda row: row.MarketCap[0] + str(
    numerize.numerize(float(row.MarketCap[1:]))),
                              axis=1)
  yu["Price"] = yu.apply(lambda row: re.sub(",", "", row.Price), axis=1)
  yu["Price"] = yu.apply(
    lambda row: row.Price[0] + str(numerize.numerize(float(row.Price[1:]))),
    axis=1)
  yu = yu.loc[:, [
    "", "Symbol", 'Price', 'Market Cap', 'Circulating Supply', "rank"
  ]]
  return yu


api_key = "402aa7508d3f4fe4b44d0a33a29a1f82"
url = "https://openexchangerates.org/api/latest.json?app_id=" + api_key + "&show_alternative=1"
response = requests.get(url)
data = response.json()
exchange_rates = data["rates"]


def convert_data(base, to, amount):
  org = int(amount) / exchange_rates[base.upper()]
  cov = org * exchange_rates[to.upper()]
  return str(numerize.numerize(cov))


def crypto_convert():
  crypto = ['BTC', 'ETH', 'XMR', 'LTC', 'DASH', 'XRP', 'DOGE']
  curr = ['INR', 'USD', 'AUD', 'EUR', 'AED', 'XAU']
  cryo = pd.DataFrame()
  amount = 1
  tab = []
  for row in crypto:
    r1 = []
    for col in curr:
      org = amount / exchange_rates[row.upper()]
      cov = org * exchange_rates[col.upper()]
      r1.append(round(cov, 4))
    tab.append(r1)

  df = pd.DataFrame(tab,
                    columns=['INR', 'USD', 'AUD', 'EUR', 'AED', 'XAU'],
                    index=['BTC', 'ETH', 'XMR', 'LTC', 'DASH', 'XRP', 'DOGE'])
  df["Crypto"] = df.index
  df = df.reset_index(drop=True)
  rd = pd.read_csv('files_path.csv', index_col=[0])
  rd.rename(columns={'Coin': 'Crypto'}, inplace=True)
  yu = pd.merge(df, rd, on='Crypto', how='left')
  yu.rename(columns={'images': ''}, inplace=True)
  df = yu.loc[:, ["", 'INR', 'USD', 'AUD', 'EUR', 'AED', 'XAU']]
  return df


def crypto_coin_dropdown():
  rd = pd.read_csv('coins.csv', index_col=[0])
  return rd


def currency_dropdown():
  rd = pd.read_csv('currency.csv', index_col=[0])
  return rd
