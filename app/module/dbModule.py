#app 에서 import 시켜 사용할 db 모듈

import pymysql

class Database():
    def __init__(self):
        #root 권한으로 접속
        self.db = pymysql.connect(host='localhost',
                     user='root',
                     password='admin',
                     db='test'
                     )

    #이건 이미 마이스큐엘에 있으니까 실행할 필요 없을듯?
    #def makeTable(TableName):
        #with self.db.cursor() as cursor:
            # table 생성
            #sql = """
                #CREATE TABLE %s(
                    #shop VARCHAR(20),
                    #pname VARCHAR(80),
                    #price VARCHAR(20),
                    #pdate DATETIME
                #);"""
            #cursor.execute(sql%(TableName,))
            #self.db.commit()

def insertData(filepath,TableName):
    data = (filepath,TableName)
    with db.cursor() as cursor:
        # row 삽입
        ##중복되면 안넣는 코드 추가,,,,,,
        sql = """LOAD DATA INFILE '%s' INTO TABLE %s;"""% (filepath,TableName)
        cursor.execute(sql)
        db.commit()

def selectData(TableName):
    with db.cursor() as cursor:
        # table 조회
        sql = """SELECT * FROM %s;"""
        cursor.execute(sql%(TableName,))
        #실행 결과 가져오기
        ##db.commit() 실행시키지 않는 이유 - 내부 데이터에 영향 X, 조회만 했기 때문
        result = cursor.fetchall()
        for i in result:
            print(i)

#특정 쇼핑몰(ShopName)에서 해당 상품(TableName)의 평균 가격을 반환한다.
def selectDataAsShop(TableName,ShopName):
    ShopName = "'"+ShopName+"'"
    AvgPrice = 0
    count=0
    with db.cursor() as cursor:
        # table 조회-해당 쇼핑몰의 data만 조회
        sql = """SELECT price FROM %s WHERE shop=%s;"""
        cursor.execute(sql%(TableName,ShopName,))
        result = cursor.fetchall()

        for i in result:
            #1.문자열의 반점(,) 제거
            ##1-1.반점으로 나눈다.
            PriceFromStr = i[0].split(',')
            ##1-2.다시 join 한다.
            PriceFromStr = ''.join(PriceFromStr)
            #2.문자열->정수로 변환
            PriceFromStr = int(PriceFromStr)
            #3.합산하여 평균 구하기
            AvgPrice += PriceFromStr
            count += 1

    AvgPrice = int(AvgPrice/count)
    return AvgPrice


try:
    # table 생성 (한번만 실행)
#    makeTable('Nintendo_TB')

    #txt file->table삽입 (한번만 실행)
    ##이때 파일 경로 -> my.ini 파일에서 secure-file-priv.
    ###상품이 더 추가될 경우 대비-> 인자로 테이블 명(제품 종류에 따라 다른 테이블)을 준다.
#    insertData('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sample_data.txt','Nintendo_TB')

    #data 조회 -> 실시간 조회의 경우
    ##상품이 더 추가될 경우 대비-> 인자로 테이블 명(제품 종류에 따라 다른 테이블)을 준다.
#    selectData('Nintendo_TB')

    ###각 쇼핑몰마다 조회할 수 있도록
    Nintendo_Naver = selectDataAsShop('Nintendo_TB','NAVER Shopping')
    Nintendo_Tmon = selectDataAsShop('Nintendo_TB','TMON')
    Nintendo_Auction = selectDataAsShop('Nintendo_TB','Auction')

except Exception as e:
    print(e)
finally:
    db.close()
