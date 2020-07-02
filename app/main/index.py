from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from app.module import dbModule
from datetime import datetime,timedelta,date
from dateutil.parser import parse


today = date.today()
now = datetime.now().hour

sevenWeek = []
for i in range(7):
    day= today-timedelta(7-i)
    sevenWeek.append(day)       

#index 파일 들어갔을때 이름 설정 , url 어떻게 붙일 지,,,
main= Blueprint('main', __name__, url_prefix='/')


@main.route('/',methods = ['GET'])
@main.route('/main',methods=['GET'])
def index():
    return render_template('/main/index.html')

@main.route("/RealTimePrice",methods = ['GET'])
def RealTimePrice():
    db_class = dbModule.Database()
    
    #최신값. 
    avg_tmon = db_class.selectLatestDataAsShop('Nintendo_TB','TMON')
    avg_naver = db_class.selectLatestDataAsShop('Nintendo_TB','SSG')
    avg_auction = db_class.selectLatestDataAsShop('Nintendo_TB','Auction')
    avg_interpark= db_class.selectLatestDataAsShop('Nintendo_TB','interpark')
    
    ##하루동안 증감
    midnight =parse('00:00:00')
    print(type(midnight))
    avg_tmon_day =[]
    avg_naver_day = []
    avg_interpark_day = []
    avg_auction_day = []
    for i in range (int(now)+8):
        print(today)
        print(midnight)
        avg_tmon_day.append(db_class.selectAvgDataAsShopPerHour('Nintendo_TB','Tmon',today,midnight))
        avg_naver_day.append(db_class.selectAvgDataAsShopPerHour('Nintendo_TB','SSG',today,midnight))
        avg_auction_day.append(db_class.selectAvgDataAsShopPerHour('Nintendo_TB','Auction',today,midnight))
        avg_interpark_day.append(db_class.selectAvgDataAsShopPerHour('Nintendo_TB','interpark',today,midnight))
        midnight = midnight+ timedelta(hours=1)
        print(avg_tmon_day)
    return render_template('/main/RealTimePrice.html',resultTmon = avg_tmon,resultNaver = avg_naver,resultAuction = avg_auction,resultInterpark = avg_interpark,resultTmon_day = avg_tmon_day,resultNaver_day = avg_naver_day,resultAuction_day = avg_auction_day,resultInterpark_day = avg_interpark_day)

@main.route("/PriceChange",methods = ['GET'])
def PriceChange():
    db_class = dbModule.Database()
    #평균값. 
    avg_tmon=[]
    avg_naver =[]
    avg_auction=[]
    avg_interpark = []
    for i in range(7):
        print(sevenWeek[i])
        avg_tmon.append(db_class.selectAvgDataAsShopPerDay('Nintendo_TB','TMON',sevenWeek[i]))
        avg_naver.append(db_class.selectAvgDataAsShopPerDay('Nintendo_TB','SSG',sevenWeek[i]))
        avg_auction.append(db_class.selectAvgDataAsShopPerDay('Nintendo_TB','Auction',sevenWeek[i]))
        avg_interpark.append(db_class.selectAvgDataAsShopPerDay('Nintendo_TB','Interpark',sevenWeek[i]))
    return render_template('main/PriceChange.html',resultTmon = avg_tmon,resultNaver = avg_naver,resultAuction = avg_auction,resultInterpark = avg_interpark)
   


