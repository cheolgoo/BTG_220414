import time
import pyupbit
import datetime
import numpy as np
import datetime
from datetime import datetime


access = "BgyVpvO8MOEmDg7j1XocJq4xcrSWYoShtAvlteJ2"
secret = "zlYA1hl4Dxguqei2xRXEf2eDEglibSitxcu5oxun"


# 로그인
upbit = pyupbit.Upbit(access, secret)


# 파라미터 ( BTG 5minute )

buy_count   = 0 
buy_vol     = 0 
buy_price   = 0 
buy_num     = 0


sum_n       = 3
sum_perc    = 0.95/100
up          = 0.65/100
num_limit   = 6.7* 60 /5 

short_in    = 0 
up_in       = 2 / 100
up_low      = 1 / 100 

# time check 초기화
OHLCV_temp  = pyupbit.get_ohlcv(ticker="KRW-BTG", interval='minute5', count=sum_n+2, to=None, period=0.1)
time_prev   = np.array( [OHLCV_temp.index[-2], OHLCV_temp.index[-1]] ) # [0] : 과거, [1] : 최근

# autotrade start
while True:
    
    time.sleep(2)

    now         = datetime.now()
    now_h       = now.hour
    now_m       = now.minute
    now_time    = now_h *100 + now_m



    if ( buy_count == 0 ) :

        if ( 855<now_time and now_time<857 ) :

            OHLCV_temp2  = pyupbit.get_ohlcv(ticker="KRW-BTG", interval='minute30', count=5, to=None, period=0.1)
            OHLCV2       = OHLCV_temp2.to_numpy()
            open2         = OHLCV2[0:,0]
            close2       = OHLCV2[0:,3]
            delta2       = close2 - open2

            sum_check2 = np.sum( delta2 ) 

            
            if (sum_check2 < 0.5/ 100 * close[-1] ) : 

                short_in = 1

                balance     = upbit.get_balance("KRW")

                buy_price    = pyupbit.get_current_price("KRW-BTG")
                buy_vol      = balance / pyupbit.get_current_price("KRW-BTG")
                upbit.buy_market_order("KRW-BTG", balance*0.999 )

                buy_count    = 1 
                buy_num      = 1 

        
    if (short_in == 1):

        if ( pyupbit.get_current_price("KRW-BTG") < buy_price * (1 - up_low) )  or ( pyupbit.get_current_price("KRW-BTG") > buy_price * (1 + up_in) )  or  ( 930<now_time and now_time<932  ) :


            BTG_balance  = upbit.get_balance("KRW-BTG") 
            upbit.sell_market_order("KRW-BTG", BTG_balance*0.999)
                    

            buy_count    = 0 
            buy_num      = 0 
            buy_vol      = 0


            short_in     = 0    
            time.sleep(5*60)


    if (short_in == 0): 
    
        try :

            OHLCV_temp  = pyupbit.get_ohlcv(ticker="KRW-BTG", interval='minute5', count=sum_n+2, to=None, period=0.1)
            time_new    = np.array( [OHLCV_temp.index[-2], OHLCV_temp.index[-1]] )
        


            if ( time_prev[0] != time_new[0] ) :

                # time count
                if ( buy_count != 0 ) :
                    buy_num  =  buy_num + 1
                

            
                # get open, close, delta
                time_prev   = time_new
                OHLCV       = OHLCV_temp.to_numpy()
                open        = OHLCV[0:-1,0]
                close       = OHLCV[0:-1,3]
                delta       = close - open
        

                sum_check = np.sum( delta ) 

                if (sum_check < -open[-1]*sum_perc)  & (buy_count == 0) :  

                        balance     = upbit.get_balance("KRW")

                        buy_price    = pyupbit.get_current_price("KRW-BTG")
                        buy_vol      = balance / pyupbit.get_current_price("KRW-BTG")
                        upbit.buy_market_order("KRW-BTG", balance*0.999 )

                        buy_count    = 1 
                        buy_num      = 1 
                        
                        


                # sell (실제buy_market한 것과 get_current한 값의 차이가 있을 수도 있는데, 약간의 BTG를 사놓으면 문제 없을듯함)

            if ( buy_count != 0 ) :

                if ( pyupbit.get_current_price("KRW-BTG") > buy_price * (1 + up) )  or  ( buy_num >= num_limit  ) :


                    BTG_balance  = upbit.get_balance("KRW-BTG") 
                    upbit.sell_market_order("KRW-BTG", BTG_balance*0.999)
                        

                    buy_count    = 0 
                    buy_num      = 0 
                    buy_vol      = 0

                    if (  upbit.get_balance("KRW-BTG") > 1) :
                        left = upbit.get_balance("KRW-BTG")
                        upbit.sell_market_order("KRW-BTG", left * 0.99)

                    time.sleep(5*60)


        except :
            print("error!")
            time.sleep(3) # n 초 동안 작동 안함
        
