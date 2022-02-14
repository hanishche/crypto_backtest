import requests 
import pandas as pd
import schedule
import time
from pytz import timezone
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfFile,PdfPages
import seaborn as sns
import pywhatkit as pywt
import threading
import keyboard

def EMA_hr(crypto,hour):
    url ='https://min-api.cryptocompare.com/data/v2/histohour?fsym={}&tsym=USD&aggregate={}'.format(crypto,hour) #&aggregate=1
    response = requests.get(url)
    data = response.json()
    data=pd.DataFrame(data['Data']['Data'])
    data['date_time']=pd.to_datetime(data['time'], unit='s').apply(lambda x: (x+timedelta(minutes = 330)))
    data=data.sort_values(by='date_time',ascending=False).reset_index().drop(['index','time','conversionType','conversionSymbol'],axis=1)
    data['EMA_13']=data['close'].ewm(span=13, adjust=False).mean()
    data['EMA_10']=data['close'].ewm(span=10, adjust=False).mean()
    data['diff']=data['EMA_10'].astype(float)-data['EMA_13'].astype(float)
    data['mins']=60 
    data['last_updated']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_10_13=data
    return data_10_13
    
def EMA_1min(crypto,mins,epoch):
  url ='https://min-api.cryptocompare.com/data/v2/histominute?fsym={}&tsym=USD&aggregate={}&toTs={}'.format(crypto,mins,epoch) #&aggregate=1
  response = requests.get(url)
  data = response.json()
  data=pd.DataFrame(data['Data']['Data'])
  data['date_time']=pd.to_datetime(data['time'], unit='s').apply(lambda x: (x+timedelta(minutes = 330)))
  data=data.sort_values(by='date_time',ascending=False).reset_index().drop(['index','time','conversionType','conversionSymbol'],axis=1)
  data['EMA_13']=data['close'].ewm(span=13, adjust=False).mean()
  data['EMA_10']=data['close'].ewm(span=10, adjust=False).mean()
  data['diff']=data['EMA_10'].astype(float)-data['EMA_13'].astype(float)
  data['mins']=mins
  data['last_updated']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     try:
#         url ='https://www.alphavantage.co/query?function=RSI&symbol={}USD&interval=1min&time_period=6&series_type=close&apikey=VMX46JR35MS4J31X'.format('MATIC')
#         response = requests.get(url)
#         data_RSI = response.json()
#         data_RSI=pd.DataFrame(data_RSI['Technical Analysis: RSI']).T.reset_index()
#         data_RSI['index']=pd.to_datetime(data_RSI['index']).apply(lambda x: (x+timedelta(minutes = 630)))
#         data_RSI.columns=['date_time','RSI']
#         data=pd.merge(data,data_RSI,how='inner',on='date_time')
#     except:
#         data['RSI']=None

  data_10_13=data
  return data_10_13
  
def EMA_1d(crypto,days):
    url ='https://min-api.cryptocompare.com/data/v2/histoday?fsym={}&tsym=USD'.format(crypto) #&aggregate=1
    response = requests.get(url)
    data = response.json()
    data=pd.DataFrame(data['Data']['Data'])
    data['date_time']=pd.to_datetime(data['time'], unit='s').apply(lambda x: (x+timedelta(minutes = 330)))
    data=data.sort_values(by='date_time',ascending=False).reset_index().drop(['index','time','conversionType','conversionSymbol'],axis=1)
    data['EMA_13']=data['close'].ewm(span=13, adjust=False).mean()
    data['EMA_10']=data['close'].ewm(span=10, adjust=False).mean()
    data['diff']=data['EMA_10'].astype(float)-data['EMA_13'].astype(float)
    data['mins']=days
    data['last_updated']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     try:
#         url ='https://www.alphavantage.co/query?function=RSI&symbol={}USD&interval=1min&time_period=6&series_type=close&apikey=VMX46JR35MS4J31X'.format('MATIC')
#         response = requests.get(url)
#         data_RSI = response.json()
#         data_RSI=pd.DataFrame(data_RSI['Technical Analysis: RSI']).T.reset_index()
#         data_RSI['index']=pd.to_datetime(data_RSI['index']).apply(lambda x: (x+timedelta(minutes = 630)))
#         data_RSI.columns=['date_time','RSI']
#         data=pd.merge(data,data_RSI,how='inner',on='date_time')
#     except:
#         data['RSI']=None
        
    data_10_13=data
    return data_10_13
    
