# buy2
import numpy as np
import pyupbit

temp = np.where(buy_count == 0)
temp2 = numpy.asarray(temp)
new = temp2[0,0]

if ( count >= n_count ) or ( delta < -tic * bigone ) :
    
    # 90% buy operation
    upbit.buy_market_order("KRW-BTG", balance * 0.9)
    buy_price[new]  = pyupbit.get_current_price("KRW-BTG")
    buy_vol[new]    = balance * 0.9 
    buy_count[new]  = 1 
    buy_num[new]    = 1 
    
    
    count = 0 
    