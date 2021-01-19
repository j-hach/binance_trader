from app.BinanceAPI import BinanceAPI
import pandas as pd
import datetime as dt
import time
import numpy as np


binanceAPI = BinanceAPI('','')
fee_rate = .001 * 0.75
bps = abs(1-((1-fee_rate)**2))



def ema(L, alpha=None):
    """
       here we use 'exponential moving average' to predict the next time period data value
    # EMA Formula:
         X(0),X(1),X(2),...,X(t-1) : data-sets total with "t" time-period-points
         EMA(1) = X(0) // initial point            -> 1 terms
         EMA(2) = EMA(1) + alpha*(X(1)-EMA(1))
                = alpha*[X(1)] + (1-alpha)*X(0)    -> 2 terms
         EMA(3) = EMA(2) + alpha*[X(2)-EMA(2)]
                = [alpha*X(1)+(1-alpha)*X(0)] + alpha*[X(2)-(alpha*X(1)+(1-alpha)*X(0))]
                = alpha*[X(2)+(1-alpha)*X(1)] + (1-alpha-alpha-alpha^2)*X(0)
                = alph*[X(2)+(1-alpha)*X(1)] + (1-alpha)^2*X(0)     -> 3 terms
           .
           .
         EMA(t) = alpha*X(t-1) + (1-alpha)*EMA(t-1) = EMA(t-1) + alpha*[X(t-1) - EMA(t-1)]
                  = ...
                                    1st               2nd                     3rd                            (t-1)-th
                  = alpha*[ (1-alpha)^(0)*X(t-1) + (1-alpha)^(1)*X(t-2) + (1-alpha)^(2)*X(t-3) + ...+ (1-alpha)^(t-2)*X(t-(t-1)) ]
                            t-th
                    + (1-alpha)^(t-1)*X(0)
         alpha = 1 /(number of data-points)
         where alpha: smoothing factor
               X(t-1) is observation value at time (t-1) period
               EMA(t-1) is prediction value at time (t-1) periods
               EMA(t) is prediction value at time t periods
    """
    ema_data = []
    if not alpha:
       alpha = 1/(len(L)+1.25) # defaults
    if (alpha<0) or (alpha>1):
       raise ValueError("0 < smoothing factor <= 1")
    alpha_bar = float(1-alpha)
    
    """ generate [x(0)], [x(1),x(0)], [x(2),x(1),x(0)],.... """
    num_terms_list = [sorted(L[:i],reverse=True) for i in range(1,len(L)+1)]
    #print num_terms_list
    #return 
    for nterms in num_terms_list:
        # calculate 1st~(t-1)-th terms corresponding exponential factor
        pre_exp_factor = [float(alpha_bar**(i-1)) for i in range(1,len(nterms))]
        # calculate the ema at the next time periods
        ema_data.append(alpha*float(sum(float(a)*float(b) for a,b in zip(tuple(pre_exp_factor), tuple(nterms[:-1])))) + \
                         (alpha_bar**(len(nterms)-1))*float(nterms[-1]))
    return ema_data

def compare_current_px(price):
    price = binanceAPI.get_ticker('BTCUSDT')
    current_price = float(price['lastPrice'])
    avg_price = round(float(price['weightedAvgPrice']),4)
    high_price = float(price['highPrice'])
    low_price = float(price['lowPrice'])
    print('last: ', current_price)
    print('from the avg price: ', round((current_price-avg_price)/avg_price*100,4) , '% (', avg_price, ')')
    print('from the high price: ', round((current_price-high_price)/high_price*100,4) , '% (', high_price, ')')
    print('from the low price: ', round((current_price-low_price)/low_price*100,4) , '% (', low_price, ')')

def get_historical(market,interval):
    result=binanceAPI.get_kline(market, interval,1000)
    columns=['start_time','open','high','low','close','volume','end_time',
             'base_asset_volume','no_of_trades','taker_volume',
             'taker_buy_base_asset_volume','none']
    df = pd.DataFrame(result, columns=columns)
    print(df['close'])
    return df['close']


'''
algo:
    initialize and get EMA-50 and EMA-200
    buy if EMA-50 < EMA-200
    sell if EMA-50 > EMA-200
    
    

'''

price=[1,34,2,5,6,7,67]

btc_usdt_hist = get_historical('BTCUSDT','5m')
print(ema(btc_usdt_hist))
# while True:
#     current_price = binanceAPI.get_price('BTCUSDT')['price']
#     print(dt.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]'),current_price)
    # print(binanceAPI.get_ticker('BTCUSDT')['weightedAvgPrice'])
    # print(binanceAPI.get_ticker('BTCUSDT')['highPrice'])
    # print(binanceAPI.get_ticker('BTCUSDT')['lowPrice'])
    # if float(current_price) > 36000:
        # print('tell me if it passed 36000!')
    # else:
    #     print('bored struggling below')1

    # # triangle arb
    # btcusdt=float(binanceAPI.get_price('BTCUSDT')['price'])
    # bnbbtc=float(binanceAPI.get_price('UNFIBTC')['price'])
    # bnbusdt=float(binanceAPI.get_price('UNFIUSDT')['price'])

    # print(dt.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]'))
    # # print('btc/usdt:',btcusdt)
    # # print('bnb/btc:',bnbbtc)
    # # print('bnb/usdt:',bnbusdt)
    # print('get:',1/btcusdt/bnbbtc*bnbusdt)
    # spread = 1-1/btcusdt/bnbbtc*bnbusdt
    # print('spread:',spread)
    # if bps > abs(spread):
    #     print('cannot arb, fees:',bps,'vs profit:',spread)
    # else:
    #     print('can arb, fees:',bps,'vs profit:',spread)
    # time.sleep(1)
    
    
    
    