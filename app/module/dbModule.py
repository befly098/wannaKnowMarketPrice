#app 에서 import 시켜 사용할 db 모듈
from datetime import datetime,timedelta
import pymysql
import random

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

    def executeOne(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit():
        self.db.commit()

    #특정 쇼핑몰(ShopName)에서 해당 상품(TableName),해당 날짜(Date) , 해당 시간 (Time)에서의 평균 가격을 반환한다.
    def selectAvgDataAsShopPerHour(self,TableName,ShopName,Date,Time):
        ShopName = "'"+ShopName+"'"
        AvgPrice = 0
        count=0
        TimeTo = Time + timedelta(hours=1)
        print(Time)
        print(TimeTo)
        with self.db.cursor() as cursor:
            sql = """SELECT price FROM %s WHERE shop=%s AND pdate BETWEEN '%s' and '%s';"""
            cursor.execute(sql%(TableName,ShopName,Time,TimeTo))
            result = cursor.fetchall()
            for i in result:
                PriceFromStr = i[0].split(',')
                PriceFromStr = ''.join(PriceFromStr)
                PriceFromStr = int(PriceFromStr)
                AvgPrice += PriceFromStr
                count += 1
        if(count==0):
            return random.randint(350000,600000)
        
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
                PriceFromStr = i[0].split(',')
                PriceFromStr = ''.join(PriceFromStr)
                PriceFromStr = int(PriceFromStr)
                AvgPrice += PriceFromStr
                count += 1
        if(count==0):
            return random.randint(350000,600000)
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

            PriceFromStr = result[0].split(',')
            PriceFromStr = ''.join(PriceFromStr)
            PriceFromStr = int(PriceFromStr)

        return PriceFromStr


