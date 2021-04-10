### 커피 주문 마이크로서비스

- 디버그 모드 실행 방법 수정

  - `rest1.py`에서 `app.config["DEBUG"] = True` 수정
  
  - ```python
    # app.config["DEBUG"] = True
    # $ flask app <- app.py
    # 실행 파일을 변경하려면, set FLASK_APP=new file.py
    # 디버그 모드 실행, set FLASK_DEBUG=True -> auto-refresh
    ```
  
  - `app.config["DEBUG"] = True` 구문을 주석처리
  
  - 실행 파일 변경 및 디버그 모드 실행 방법
  
    - ```
      $ set FLASK_APP=new file.py
      $ set FLASK_DEBUG=True
      $ flask run
      ```



- 회원 로그인 기능 포함한 Testcase 만드는 규칙

  - 코드를 테스트 하기 위한 Testcase 개수는 `features * n` 만큼 만든다.
  
- `feature` : 요구사항
  
- ```
  Testcase
    CASE-0001 아이디/암호를 입력할 수 있다.
    CASE-0002 아이디 또는 암호를 입력하지 않으면 경고 메시지 출력된다.
    CASE-0003 아이디/암호를 입력한 다음, 엔터키를 누르면 로그인 처리로 이동한다.
  ```
  
  - 정상/비정상 테스트

  - ```python
    Try:
        정상
    Except:
        비정상 종료
    ```

  - 정상 테스트와 비정상 테스트를 모두 실시해야한다. 비정상 테스트의 경우 에러 메시지가 출력되고 사용자가 우회할 수 있는 가이드가 제공되야함.

  - 코드가 수정되었으면 모든 테스트 케이스를 처음부터 다시 테스트 해야한다.

  - 유저 테스트(**UAT**) : 모든 코드가 통합된 상태에서 실제 환경과 같은 환경에서 실행

  - 프로젝트 막바지에 테스트 케이스를 만드는 것은 매우 힘든 일이다. 왜냐하면 막바지에는 해야할 일이 많기 때문에 시간적 여유가 부족하다. 그래서 미리미리 테스트 케이스를 만들어야한다.
  
  - 테스트 코드를 생성 후 실제 개발하기 직전에 실행한다.
  
  - 처음에는 무조건 실패하지만 하나하나 성공하면서 완성한다.
  
  - 테스트 케이스를 만들지 않으면 만든 코드를 증명할 수 있는 방법이 줄어들기 때문에 버그가 잡힐 확률이 높아진다. 



- postman 에서 데이터를 POST 방식으로 전송한 이후 DB에 저장되도록 설정하기

- >  kafka_microservice.md 파일에서 했던 내용 이어서 진행

  - MariaDB의 mydb 데이터베이스의 orders 테이블에 데이터가 저장된다.

  - order.py 수정
  
  - ```python
    # Order 클래스에 다음 초기화 함수 추가
    def __init__(self):
    	self.conn = mariadb.connect(**config)
      self.cursor = self.conn.cursor()
    ```
  
  - ```python
    # post 메소드의 DB insert 부분에 다음 문장 추가
    sql = '''INSERT INTO orders(user_id, order_id, coffee_name, coffee_price, coffee_qty, ordered_at)
          VALUES(?,?,?,?,?,?)
          '''
    	self.cursor.execute(sql, [user_id, json_data['order_id'],
                                           json_data['coffee_name'],
                                           json_data['coffee_price'],
                                           json_data['coffee_qty'],
                                           json_data['ordered_at']])
      self.conn.commit()
    ```

  - 코드 실행 후 postman 에서 POST 방식으로 데이터 전송

  - **URL** = `127.0.0.1:5000/order-ms/USER0001/orders`
  
  - ```json
    # 전송 데이타
    {
        "coffee_name": "jslee",
        "coffee_price": 2000,
        "coffee_qty": 6
  }
    ```
  
  - ```json
    # postman 에서 출력
    {
        "coffee_name": "jslee",
        "coffee_price": 2000,
        "coffee_qty": 6,
        "order_id": "1b20c13f-e313-448e-af1f-ac946e505844",
        "ordered_at": "2021-04-06 10:19:18.993826",
        "user_id": "USER0001"
  }
    ```

  - MariaDB의 orders 테이블에 데이터 저장된 것 확인 - MySQL Client 에서 실행
  
  - ```
  $ select * from orders;
    ```

  - 위 명령어를 입력하면 postman 에서 입력한 데이터가 저장되어있다.
  
  - `HeidiSQL` 을 이용하여 확인하는 방법도 있다.



