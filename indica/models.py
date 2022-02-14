#!/usr/bin/env python
# coding: utf-8

# In[6]:


import warnings
warnings.simplefilter("ignore")
import pandas as pd
import numpy as np

def RSI_model_perf(Wallet_bal,sl:0.02,data,column,LL,UL):
    list_BS=[]
    i=0
    j=0
    for row in range(0,len(data)):
        while (i<row+1) and (j<len(data)) :
            qty=Wallet_bal/data['close'][j]
            Wallet_bal1=qty%data['close'][j]
            if data[column][j]<=LL:
                list_BS.append((j,data['date_time'][j]
                                ,data[column][j]
                                ,data['open'][j]
                                ,data['close'][j]
                                ,qty
                                ,qty*data['close'][j]
                                ,0
                                ,Wallet_bal1
                                ,'Buy'
                                ,None
                                ,None
                               ,(qty*data['close'][j])*0.002
                               ))
                k=j
                i+=1

            else:
                k='NA'
            j+=1
            while (k!='NA') and ((j>k) and (j<len(data))):
                if sl==0:
                    if (data[column][j]>=UL):  # | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[column][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'RSI_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'
                else:
                    if (data[column][j]>=UL) | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[column][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'Sold by SL' if (data['close'][j]<=(1-sl)*data['close'][k]) else 'RSI_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'

                j+=1

    try:
        df=pd.DataFrame(list_BS,columns=['index','date_time','{}'.format(column),'open','close','qty','invest','profit','wallet_bal','tag','win','Sold_Status','Txn_fee'])
        df['Model']='RSI'
        if df.iloc[-1]['tag']=='Buy':
            df=(df.drop(len(df)-1,axis=0))

        if df[df['win']=='win'].empty:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win']=0
            win['win%']=0
            win['max_profit%']=0
        else:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win%']=round((df['win'].value_counts()['win']/df['win'].value_counts().sum())*100,2)
            win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100

        
        win['max_profit']=df['profit'].max()
        win['max_loss']=df['profit'].min()
        win['profit@endofdaterange']=df['wallet_bal'].iloc[-1:].values[0]-df['invest'].iloc[:1].values[0]
        win['profit@endofdaterange%']=((df['wallet_bal'].iloc[-1:].values[0]/df['invest'].iloc[:1].values[0])-1)*100
        win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100
        win['max_loss%']=((df.iloc[df[df['profit']==df['profit'].min()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].min()].index-1]['invest'].values[0])-1)*100
        win['Txn_fee']=df['Txn_fee'].sum()
        win['overall_profit']=win['profit@endofdaterange']-win['Txn_fee']
        win=win.rename(index={'win': '{}'.format('RSI')})
    except:
        win=pd.DataFrame(columns=['Error'],index=['win'])
        win['Error']='Data Insufficient'
        win=win.rename(index={'win': '{}'.format('RSI')})
    
    return win,df



