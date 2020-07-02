# Eolmani?!(얼마니?!) 닷컴
동일한 상품(닌텐도 스위치)에 대해 쇼핑몰 별로 쉬운 가격 비교가 가능하며, 해당 정보의 신뢰도가 높은 가격비교 웹 사이트.

* 시스템 구조 <br/>
    <img src="https://user-images.githubusercontent.com/44567793/86321498-11dac680-bc74-11ea-92b6-139a9adf797a.png" width="830" height="470">



* 사용 기술 상세 설명<br/>
  1. 백엔드<br/>
      * 웹 크롤링<br/>
      <img src="https://user-images.githubusercontent.com/44567793/86322412-e5c04500-bc75-11ea-8b54-42e25b891ca4.JPG" width="830" height="470"><br/>
        * Python2.7 Selenium ackage 사용
        * 인터파크, 티몬, 신세계, 옥션 쇼핑몰 크롤링
        * 관련 파일:/wannaKnowMarketPrice/crawl.py<br/>
     
     * 데이터 처리<br/>
       <img src="https://user-images.githubusercontent.com/44567793/86322416-e8bb3580-bc75-11ea-9ff6-eb7921fe96d0.JPG" width="830" height="470">
        * Python2.7, Bi-gram 기법 사용
        * Bi-gram 기법은 제품의 관련도를 측정함
        * 가격이 평균보다 낮은 제품의 데이터 삭제
        * 관련 파일: /wannaKnowMarketPrice/run.py, 
                  /wannaKnowMarketPrice/app/__init__.py, 
                  /wannaKnowMarketPrice/app/main/index.py
                
      * MySQL DB 구축 
        * MySQL DB 사용
        * 쇼핑몰 이름, 제품 이름, 제품 가격, 크롤링 시간 업데이트
        * /wannaKnowMarketPrice/crawl.py
 
  2. 프론트 엔드<br/>
  
      * Flask 웹 서버 구축: 
        * Python3.6 Flask package 사용
        * aws 서버와 연동한 웹 서버 구축
        * 관련 파일: /wannaKnowMarketPrice/run.py, 
                  /wannaKnowMarketPrice/app/__init__.py, 
                  /wannaKnowMarketPrice/app/main/index.py
             
      * 웹 서버, MySQL DB 연동<br/>
        <img src="https://user-images.githubusercontent.com/44567793/86322866-b2ca8100-bc76-11ea-9817-f17d2049cdea.JPG" width="830" height="470">
	      * Python3 MySQL 관련 package 사용
	      * MySQL DB와 웹서버 연결
	      * MySQL 데이터 웹페이지 적용
        * 관련 파일: /wannaKnowMarketPrice/app/module/dbModule.py
	
     * 웹 UI 제작: 
        * BootStrap을 사용한 웹 페이지 제작
        * 일간 시세 그래프, 주간 시세 그래프, 메인 페이지 포함 
        * 관련 폴더: /wannaKnowMarketPrice/app/templates/main/
  <br/>
  
* 프로젝트 사용 방법 <br/>
     * 웹페이지 접속 방법<br/>
        http://3.135.191.2:8700/ 접속<br/>
     * 웹 서버 실행 방법<br/>
        1)3.135.191.2에 server_key.pem을 사용해 접속<br/>
        2) ```python3 run.py```<br/>
* 실행 화면
  * 메인 페이지<br/>
    ![메인](https://user-images.githubusercontent.com/44567793/86323731-51a3ad00-bc78-11ea-99c2-3a07e015fce3.png)
  
   * 주간 시세 변동 - 1<br/>
    ![주간1](https://user-images.githubusercontent.com/44567793/86323725-4fd9e980-bc78-11ea-998c-ac8dd2e1235f.png)
    
    * 주간 시세 변동 - 2<br/>
    ![주간2](https://user-images.githubusercontent.com/44567793/86323728-510b1680-bc78-11ea-93e2-1efd598cadda.png)
  
    * 일간 시세 변동<br/>
    ![일간](https://user-images.githubusercontent.com/44567793/86323733-51a3ad00-bc78-11ea-8fb5-14b2eba3c4cc.png)
                 