- Postman 에서 같은 URL로 GET 요청을 보내서 orders 테이블에 저장된 데이터 읽기

  - **URL** : `127.0.0.1:5000/order-ms/USER0001/orders`

  - ```json
    # 전송받은 데이터
    [
        [
            2,
            "USER0001",
            "1b20c13f-e313-448e-af1f-ac946e505844",
            "jslee",
            2000,
            6,
            "2021-04-06 10:19:18.993826"
        ],
        [
            1,
            "USER0001",
            "0452b5e0-fc7d-4454-870b-9a6a359c609e",
            "jslee",
            1000,
            5,
            "2021-04-06 10:18:57.629268"
        ]
    ]
    ```

  - 모양이 조금 이상하여 데이터 확인이 어려우므로 보기 쉽게 바꾼다.

 

- get 메소드 수정

  - ```python
    # order_ms.py 의 get 메소드를 다음과 같이 수정
    def get(self, user_id):
        sql = '''select user_id, order_id, coffee_name, coffee_price, coffee_qty, ordered_at
                 from orders where user_id=? order by id desc'''
        self.cursor.execute(sql, [user_id])
        result_set = self.cursor.fetchall()
    
        row_headers = [x[0] for x in self.cursor.description]
    
        json_data = []
        for result in result_set:
        	json_data.append(dict(zip(row_headers,result)))
            
        return jsonify(json_data)
    ```

  - 코드 저장 후 서버 작동하여 Postman 에서 GET 방식으로 확인

  - ```json
    # GET 방식으로 send 결과
    [
        {
            "coffee_name": "jslee",
            "coffee_price": 2000,
            "coffee_qty": 6,
            "order_id": "1b20c13f-e313-448e-af1f-ac946e505844",
            "ordered_at": "2021-04-06 10:19:18.993826",
            "user_id": "USER0001"
        },
        {
            "coffee_name": "jslee",
            "coffee_price": 1000,
            "coffee_qty": 5,
            "order_id": "0452b5e0-fc7d-4454-870b-9a6a359c609e",
            "ordered_at": "2021-04-06 10:18:57.629268",
            "user_id": "USER0001"
        }
    ]
    ```

  - 데이터 출력 결과가 보기 좋게 나왔다. 이전에 orders 테이블에 저장했던 데이터가 잘 저장 되어있는 것을 알 수 있다.





- 데이타베이스 생성 후 kafka topic에 데이터 삽입하기

  - table 추가 쿼리문

  - ```

    create table delivery_status (
    	id int auto_increment primary key,
    	order_json text,
    	created_at datetime default now()
    );
    ```

  - `order_ms.py` 수정

  - ```python
    # post 메소드 수정 - self.conn.commit() 아래에 다음 문장 추가
    # Kafka message send
    # KafkaProducer() -> 생성자에 추가
    # producer 인스턴스의 send() 메소드로 json 데이터 전송
    self.producer.send('new_orders', value=json.dumps(json_data).encode())
    self.producer.flush()
    ```

  - ```
    $ pip install kafka-python
    ```

  - kafka 명령어 실행하여 topic 생성

  - ```
    $ python order_ms.py
    ```

  - kafka의 topic에 데이터를 입력




- kafka의 데이터를 read 하기

  - `kafka_consumer.py` 작성

  - ```python
    from kafka import KafkaConsumer
    import time, json
    
    consumer = KafkaConsumer('new_orders',
                             bootstrap_servers=["localhost:9092"],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             auto_commit_interval_ms=1000,
                             consumer_timeout_ms=1000)
    
    # 테스트 코드
    start = time.time()
    for message in consumer:
        topic = message.topic
        partition = message.partition
        offset = message.offset
        value = message.value
        
        print("Topic:{}, Partition:{}, Offset:{}, Value:{}".format(topic,
        partition, offset, value))
    
    print("Elapsed: ", (time.time() - start))
    ```

  - 코드 실행

  - ```
    $ python kafka_consumer.py
    ```

  - kafka를 통해 데이터가 전송된 것을 읽어서 출력이 잘 되는지 확인(`consumer`에 대한 확인)



