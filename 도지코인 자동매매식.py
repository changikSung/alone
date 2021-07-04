import pyupbit
import time
import datetime

def cal_target(ticker): 
    df = pyupbit.get_ohlcv(ticker, "day")
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high']-yesterday['low']
    target = today['open'] + yesterday_range * 0.3
    return target

f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()
upbit = pyupbit.Upbit(access,secret)

target = cal_target("KRW-DOGE")
print(target)
op_mode = False
hold = False

while True :
    now = datetime.datetime.now()
    if now.hour ==8 and now.minute ==57 and 30<= now.second<=40:
        if op_mode is True and hold is True:
            doge_balance = upbit.get_balance("KRW-DOGE")
            upbit.sell_market_order("KRW-DOGE",doge_balance)
            hold is False

            op_mode = False
            time.sleep(30)



    if now.hour == 9 and now.minute == 0 and 20<= now.second <= 30:
        target = cal_target("KRW-DOGE")
        op_mode = True


    price = pyupbit.get_current_price("KRW-DOGE")

    if op_mode is True and price is not None and hold is False and price >= target:
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order("KRW-DOGE",krw_balance*0.1)
        hold = True


    print(f"현재시간: {now} 목표가: {target} 현재가: {price} 보유상태: {hold} 동작상태{op_mode}")
    
    time.sleep(1)
