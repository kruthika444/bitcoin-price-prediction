# importing Flask and other modules
from flask import Flask, request, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf  
from btc import *
# Flask constructor
app = Flask(__name__)  
 

@app.route('/',methods =["GET", "POST"])
def home():
    grf=graph_normal()
    rad1='checked'
    dis1,dis2,rad2='' ,'' ,'' 
    if request.method == "POST":
        # getting input with name = fname in HTML form
        val = request.form.get("chart")
        if val=="1": 
            grf=graph_normal() 
            dis1='disabled'
            rad1='checked'
        elif val=="2":
            dis2='disabled'
            rad2='checked'
            grf=graph_candle_stick()
            
    df=btc_price()
    pd_df=past_btc()
    head=pd_df

    return render_template("home.html",column_names=df.columns.values, 
                           row_data=list(df.values.tolist()), graphJSON=grf
                           ,head_c=head.columns.values, 
                          head_r=list(head.values.tolist())
                          ,zip=zip,rad2=rad2,rad1=rad1)

@app.route('/prediction',methods =["GET", "POST"])
def prediction():
    today=today_price()
    tmro=tmro_price() 
    graph=pred_graph()
    today_date=date.today().strftime('%d-%m-%Y')
    tmro_date=(date.today() + timedelta(days=1)).strftime('%d-%m-%Y') 
    week=pred_week()
    return render_template("pred.html",today=today,tmro=tmro,graphJSON=graph
            ,today_date=today_date,tmro_date=tmro_date,week_c=week.columns.values, 
         week_r=list(week.values.tolist()),zip=zip)

@app.route('/sentiment',methods =["GET", "POST"])
def sentiment(): 
    senti=senti_graph()
    twt=twt_plot()
    year_twt=twt_year_plot()
    pos=positive_pie()
    neg=negative_pie()
    return render_template('senti.html',senti=senti,twt=twt,year_twt=year_twt,
                           pos=pos,neg=neg)

@app.route('/crypto',methods =["GET", "POST"])
def crypto(): 
    graph=BTC_crypto() 
    if request.method == "POST":
        val = request.form.get("chart") 
        graph=crypto_graph(val) 
    df=crypto_coins() 
    trend=trend_crypto() 
    dropdown=crypto_coin_dropdown()
    return render_template('crypto.html',graph=graph,column_names=df.columns.values, 
                           row_data=list(df.values.tolist()),
                           trend_col=trend.columns.values, 
                          trend_row=list(trend.values.tolist()),
                          col_dd=dropdown.columns.values, 
                          row_dd=list(dropdown.values.tolist()),
                           zip=zip,img_col='',pic='')

@app.route('/convert',methods =["GET", "POST"])
def convert(): 
    if request.method == "POST": 
        base = request.form.get("base") 
        to=request.form.get('to')
        amount=request.form.get('money')  
    else:
        base,to,amount='BTC','INR',1
    crypto=convert_data(base, to, amount)
    trend=crypto_convert() 
    dropdown=currency_dropdown()
    return render_template('convertor.html',trend_col=trend.columns.values, 
            trend_row=list(trend.values.tolist()),base=base,to=to,amount=amount,
            col_dd=dropdown.columns.values,row_dd=list(dropdown.values.tolist()),
    zip=zip,img_col='',pic='',crypto=crypto)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    
    
    
    
    