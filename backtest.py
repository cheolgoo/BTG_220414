import pyupbit
import numpy as np





#for list in coin_list:

#coin_data = pyupbit.get_ohlcv(ticker = list)


# 파라미터들




# 과거 정보 획득

coin_list = ["KRW-BTC", "KRW-ETH"]


coin_data = pyupbit.get_ohlcv(ticker="KRW-ETH", interval='minute5', count=15000, to=20210605, period=0.1 )


open = coin_data['open']
close = coin_data['close']

delta = close - open

num = 0
count = 0
# 4차 매수까지 있다.
buy_count = 0
fee = 0.05 / 100 
buyfull_count = 0
mymoney = 1

# 추가해야될 것. 큰 폭으로 (3%나 그정도 ) 떨어지면 사는양을 늘리기 0.5 (단일 낙폭이 아니라 누적 낙폭이다.)

for i in range(0, len(open)) :

    tic = open[i] * 0.08 / 100

    # 사기

    if buy_count == 0 :

        if delta[i] < -tic :
            count = count + 1
        elif delta[i] > tic :
            count = 0
    

        if count >= 3 and mymoney > 0:

            buy1_price = open[i+1]
            count = 0
            buy_count = 1
            
            mymoney = mymoney*(3/4) - mymoney*(1/4)*fee
            buy1_vol = mymoney*(1/4)


    elif buy_count == 1 :

        #팔기
        if close[i] > buy1_price*1.02 :

            mymoney = mymoney + buy1_vol * (close[i]/buy1_price) * (1 - fee)
            buy_count = 0

        else :

            if delta[i] < -tic :
                count = count + 1
            elif delta[i] > tic :
                count = 0
            
            if count >= 3 and mymoney > 0:

                buy2_price = open[i+1]
                count = 0
                buy_count = 2
                
                mymoney = mymoney*(2/3) - mymoney*(1/3)*fee
                buy2_vol = mymoney*(1/3)




    elif buy_count == 2 :

        #팔기
        if close[i] > ( (buy1_price*0.25 + buy2_price*0.25)/(0.25+0.25) )*1.02 :

            mymoney = mymoney + buy1_vol * (close[i]/buy1_price) * (1 - fee) + buy2_vol * (close[i]/buy2_price) * (1 - fee)
            buy_count = 0

        else :

            if delta[i] < -tic :
                count = count + 1
            elif delta[i] > tic :
                count = 0
            
            if count >= 3 and mymoney > 0:

                buy3_price = open[i+1]
                count = 0
                buy_count = 3
                
                mymoney = mymoney*(1/2) - mymoney*(1/2)*fee
                buy3_vol = mymoney*(1/2)
            



    elif buy_count == 3 :

        #팔기
        if close[i] > ( (buy1_price*0.25 + buy2_price*0.25 + buy3_price*0.25)/(0.25+0.25+0.25) )*1.02 :

            mymoney = mymoney + buy1_vol * (close[i]/buy1_price) * (1 - fee) + buy2_vol * (close[i]/buy2_price) * (1 - fee) + buy3_vol * (close[i]/buy3_price) * (1 - fee)
            buy_count = 0

        else :
                
            if delta[i] < -tic :
                count = count + 1
            elif delta[i] > tic :
                count = 0
            
            if count >= 3 and mymoney > 0:

                buy4_price = open[i+1]
                count = 0
                buy_count = 4
                
                mymoney = 0
                buy4_vol = mymoney*(1 - fee)
        



    elif buy_count == 4 :

        #팔기
        if close[i] > ( (buy1_price*0.25 + buy2_price*0.25 + buy3_price*0.25 + buy4_price*0.25)/(0.25+0.25+0.25+0.25) )*1.02 :

            mymoney = mymoney + buy1_vol * (close[i]/buy1_price) * (1 - fee) + buy2_vol * (close[i]/buy2_price) * (1 - fee) + buy3_vol * (close[i]/buy3_price) * (1 - fee) + buy4_vol * (close[i]/buy4_price) * (1 - fee)
            buy_count = 0

        elif buyfull_count == 48 :# 4시간 
            
            mymoney = mymoney + buy1_vol * (close[i]/buy1_price) * (1 - fee) + buy2_vol * (close[i]/buy2_price) * (1 - fee) + buy3_vol * (close[i]/buy3_price) * (1 - fee) + buy4_vol * (close[i]/buy4_price) * (1 - fee)
            buyfull_count = 0
            buy_count = 0

        buyfull_count = buyfull_count + 1    



    print(mymoney)
    



'''

# 5분봉이 특정값보다 크면 2틱으로 치는거 어떰?




# 화폐별 tickers
tickers             = pyupbit.get_tickers(fiat="KRW")
tickers_length      = len(tickers)



ee = 0.0005 


# invest strategy
# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.1

# target(매수가), range 칼럼을 한칸씩 밑으로 내림 (.shift(1))
df['target'] = df['open'] + df['range'].shift(1)


# ror(그날 수익률), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] -fee,
                     1)


'''
'''
# n분봉, m틱

n  = 
m  = 


# 평일 주말 구분하는 게 의미가 있을까? (보통 주말에는 거래량이 적은 것 같다. 주말엔 좀 안전하게 가자?)



큰장대 음봉이 나왔을 때는, 틱수를 줄여서 2틱 구매하는 방법도?



산 후 몇시간 지나면 무조건 파는 전략


몇 % 이득 보면 무조건 익절하는 전략 (매 분마다 캐치해서 파는 전략 가져가야 할 듯)



분할매수의 원칙을 지킨다. 리스크 관리...
평소거래량보다 많은 거래량을 동반하며 하락한다면, 그 이후에 급 상승할 확률이 좀 있다.



최적화 파라미터, n분봉 / m틱 / 거래량 / 하강 - 상승 지수 / 큰 막대인지 작은 막대인지 분별하는 알고리즘 (fuzzy)



# CHLCV (open, high, low, close, volume) 당일 시가, 고가, 저가, 종가, 거래량
df = pyupbit.get_ohlcv("KRW-BTC",  interval="minute120", count = 200)

fee = 0.0005 


# invest strategy
# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.1

# target(매수가), range 칼럼을 한칸씩 밑으로 내림 (.shift(1))
df['target'] = df['open'] + df['range'].shift(1)


# ror(그날 수익률), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] -fee,
                     1)

#누적 곱 계산 (cumprod) -> 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Dorn 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())

# 
df.to_excel("data.xlsx")
'''