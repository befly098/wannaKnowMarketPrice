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
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    #쿼리 실행
    def execute(self,query,args={}):
        self.cursor.execute(query,args)

    #tuple 하나만
    def executeOne(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchone()
        return row

    #tuple 다
    ## 실시간: 오늘꺼 ->(row 막줄) 
    def executeAll(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit():
        self.db.commit()

    #특정 쇼핑몰(ShopName)에서 해당 상품(TableName),해당 날짜(Date) , 해당 시간 (Time)에서의 평균 가격을 반환한다.
    def selectAvgDataAsShopPerHour(self,TableName,ShopName,Date,TimeFrom,TimeTo):
        ShopName = "'"+ShopName+"'"
        AvgPrice = 0
        count=0
        with self.db.cursor() as cursor:
            sql = """SELECT price FROM %s WHERE shop=%s and pdate BETWEEN '%s %s' AND '%s %s';"""
            cursor.execute(sql%(TableName,ShopName,Date,TimeFrom,Date,TimeTo))
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

 #특정 쇼핑몰(ShopName)에서 해당 상품(TableName),해당 날짜(Date) 의 평균 가격을 반환한다.
    def selectAvgDataAsShopPerDay(self,TableName,ShopName,Date):
        ShopName = "'"+ShopName+"'"
        AvgPrice = 0
        count=0
        with self.db.cursor() as cursor:
            sql = """SELECT price FROM %s WHERE shop=%s and pdate BETWEEN '%s 00:00:00' AND '%s 23:59:59';"""
            cursor.execute(sql%(TableName,ShopName,Date,Date))
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
        if(count==0):
            return 600152
        else:
           AvgPrice = int(AvgPrice/count)
        return AvgPrice

    #특정 쇼핑몰(ShopName)에서 해당 상품(TableName)의 최신 가격을 반환한다.
    def selectLatestDataAsShop(self,TableName,ShopName):
        ShopName = "'"+ShopName+"'"
        AvgPrice = 0
        count=0
        with self.db.cursor() as cursor:
            sql = """SELECT price FROM %s WHERE shop=%s;"""
            cursor.execute(sql%(TableName,ShopName,))
            result = cursor.fetchone()
            
            #1.문자열의 반점(,) 제거
            ##1-1.반점으로 나눈다.
            PriceFromStr = result[0].split(',')
            PriceFromStr = ''.join(PriceFromStr)
            PriceFromStr = int(PriceFromStr)

        return PriceFromStr


