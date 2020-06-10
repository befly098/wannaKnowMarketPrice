from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from app.module import dbModule

#index 파일 들어갔을때 이름 설정 , url 어떻게 붙일 지,,,
main= Blueprint('main', __name__, url_prefix='/')


@main.route('/',methods = ['GET'])
@main.route('/main',methods=['GET'])
def index():
    return render_template('/main/index.html')

@main.route("/RealTimePrice",methods = ['GET'])
def RealTimePrice():
    db_class = dbModule.Database()
    #평균값. 
    avg_tmon = db_class.selectDataAsShop('Nintendo_TB','TMON')
    avg_naver = db_class.selectDataAsShop('Nintendo_TB','NAVER Shopping')
    avg_auction = db_class.selectDataAsShop('Nintendo_TB','Auction')
    return render_template('/main/RealTimePrice.html',resultTmon = avg_tmon,resultNaver = avg_naver,resultAuction = avg_auction)

@main.route("/PriceChange",methods = ['GET'])
def PriceChange():
   return render_template('main/PriceChange.html')