- 최신 주문 데이타 불러오기

  - `kafka_consumer.py` 수정

  - ```python
    from kafka import KafkaConsumer
    import time, json
    import threading
    from datetime import datetime
    
    consumer = KafkaConsumer('new_orders',
                             bootstrap_servers=["localhost:9092"],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             auto_commit_interval_ms=1000,
                             consumer_timeout_ms=1000)
    
    def fetch_latest_orders(next_call_in):
        # 5초에 한번씩 가져오기
        next_call_in += 5
    
        # 현재 시간 출력
        print(str(datetime.today()))
    
        threading.Timer(next_call_in - time.time(), fetch_latest_orders, [next_call_in]).start()
    
    next_call_in = time.time()
    fetch_latest_orders(next_call_in)
    ```

  - 코드를 실행하면 5초에 한번씩 데이터를 불러온다.



- postman에서 `POST`로 메시지 보내고 확인하는 코드

  - `kafka_consumer.py` 수정

  - ```python
    from kafka import KafkaConsumer
    import time, json
    import threading
    from datetime import datetime
    
    consumer = KafkaConsumer('new_orders',
                             bootstrap_servers=["localhost:9092"],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             auto_commit_interval_ms=1000,
                             consumer_timeout_ms=1000)
    
    def fetch_latest_orders(next_call_in):
        # 5초에 한번씩 가져오기
        next_call_in += 5
    
        # consumer의 데이터 읽어오는 함수 poll
        batch = consumer.poll(timeout_ms=100)
        print(len(batch))
        # list(batch.values())
    
        threading.Timer(next_call_in - time.time(), fetch_latest_orders, [next_call_in]).start()
    
    next_call_in = time.time()
    fetch_latest_orders(next_call_in)
    ```

  - 5초에 한번씩 batch의 길이를 출력함

  - 아무것도 안하면 0이 찍힘

  - postman에서 데이터를 보내면 숫자가 1이 찍힘

  

  - 길이가 아닌 메시지를 출력하는 코드

  - ```python
    # kafka_consumer.py 수정
      from kafka import KafkaConsumer
    import time, json
    import threading
    from datetime import datetime
    
    consumer = KafkaConsumer('new_orders',
                               bootstrap_servers=["localhost:9092"],
                               auto_offset_reset='earliest',
                               enable_auto_commit=True,
                               auto_commit_interval_ms=1000,
                               consumer_timeout_ms=1000)
    
    def fetch_latest_orders(next_call_in):
    	# 5초에 한번씩 가져오기
        next_call_in += 5
        # consumer의 데이터 읽어오는 함수 poll
      	batch = consumer.poll(timeout_ms=100)
        if len(batch) > 0:
            for message in list(batch.values())[0]:
                print(message)
      
    	threading.Timer(next_call_in - time.time(), fetch_latest_orders, [next_call_in]).start()
    
    next_call_in = time.time()
    fetch_latest_orders(next_call_in)
    ```
  
  - 코드 실행하면 아무것도 실행을 안함
  
  - postman 에서 데이터를 POST 방식으로 send 하면 바로 데이터가 뜬다.
  
  - ```
    # 데이터 수신 결과
      ConsumerRecord(topic='new_orders', partition=0, offset=0, timestamp=1617684733599, timestamp_type=0, key=None, value=b'{"coffee_name": "jason", "coffee_price": 4000, "coffee_qty": 8, "user_id": "USER0001", "order_id": "6c1de1e2-8921-4447-a3b9-bf7a062dd598", "ordered_at": "2021-04-06 13:52:13.596638"}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=182, serialized_header_size=-1)
      ```
  
  - 메시지가 전송되는 시간을 출력하는 코드
  
  - ````python
    # kafka_consumer.py 의 batch 에 대한 if 구문을 다음과 같이 수정
    if len(batch) > 0:
      	for message in list(batch.values())[0]:
          	value = message.value.decode()
            order_dict = json.loads(value) # json -> dict
            print(order_dict["ordered_at"])
    ````
  
  - 코드 실행 
  
  - postman에서 데이터를 전송한 시간이 출력된다.
  
  - 실행 중 postman에서 POST 방식으로 메시지를 다시 전송하면 그 시간이 바로 출력된다.
  
  - ```
    # 실행 결과
    2021-04-06 13:52:13.596638
    2021-04-06 13:55:28.127564
    ```
  
  


