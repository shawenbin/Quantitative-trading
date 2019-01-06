import datetime,pandas
开始时间=datetime.datetime.now()
限长=150
预警=.01
峰态=[20,.3]#峰距，峰偏
序号=list(range(0,限长))
候选=pandas.DataFrame(columns=['股票','左序','左价','右序','右价','突破'])
股票=[股票 for 股票 in list(all_instruments(type='CS').order_book_id) if instruments(股票).days_from_listed()>40 and not is_suspended(股票).iat[-1,0]]
for 成员 in 股票:
    行情=get_price(成员, start_date='2015-12-09', end_date=datetime.date.today(), fields=['high','low','close','volume'])
    行情=行情[行情.volume>0].tail(限长)
    收盘=行情.iat[-1,2]
    实长=len(行情)
    行情['日序']=序号[0:实长]
    行情['峰']=False
    角标=1
    while 角标<实长-1:
        if 行情.iat[角标,0]>=行情.iat[角标-1,0] and 行情.iat[角标,0]>行情.iat[角标+1,0]:
            行情.iat[角标,5]=True
        角标+=1
    行情=行情.sort_values(by=['high','日序'],ascending=[False,True])
    采样=[0]
    角标=1
    参照=行情.iat[0,4]
    while 角标<len(行情):
        if 行情.iat[角标,4]>参照:
            采样.append(角标)
            参照=行情.iat[角标,4]
        角标+=1
    行情=行情.iloc[采样]
    游一=0
    新长=len(行情)
    while 游一<新长:
        左序=行情.iat[游一,4]
        if 行情.iat[游一,5] and 左序-1<实长-峰态[0]/(.5+峰态[1]):
            左价=行情.iat[游一,0]
            游二=游一+1
            while 游二<新长:#考虑峰态
                右序=行情.iat[游二,4]
                if 右序>左序:
                    右价=行情.iat[游二,0]
                    步进=(右价-左价)/(右序-左序)
                    游三=游二+1
                    while 游三<新长:
                        验序=行情.iat[游三,4]
                        突破=右价+步进*(实长-右序)
                        if 行情.iat[游三,0]>右价+步进*(验序-右序):
                            break
                        elif 验序==实长-1:
                            游二=实长
                            if 右序-左序>峰态[0] and 右序-左序>(实长-左序)*(.5-峰态[1]) and 实长-右序>(实长-左序)*(.5-峰态[1]) and 收盘*(1+预警)>突破:
                                候选=候选.append({'股票':成员,'左序':左序,'左价':左价,'右序':右序,'右价':右价,'突破':突破},ignore_index=True)
                            break
                        游三+=1
                游二+=1
        游一+=1
if len(候选)>0:
    候选=候选.sort_values(by=['股票','突破'])
    采样=[0]
    角标=1
    while 角标<len(候选):
        if 候选.iat[角标,0]!=候选.iat[角标-1,0]:
            采样.append(角标)
        角标+=1
    候选=候选.iloc[采样].sort_values(by=['突破']).tail(round(len(采样)*.6))
print('输出完成，耗时',datetime.datetime.now()-开始时间,'\n',候选)