def RSI_EMA_10_13_model_perf(Wallet_bal,sl:0.02,data,RSI_column,EMA_column,LL,UL):
    list_BS=[]
    i=0
    j=0
    for row in range(0,len(data)):
        while (i<row+1) and (j+1<len(data)) :
            qty=Wallet_bal/data['close'][j]
            Wallet_bal1=qty%data['close'][j]
            if (data[RSI_column][j]<=LL) & ((data[EMA_column][j+1]>0) & (data[EMA_column][j]<0)):
                list_BS.append((j,data['date_time'][j]
                                ,data[RSI_column][j]
                                ,data[EMA_column][j]
                                ,data['open'][j]
                                ,data['close'][j]
                                ,qty
                                ,qty*data['close'][j]
                                ,0
                                ,Wallet_bal1
                                ,'Buy'
                                ,None
                                ,None
                               ,(qty*data['close'][j])*0.002
                               ))
                k=j
                i+=1

            else:
                k='NA'
            j+=1
            while (k!='NA') and ((j>k) and (j+1<len(data))):
                if sl==0:
                    if ((data[RSI_column][j]>=UL) & ((data[EMA_column][j+1]<0) and (data[EMA_column][j]>0))): # | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[RSI_column][j]
                                        ,data[EMA_column][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'RSI_EMA_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'
                else:
                        if ((data[RSI_column][j]>=UL) & ((data[EMA_column][j+1]<0) and (data[EMA_column][j]>0))) | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                            list_BS.append((j,data['date_time'][j]
                                            ,data[RSI_column][j]
                                            ,data[EMA_column][j]
                                            ,data['open'][j]
                                            ,data['close'][j]
                                            ,qty
                                            ,0
                                            ,qty*data['close'][j]-qty*data['close'][k]
                                            ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                            ,'Sell'
                                            ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                            ,'Sold by SL' if (data['close'][j]<=(1-sl)*data['close'][k]) else 'RSI_EMA_SOLD'
                                            ,(qty*data['close'][j])*0.002
                                           ))

                            Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                            k='NA'
                

                j+=1

    try:
        df=pd.DataFrame(list_BS,columns=['index','date_time','{}'.format(RSI_column),'{}'.format(EMA_column),'open','close','qty','invest','profit','wallet_bal','tag','win','Sold_Status','Txn_fee'])
        df['Model']='RSI_EMA_10_13'
        if df.iloc[-1]['tag']=='Buy':
            df=(df.drop(len(df)-1,axis=0))

        if df[df['win']=='win'].empty:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win']=0
            win['win%']=0
            win['max_profit%']=0
        else:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win%']=round((df['win'].value_counts()['win']/df['win'].value_counts().sum())*100,2)
            win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100

        
        win['max_profit']=df['profit'].max()
        win['max_loss']=df['profit'].min()
        win['profit@endofdaterange']=df['wallet_bal'].iloc[-1:].values[0]-df['invest'].iloc[:1].values[0]
        win['profit@endofdaterange%']=((df['wallet_bal'].iloc[-1:].values[0]/df['invest'].iloc[:1].values[0])-1)*100
        win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100
        win['max_loss%']=((df.iloc[df[df['profit']==df['profit'].min()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].min()].index-1]['invest'].values[0])-1)*100
        win['Txn_fee']=df['Txn_fee'].sum()
        win['overall_profit']=win['profit@endofdaterange']-win['Txn_fee']
        win=win.rename(index={'win': '{}'.format('RSI_EMA_10_13')})
    except:
        win=pd.DataFrame(columns=['Error'],index=['win'])
        win['Error']='Data Insufficient'
        win=win.rename(index={'win': '{}'.format('RSI_EMA_10_13')})
    return win,df