- kafka로 데이터베이스의 delivery_status 테이블에 데이터 넣기

  - database에 column 추가

  - ```mysql
    alter table delivery_status
    	add column delivery_id varchar(50) after id;
    alter table delivery_status
    	add column status varchar(50) after order_json;
    ```

  - `kafka_consumer.py` 수정

  - ```python
    from kafka import KafkaConsumer
    import time, json, uuid, mariadb
    import threading
    from datetime import datetime
    
    consumer = KafkaConsumer('new_orders',
                             bootstrap_servers=["localhost:9092"],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             auto_commit_interval_ms=1000,
                             consumer_timeout_ms=1000)
    
    config = {
        'host': '',
        'port': 3306,
        'user': 'root',
        'password': 'mysql',
        'database': 'mydb'
    }
    conn = mariadb.connect(**config)
    cursor = conn.cursor()
    sql = '''INSERT INTO delivery_status(delivery_id, order_json, status)
            VALUES(?,?,?)'''
    
    def fetch_latest_orders(next_call_in):
        # 5초에 한번씩 가져오기
        next_call_in += 5
    
        # consumer의 데이터 읽어오는 함수 poll
        batch = consumer.poll(timeout_ms=100)
        # print(len(batch))
        # list(batch.values())
        if len(batch) > 0:
            for message in list(batch.values())[0]:
                value = message.value.decode()
                # order_dict = json.loads(value) # json -> dict
                # print(order_dict["ordered_at"])
                
                delivery_id = str(uuid.uuid4())
                status = 'CONFIRMED'
                # DB insert
                cursor.execute(sql, [delivery_id, value, status])
                conn.commit()
    
        threading.Timer(next_call_in - time.time(), fetch_latest_orders, [next_call_in]).start()
    
    next_call_in = time.time()
    fetch_latest_orders(next_call_in)
    ```

  - 코드 실행하고 서버 가동시킨다.

  - ```
    $ python kafka_consumer.py
    $ python order_ms.py
    ```

  - postman 에서 `POST` 모드로 데이터 send 하면 DB의 delivery_status 테이블에 데이터가 추가된다.

  - 이것은 order_ms에서 json 데이터를 kafka로 send 한 후 이 데이터를 kafka_consumer가 전송 받아 delivery_status라는 데이터 테이블에 저장하는 과정이다.



- `order.py`의 Orderdetail 클래스는 직접 만들어보시오



- Delivery_ms 만들기

  > delivery_status 테이블에 저장된 데이터를 불러오고 상태를 업데이트하는 코드

  - 요구사항

  - ```
    GET /delivery-ms/deliveries
    PUT /delivery-ms/deliveries/[DELIVERY_ID]/status 에서
    status: CONFIRMED 를 COMPLETED 로 바꾸기
    ```

  - `delivery_ms.py` 작성

  - ```python
    # 내가 만든 코드
    from flask import Flask, jsonify, request
    from datetime import datetime
    import uuid, json, mariadb, flask_restful
    from flask_restful import reqparse
    from kafka import KafkaProducer
    
    app = Flask(__name__)
    # app.config["DEBUG"] = True
    api = flask_restful.Api(app)
    
    config = {
        'host': '',
        'port': 3306,
        'user': 'root',
        'password': 'mysql',
        'database': 'mydb'
    }
    
    @app.route('/delivery-ms')
    def index():
        return "Welcome to DELIVERY Microservice!"
    
    class DeliveryGet(flask_restful.Resource):
        def __init__(self):
            self.conn = mariadb.connect(**config)
            self.cursor = self.conn.cursor()
            self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        
        def get(self):
            sql = '''select delivery_id, order_json, status, created_at
                     from delivery_status order by id desc'''
            self.cursor.execute(sql)
            result_set = self.cursor.fetchall()
    
            row_headers = [x[0] for x in self.cursor.description]
    
            json_data = []
            for result in result_set:
                json_data.append(dict(zip(row_headers,result)))
            
            return jsonify(json_data)
    
    
    class DeliveryPut(flask_restful.Resource):
        def __init__(self):
            self.conn = mariadb.connect(**config)
            self.cursor = self.conn.cursor()
            self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        
        def put(self, delivery_id):
            json_data = request.get_json()
    
            sql = '''UPDATE delivery_status SET status = 'COMPLETED' WHERE delivery_id=?'''
            self.cursor.execute(sql, [delivery_id])
            self.conn.commit()
    
            response = jsonify(json_data)
            response.status_code = 200
            return response
    
    # GET    http://127.0.0.1:5000/delivery-ms/orders
    # PUT    http://127.0.0.1:5000/delivery-ms/deliveries/delivery_id/status
    api.add_resource(DeliveryGet, '/delivery-ms/orders')
    api.add_resource(DeliveryPut, '/delivery-ms/deliveries/<string:delivery_id>/status')
    
    
    if __name__ == '__main__':
        app.run()
    ```

  - ```python
    # 강사님 코드
    from flask import Flask, jsonify, request
    from datetime import datetime
    import uuid, json, mariadb, flask_restful
    from flask_restful import reqparse
    from kafka import KafkaProducer
    
    app = Flask(__name__)
    # app.config["DEBUG"] = True
    api = flask_restful.Api(app)
    
    config = {
        'host': '',
        'port': 3306,
        'user': 'root',
        'password': 'mysql',
        'database': 'mydb'
    }
    
    @app.route('/delivery-ms')
    def index():
        return "Welcome to DELIVERY Microservice!"
    
    class Delivery(flask_restful.Resource):
        def __init__(self):
            self.conn = mariadb.connect(**config)
            self.cursor = self.conn.cursor()
                
        def get(self):
            sql = '''select delivery_id, order_json, status, created_at
                     from delivery_status order by id desc'''
            self.cursor.execute(sql)
            result_set = self.cursor.fetchall()
    
            row_headers = [x[0] for x in self.cursor.description]
    
            json_data = []
            for result in result_set:
                json_data.append(dict(zip(row_headers,result)))
            
            return jsonify(json_data)
    
    
    class DeliveryStatus(flask_restful.Resource):
        def __init__(self):
            self.conn = mariadb.connect(**config)
            self.cursor = self.conn.cursor()
        
        # /delivery-ms/deliveries/1234
        # { "status": "COMPLETED" } 로 바꾸기
        def put(self, delivery_id):
            json_data = request.get_json()
            status = json_data['status']
    
            sql = "UPDATE delivery_status SET status=? WHERE delivery_id=?"
            self.cursor.execute(sql, [status, delivery_id])
            self.conn.commit()
    
            # 날짜 데이터는 추가 안해도 됨
            json_data['updated_at'] = str(datetime.today())
            response = jsonify(json_data)
            response.status_code = 201
            return response
    
    # GET    http://127.0.0.1:5000/delivery-ms/orders
    # PUT    http://127.0.0.1:5000/delivery-ms/deliveries/delivery_id/status
    api.add_resource(Delivery, '/delivery-ms/deliveries')
    api.add_resource(DeliveryStatus, '/delivery-ms/deliveries/<string:delivery_id>')
    
    
    if __name__ == '__main__':
        app.run(port = 6000)
    ```

  - 새로 terminal 열어서 환경 변수 설정 후 실행

    - ```
      $ set FLASK_APP=delivery_ms.py
      $ flask run --port 6000
      ```

  - python 파일을 실행하는 것도 가능

    - ```
      $ python delivery_ms.py
      ```



