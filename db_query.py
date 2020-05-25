import pymysql

#root 권한으로 접속
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='admin',
                     db='test')

def makeTable(TableName):
    with db.cursor() as cursor:
        # table 생성
        sql = """
            CREATE TABLE %s(
                shop VARCHAR(20),
                pname VARCHAR(80),
                price VARCHAR(20),
                pdate DATETIME
            );"""
        cursor.execute(sql%(TableName,))
        db.commit()

def insertData(filepath,TableName):
    data = (filepath,TableName)
    with db.cursor() as cursor:
        # table 생성
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
try:
    # table 생성 (한번만 실행)
    makeTable('Nintendo_TB')

    #txt file->table삽입 (한번만 실행)
    ##이때 파일 경로 -> my.ini 파일에서 secure-file-priv.
    ###상품이 더 추가될 경우 대비-> 인자로 테이블 명(제품 종류에 따라 다른 테이블)을 준다.
    insertData('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sample_data.txt','Nintendo_TB')

    #data 조회 -> 실시간 조회의 경우
    ##상품이 더 추가될 경우 대비-> 인자로 테이블 명(제품 종류에 따라 다른 테이블)을 준다.
    selectData('Nintendo_TB')

finally:
    db.close()