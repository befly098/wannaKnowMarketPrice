from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from app.module import dbModule
from datetime import datetime,timedelta,date

today = date.today()
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
    avg_naver = db_class.selectLatestDataAsShop('Nintendo_TB','NAVER Shopping')
    avg_auction = db_class.selectLatestDataAsShop('Nintendo_TB','Auction')
    return render_template('/main/RealTimePrice.html',resultTmon = avg_tmon,resultNaver = avg_naver,resultAuction = avg_auction)

@main.route("/PriceChange",methods = ['GET'])
def PriceChange():
    db_class = dbModule.Database()
    #평균값. 
    avg_tmon=[]
    avg_naver =[]
    avg_auction=[]
    for i in range(7):
        print(sevenWeek[i])
        avg_tmon.append(db_class.selectAvgDataAsShopPerDay('Nintendo_TB','TMON',sevenWeek[i]))
        avg_naver.append(db_class.selectAvgDataAsShopPerDay('Nintendo_TB','Naver Shopping',sevenWeek[i]))
        avg_auction.append(db_class.selectAvgDataAsShopPerDay('Nintendo_TB','Auction',sevenWeek[i]))
    return render_template('main/PriceChange.html',resultTmon = avg_tmon,resultNaver = avg_naver,resultAuction = avg_auction)
   
@main.route("/Market",methods = ['GET'])
def Market():
   return render_template('main/Market_frame.html')

@main.route("/Login",methods = ['GET'])
def Login():
   return render_template('main/Login.html')