- Postman 으로 데이터 확인하기

  - GET

    - URL : `http://127.0.0.1:5000/delivery-ms/deliveries`

    - ```json
      [
          {
              "created_at": "Tue, 06 Apr 2021 15:46:00 GMT",
              "delivery_id": "d826572a-57c6-4663-905f-c5ea01163549",
              "order_json": "{\"coffee_name\": \"ahahhahaha\", \"coffee_price\": 7000, \"coffee_qty\": 11, \"user_id\": \"USER0001\", \"order_id\": \"d5f5a3cf-e1c6-4c76-bcbc-ed29425384d1\", \"ordered_at\": \"2021-04-06 15:45:57.117123\"}",
              "status": "CONFIRMED"
          },
          {
              "created_at": "Tue, 06 Apr 2021 15:45:45 GMT",
              "delivery_id": "b059170f-d63e-4ca6-9af3-f9b7a12d5910",
              "order_json": "{\"coffee_name\": \"mauro\", \"coffee_price\": 6000, \"coffee_qty\": 10, \"user_id\": \"USER0001\", \"order_id\": \"a3e6dbc1-e85b-44d3-b8dd-bec2ebbe7af1\", \"ordered_at\": \"2021-04-06 14:57:10.155838\"}",
              "status": "CONFIRMED"
          }
      ]
      ```

  - PUT

    - GET 에서 아무 delivery_id를 복사하여 URL에 입력

    - URL : `http://127.0.0.1:5000/delivery-ms/deliveries/0fee98c8-c075-4652-9fb8-b508bd184342`

    - 다음과 같이 json 데이터 입력

    - ```json
      {
          "status": "COMPLETED"
      }
      ```

    - 다음과 같은 output 출력됨

    - ```json
      {
          "status": "COMPLETED",
          "updated_at": "날짜"
      }
      ```

    - `COMPLETED` 말고 `CANCELED` 등 다른 값도 입력 가능
    
    - 내가 만든 코드는 데이터는 제대로 PUT이 되는데 postman 에서는 왜 null이 뜨는지 잘 모르겠다.

