from flask import Flask

app= Flask(__name__)

#index.py의 내용
#index 파일 들어갔을때 이름 설정 , url 어떻게 붙일 지,,,
#main= Blueprint('main', __name__, url_prefix='/')

#@main.route('/main',methods=['GET'])
#def index():
#    return render_template('/main/index.html')
from app.main.index import main as main
 
app.register_blueprint(main)