def EMA_10_13_model_perf(Wallet_bal,sl:0.02,data,column):
    list_BS=[]
    i=0
    j=0
    for row in range(0,len(data)):
        while (i<row+1) and (j+1<len(data)) :
            qty=Wallet_bal/data['close'][j]
            Wallet_bal1=qty%data['close'][j]
            if ((data[column][j+1]>0) & (data[column][j]<0)):
                list_BS.append((j,data['date_time'][j]
                                ,data[column][j]
                                ,data['open'][j]
                                ,data['close'][j]
                                ,qty
                                ,qty*data['close'][j]
                                ,0
                                ,Wallet_bal1
                                ,'Buy'
                                ,None
                                ,None
                               ,(qty*data['close'][j])*0.002))
                k=j
                i+=1

            else:
                k='NA'
            j+=1
            while (k!='NA') and ((j>k) and (j+1<len(data))):
                if sl==0:
                    if ((data[column][j+1]<0) and (data[column][j]>0) and (data['close'][j]>=data['close'][k])):  #  | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[column][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'EMA_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'
                else:
                    if ((data[column][j+1]<0) and (data[column][j]>0) and (data['close'][j]>=data['close'][k])) | (data[column][j]<=(1-sl)*data[column][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[column][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'Sold by SL' if (data['close'][j]<=(1-sl)*data['close'][k]) else 'EMA_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'

                j+=1

    try:
        df=pd.DataFrame(list_BS,columns=['index','date_time','{}'.format(column),'open','close','qty','invest','profit','wallet_bal','tag','win','Sold_Status','Txn_fee'])
        df['Model']='EMA_10_13'
        if df.iloc[-1]['tag']=='Buy':
            df=(df.drop(len(df)-1,axis=0))

        if df[df['win']=='win'].empty:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win']=0
            win['win%']=0
            win['max_profit%']=0
        else:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win%']=round((df['win'].value_counts()['win']/df['win'].value_counts().sum())*100,2)
            win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100

        
        win['max_profit']=df['profit'].max()
        win['max_loss']=df['profit'].min()
        win['profit@endofdaterange']=df['wallet_bal'].iloc[-1:].values[0]-df['invest'].iloc[:1].values[0]
        win['profit@endofdaterange%']=((df['wallet_bal'].iloc[-1:].values[0]/df['invest'].iloc[:1].values[0])-1)*100
        win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100
        win['max_loss%']=((df.iloc[df[df['profit']==df['profit'].min()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].min()].index-1]['invest'].values[0])-1)*100
        win['Txn_fee']=df['Txn_fee'].sum()
        win['overall_profit']=win['profit@endofdaterange']-win['Txn_fee']
        win=win.rename(index={'win': '{}'.format('EMA_10_13')})
    except:
        win=pd.DataFrame(columns=['Error'],index=['win'])
        win['Error']='Data Insufficient'
        win=win.rename(index={'win': '{}'.format('EMA_10_13')})
   
    return win,df


def MACD_Crossover_model_perf(Wallet_bal,sl:0.02,data,column):    
    list_BS=[]
    i=0
    j=0
    for row in range(0,len(data)):
        while (i<row+1) and (j+1<len(data)) :
            qty=Wallet_bal/data['close'][j]
            Wallet_bal1=qty%data['close'][j]
            if (data[column][j+1]>0) & (data[column][j]<0):
                list_BS.append((j,data['date_time'][j]
                                ,data[column][j]
                                ,data['open'][j]
                                ,data['close'][j]
                                ,qty
                                ,qty*data['close'][j]
                                ,0
                                ,Wallet_bal1
                                ,'Buy'
                                ,None
                                ,None
                               ,(qty*data['close'][j])*0.002
                               ))
                k=j
                i+=1

            else:
                k='NA'
            j+=1
            while (k!='NA') and ((j>k) and (j+1<len(data))):
                if sl==0:
                    if (data[column][j+1]<0) & (data[column][j]>0):  #  | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[column][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'MACD_CO_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'
                else:
                    if ((data[column][j+1]<0) & (data[column][j]>0)) | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[column][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'Sold by SL' if (data['close'][j]<=(1-sl)*data['close'][k]) else 'MACD_CO_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'

                j+=1

    try:
        df=pd.DataFrame(list_BS,columns=['index','date_time','{}'.format(column),'open','close','qty','invest','profit','wallet_bal','tag','win','Sold_Status','Txn_fee'])
        df['Model']='MACD_CO'
        if df.iloc[-1]['tag']=='Buy':
            df=(df.drop(len(df)-1,axis=0))

        if df[df['win']=='win'].empty:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win']=0
            win['win%']=0
            win['max_profit%']=0
        else:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win%']=round((df['win'].value_counts()['win']/df['win'].value_counts().sum())*100,2)
            win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100


        win['max_profit']=df['profit'].max()
        win['max_loss']=df['profit'].min()
        win['profit@endofdaterange']=df['wallet_bal'].iloc[-1:].values[0]-df['invest'].iloc[:1].values[0]
        win['profit@endofdaterange%']=((df['wallet_bal'].iloc[-1:].values[0]/df['invest'].iloc[:1].values[0])-1)*100
        win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100
        win['max_loss%']=((df.iloc[df[df['profit']==df['profit'].min()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].min()].index-1]['invest'].values[0])-1)*100
        win['Txn_fee']=df['Txn_fee'].sum()
        win['overall_profit']=win['profit@endofdaterange']-win['Txn_fee']
        win=win.rename(index={'win': '{}'.format('MACD_CO')})
        
    except:
        win=pd.DataFrame(columns=['Error'],index=['win'])
        win['Error']='Data Insufficient'
        win=win.rename(index={'win': '{}'.format('MACD_CO')})
    
    return win,df




def MACD_ZL_Crossover_model_perf(Wallet_bal,sl:0.02,data,macd_line,macd_cross):    
    list_BS=[]
    i=0
    j=0
    for row in range(0,len(data)):
        while (i<row+1) and (j+1<len(data)) :
            qty=Wallet_bal/data['close'][j]
            Wallet_bal1=qty%data['close'][j]
            if (data[macd_cross][j]>0) & (data[macd_line][j]>0):
                list_BS.append((j,data['date_time'][j]
                                ,data[macd_line][j]
                                ,data[macd_cross][j]
                                ,data['open'][j]
                                ,data['close'][j]
                                ,qty
                                ,qty*data['close'][j]
                                ,0
                                ,Wallet_bal1
                                ,'Buy'
                                ,None
                                ,None
                               ,(qty*data['close'][j])*0.002
                               ))
                k=j
                i+=1

            else:
                k='NA'
            j+=1
            while (k!='NA') and ((j>k) and (j+1<len(data))):
                if sl==0:
                    if (data[macd_cross][j]<0) & (data[macd_line][j]<0):  #  | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[macd_line][j]
                                        ,data[macd_cross][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'MACD_ZL_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'
                else:
                    if ((data[macd_cross][j]<0) & (data[macd_line][j]<0)) | (data['close'][j]<=(1-sl)*data['close'][k]):  # | (pl>=((data['close'][j]/data['close'][k])-1)*100)
                        list_BS.append((j,data['date_time'][j]
                                        ,data[macd_line][j]
                                        ,data[macd_cross][j]
                                        ,data['open'][j]
                                        ,data['close'][j]
                                        ,qty
                                        ,0
                                        ,qty*data['close'][j]-qty*data['close'][k]
                                        ,Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                                        ,'Sell'
                                        ,'win' if (qty*data['close'][j]-qty*data['close'][k])>0 else 'lose' if (qty*data['close'][j]-qty*data['close'][k])<=0 else None
                                        ,'Sold by SL' if (data['close'][j]<=(1-sl)*data['close'][k]) else 'MACD_ZL_SOLD'
                                        ,(qty*data['close'][j])*0.002
                                       ))

                        Wallet_bal=Wallet_bal+(qty*data['close'][j]-qty*data['close'][k])
                        k='NA'

                j+=1

    try:
        df=pd.DataFrame(list_BS,columns=['index','date_time','{}'.format(macd_line),'{}'.format(macd_cross),'open','close','qty','invest','profit','wallet_bal','tag','win','Sold_Status','Txn_fee'])
        df['Model']='MACD_ZL_CO'
        if df.iloc[-1]['tag']=='Buy':
            df=(df.drop(len(df)-1,axis=0))

        if df[df['win']=='win'].empty:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win']=0
            win['win%']=0
            win['max_profit%']=0
        else:
            win=pd.DataFrame(df['win'].value_counts()).T
            win['win%']=round((df['win'].value_counts()['win']/df['win'].value_counts().sum())*100,2)
            win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100

        
        win['max_profit']=df['profit'].max()
        win['max_loss']=df['profit'].min()
        win['profit@endofdaterange']=df['wallet_bal'].iloc[-1:].values[0]-df['invest'].iloc[:1].values[0]
        win['profit@endofdaterange%']=((df['wallet_bal'].iloc[-1:].values[0]/df['invest'].iloc[:1].values[0])-1)*100
        win['max_profit%']=((df.iloc[df[df['profit']==df['profit'].max()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].max()].index-1]['invest'].values[0])-1)*100
        win['max_loss%']=((df.iloc[df[df['profit']==df['profit'].min()].index]['wallet_bal'].values[0]/df.iloc[df[df['profit']==df['profit'].min()].index-1]['invest'].values[0])-1)*100
        win['Txn_fee']=df['Txn_fee'].sum()
        win['overall_profit']=win['profit@endofdaterange']-win['Txn_fee']
        win=win.rename(index={'win': '{}'.format('MACD_ZL_CO')})
    except:
        win=pd.DataFrame(columns=['Error'],index=['win'])
        win['Error']='Data Insufficient'
        win=win.rename(index={'win': '{}'.format('MACD_ZL_CO')})

    return win,df


# In[ ]:




