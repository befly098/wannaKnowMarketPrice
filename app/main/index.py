from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app

#index 파일 들어갔을때 이름 설정 , url 어떻게 붙일 지,,,
main= Blueprint('main', __name__, url_prefix='/')


@main.route('/',methods = ['GET'])
@main.route('/main',methods=['GET'])
def index():
    return render_template('/main/index.html')

@main.route("/RealTimePrice",methods = ['GET'])
def RealTimePrice():
    return render_template('/main/RealTimePrice.html')

@main.route("/PriceChange",methods = ['GET'])
def PriceChange():
   return render_template('main/PriceChange.html')
