### ORDER_MS, DELIVERY_MS, KAFKA, DB 를 Dockerfile 로 만들기 과제

1. order_ms.py를 Dockerfile로 만들기
   - Order Microservice
2. delivery_ms.py
   - Delivery Microservice
3. kafka_consumer.py
   - Kafka Topic에서 메시지 가져와서 DB에 저장
4. DB는 Dockerfile로 생성
   - Local DB or AWS RDS 사용
5. Zookeeper + Kafka 이미지는 제공됨





### 강사님의 강의

##### delivery_ms docker image 만들기

1. mysql DB를 실행하는 컨테이너를 만든다.

   - ```
     $ docker run -d -p 13306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mydb mysql:5.7
     ```
     




2. docker container에 접속 후 DB 테이블 등을 직접 만든다.

   - ```
     $ docker exec -it mydb /bin/bash
     $ mysql -uroot -p
     ```
     
   - mydb 데이타베이스와 orders, delivery_status 테이블 생성한다.
   
   - HeidiSQL 에서 실행하는 쿼리문 참고
   
   - ```mysql
     CREATE TABLE IF NOT EXISTS `delivery_status` (
         `id` int(11) NOT NULL AUTO_INCREMENT,
         `delivery_id` varchar(50) DEFAULT NULL,
         `order_json` text DEFAULT NULL,
         `status` varchar(50) DEFAULT NULL,
         `created_at` datetime DEFAULT current_timestamp(),
     	PRIMARY KEY (`id`)
     ) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
            
     CREATE TABLE IF NOT EXISTS `orders` (
         `id` int(11) NOT NULL AUTO_INCREMENT,
         `user_id` varchar(100) NOT NULL,
         `order_id` varchar(100) NOT NULL,
         `coffee_name` varchar(100) NOT NULL,
         `coffee_price` int(11) NOT NULL,
         `coffee_qty` int(11) DEFAULT 1,
         `ordered_at` varchar(50) DEFAULT NULL,
     	PRIMARY KEY (`id`)
     ) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
     ```
   
   - HeidiSQL로 접속해서 하는게 편할 것 같다.

​     


3. `delivery_ms.py` 에서 `import mariadb` 가 실행이 되지 않으므로 `import pymysql` 로 변경
   - `self.conn = pymysql.connect(**config)` 변경
   - `sql = '''UPDATE delivery_status SET status = 'COMPLETED' WHERE delivery_id=%s` 변경



4. `Dockerfile` 작성

   - 파일 이름 : `Dockerfile_delivery`

   - ```dockerfile
     FROM python:3.7.9-stretch
     
     WORKDIR /myflask
     
     RUN pip install flask
     RUN pip install flask_restful
     RUN pip install pymysql
     
     COPY ./delivery_ms.py /myflask/app.py
     
     CMD ["flask", "run", "--host", "0.0.0.0", "--port", "6000"]
     ```

   - `CMD` 명령어에서 --host 0.0.0.0을 쓰는 이유는 외부에서 도커 컨테이너에 접근하도록 하기 위함이다.



5. Docker build

   - ```
     $ docker build -t jslee6091/flask_delivery_ms -f Dockerfile_delivery .
     ```

   - 이를 실행하면 이미지가 만들어진다.



6. Docker run

   - ```
     $ docker run -d -p 16000:6000 jslee6091/flask_delivery_ms
     ```

   - 이를 실행하면 컨테이너가 실행된다.



#### kafka_docker

1. ```
   git clone https://github.com/wurstmeister/kafka-docker
   ```

2. `docker-compose-single-broker.yml` 수정

   - ```yaml
     version: '2'
     services:
       zookeeper:
         image: wurstmeister/zookeeper # 수정한 부분
         ports:
           - "2181:2181"
       kafka:
         image: wurstmeister/kafka
         ports:
           - "9092:9092"
         environment:
           KAFKA_ADVERTISED_HOST_NAME: 172.17.0.101 # 수정한 부분
           KAFKA_CREATE_TOPICS: "test:1:1"
           KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
         volumes:
           - /var/run/docker.sock:/var/run/docker.sock
         # 추가한 부분
         depends_on:
           - zookeeper
     ```

   - ```
     $ docker-compose -f docker-compose-single-broker.yml up -d
     ```

- 이거 에러나서 새로운 yml 파일로 만들려고 한다.

  - yml 파일 만들기 전에 docker network 먼저 만든다.

  - ```
    $ docker network create --gateway 172.19.0.1 --subnet 172.19.0.0/24 my-coffee-network
    ```

  - ```yaml
    # 수정한 docker-compose-single-broker.yml 파일
    version: '2'
    services:
      zookeeper:
        image: wurstmeister/zookeeper
        ports:
          - "2181:2181"
        networks:
          my-network:
            ipv4_address: 172.19.0.100
      kafka:
        image: wurstmeister/kafka
        ports:
          - "9092:9092"
        environment:
          KAFKA_ADVERTISED_HOST_NAME: 172.19.0.101
          KAFKA_CREATE_TOPICS: "test:1:1"
          KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
        volumes:
          - /var/run/docker.sock:/var/run/docker.sock
        depends_on:
          - zookeeper
        networks:
          my-network:
            ipv4_address: 172.19.0.101
    
    networks:
      my-network:
        name: my-coffee-network
    ```

  - ```
    $ docker-compose -f docker-compose-single-broker.yml up -d
    ```

  - 이렇게 하면 두가지 docker container가 생성되어 실행중에 있다. 

  - docker network 정보 확인

  - ```
    $ docker network inspect my-coffee-network
    ```

  - `my-coffee-network` 네트워크에 대한 정보에서 

  - 기존에 먼저 만든 delivery_ms 컨테이너를 종료하고 delivery_ms.py 파일 수정

  - ```python
    # delivery_ms.py 수정
    from flask import Flask, jsonify, request
    from datetime import datetime
    import uuid, json, pymysql, flask_restful # mariadb를 pymysql로 변경
    from flask_restful import reqparse
    
    app = Flask(__name__)
    # app.config["DEBUG"] = True
    api = flask_restful.Api(app)
    
    config = {
        'host': '172.19.0.2', # 수정한 부분 - mysql의 IPv4 주소로 변경
        'port': 3306,
        'user': 'root',
        'password': '', # EMPTY 이므로 공백
        'database': 'mydb'
    }
    
    @app.route('/') # 수정한 부분 - 큰 의미는 없다.
    def index():
        return "Welcome to DELIVERY Microservice!"
    
    class DeliveryGet(flask_restful.Resource):
        def __init__(self):
            self.conn = pymysql.connect(**config) # 수정한 부분 - pymysql로 변경
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
    
    
    class DeliveryPut(flask_restful.Resource):
        def __init__(self):
            self.conn = pymysql.connect(**config) # pymysql로 변경
            self.cursor = self.conn.cursor()
            
        def put(self, delivery_id):
            json_data = request.get_json()
            status = json_data['status']
    
            # 수정한 부분 - ? 를 %s 로 변경
            sql = '''UPDATE delivery_status SET status = %s WHERE delivery_id=%s'''
            self.cursor.execute(sql, [delivery_id])
            self.conn.commit()
    
            json_data['updated_at'] = str(datetime.today())
            response = jsonify(json_data)
            response.status_code = 200
            return response
    
    # GET    http://127.0.0.1:5000/delivery-ms/orders
    # PUT    http://127.0.0.1:5000/delivery-ms/deliveries/delivery_id/status
    api.add_resource(DeliveryGet, '/delivery-ms/orders')
    api.add_resource(DeliveryPut, '/delivery-ms/deliveries/<string:delivery_id>/status')
    
    
    if __name__ == '__main__':
        app.run(port=6000)
    ```

  - network 옵션과 함께 다시 생성

  - ```
  $ docker run -d -p 16000:6000 --network my-coffee-network --name delivery_ms jslee6091/flask_delivery_ms
    ```
  
  - 기존에 실행했던 mysql 컨테이너도 종료하고 network 옵션과 함께 다시 생성

  - ```
  $ docker run -d -p 13306:6000 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --network my-coffee-network --name mydb mysql:5.7
    ```
  
  - postman 에서 GET 방식으로 send 하면 아무 데이터도 전송되지 않음 (docker로 만든 mysql 데이터베이스에 아무런 데이터가 없으므로)





#### order_ms.py

1. `Dockerfile` 작성

   - 파일 이름 : `Dockerfile_order`

   - ```dockerfile
     FROM python:3.7.9-stretch
     
     WORKDIR /myflask
     
     RUN pip install flask
     RUN pip install flask_restful
     RUN pip install pymysql
     RUN pip install kafka-python
     
     COPY ./order_ms.py /myflask/app.py
     
     CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
     ```

2. `order_ms.py` 수정

   - ```python
     from flask import Flask, jsonify, request
     from datetime import datetime
     import uuid, json, flask_restful, pymysql # mariadb는 import 하지 않음
     from flask_restful import reqparse
     from kafka import KafkaProducer
     
     app = Flask(__name__)
     # app.config["DEBUG"] = True
     api = flask_restful.Api(app)
     
     config = {
         'host': '172.19.0.1', # 수정한 부분 - 내 network의 gateway 주소
         'port': 3306,
         'user': 'root',
         'password': '',		# 수정한 부분 - mysql 을 empty password 로 했음
         'database': 'mydb'
     }
     
     @app.route('/') # 수정한 부분 - 큰 의미는 없다.
     def index():
         return "Welcome to ORDER Microservice!"
     
     class Order(flask_restful.Resource):
         def __init__(self):
             self.conn = pymysql.connect(**config) # 수정한 부분 - docker에서 mariadb가 실행이 되지 않기 때문에 pymysql로 바꿨다.
             self.cursor = self.conn.cursor()
             self.producer = KafkaProducer(bootstrap_servers=['172.19.0.101:9092']) # 기존의 localhost에서 kafka-docker의 IPv4 주소로 변경
                 
         def get(self, user_id):
             # 수정한 부분 - pymysql 에서는 ?가 아니라 %s 이다.
             sql = '''select user_id, order_id, coffee_name, coffee_price, coffee_qty, ordered_at
                      from orders where user_id=%s order by id desc'''
             self.cursor.execute(sql, [user_id])
             result_set = self.cursor.fetchall()
     
             row_headers = [x[0] for x in self.cursor.description]
     
             json_data = []
             for result in result_set:
                 json_data.append(dict(zip(row_headers,result)))
             
             return jsonify(json_data)
         
         def post(self, user_id):
             json_data = request.get_json()
             
             json_data['user_id'] = user_id
             json_data['order_id'] = str(uuid.uuid4()) # randomo
             json_data['ordered_at'] = str(datetime.today())
     
             # DB insert
             # 수정한 부분 - ? 를 %s 로 변경
             sql = '''INSERT INTO orders(user_id, order_id, coffee_name, coffee_price, coffee_qty, ordered_at)
             VALUES(%s,%s,%s,%s,%s,%s)
             '''
             self.cursor.execute(sql, [user_id, json_data['order_id'],
                                                json_data['coffee_name'],
                                                json_data['coffee_price'],
                                                json_data['coffee_qty'],
                                                json_data['ordered_at']])
             self.conn.commit()
     
             # Kafka message send
             # KafkaProducer() -> 생성자에 추가
             # producer 인스턴스의 send() 메소드로 json 데이터 전송
             self.producer.send('new_orders', value=json.dumps(json_data).encode())
             self.producer.flush()
     
             # return {'coffee_name': coffee_name, 'coffee_price': coffee_price, 'coffee_qty': coffee_qty}, 201
             response = jsonify(json_data)
             response.status_code = 200
             return response
     
     class OrderDetail(flask_restful.Resource):
         def get(self, user_id, order_id):
             return {'user_id':user_id, 'order_id': order_id}
     
     # GET    http://127.0.0.1:5000/order-ms/USER0001/orders
     # POST   http://127.0.0.1:5000/order-ms/USER0001/orders
     # GET    http://127.0.0.1:5000/order-ms/USER0001/orders/ORD0001
     api.add_resource(Order, '/order-ms/<string:user_id>/orders')
     api.add_resource(OrderDetail, '/order-ms/<string:user_id>/orders/<string:order_id>')
     
     
     if __name__ == '__main__':
         app.run()
     ```

   - 도커 이미지 생성

   - ```
     $ docker build -t jslee6091/flask_order_ms -f Dockerfile .     
     ```

   - 컨테이너 빌드

   - ```
     $ docker run -d -p 15000:6000 --network my-coffee-network --name order_ms jslee6091/flask_order_ms
     ```






#### kafka_consumer.py

1. Dockerfile 생성

   - 파일 이름 : `Dockerfile_consumer`

   - ```dockerfile
     FROM python:3.7.9-stretch
     
     WORKDIR /mykafka
     
     RUN pip install pymysql
     RUN pip install kafka-python
     
     COPY ./kafka_consumer.py /mykafka/app.py
     
     CMD ["python", "/mykafka/app.py"]
     ```

2. `kafka_consumer.py` 수정

   - ```python
     from kafka import KafkaConsumer
     import time, json, uuid, pymysql # mariadb import 제거
     import threading
     from datetime import datetime
     
     # 수정한 부분 - bootstrap_servers 의 주소를 localhost 에서 kafka-docker의 IPv4 주소로 변경
     consumer = KafkaConsumer('new_orders',
                              bootstrap_servers=["172.19.0.101:9092"],
                              auto_offset_reset='earliest',
                              enable_auto_commit=True,
                              auto_commit_interval_ms=1000,
                              consumer_timeout_ms=1000)
     
     config = {
         'host': '172.19.0.2', # 수정한 부분 - 내 mysql 의 IPv4 주소로 변경
         'port': 3306,
         'user': 'root',
         'password': '', # 비밀 번호 EMPTY 로 했으므로 삭제
         'database': 'mydb'
     }
     conn = pymysql.connect(**config) # mariadb에서 pymysql로 변경
     cursor = conn.cursor()
     # ? -> %s 로 수정
     sql = '''INSERT INTO delivery_status(delivery_id, order_json, status)
             VALUES(%s,%s,%s)'''
     
     def fetch_latest_orders(next_call_in):
         # 30초에 한번씩 가져오기
         next_call_in += 30
     
         # consumer의 데이터 읽어오는 함수 poll
         batch = consumer.poll(timeout_ms=100)
         if len(batch) > 0:
             for message in list(batch.values())[0]:
                 value = message.value.decode()
                 
                 delivery_id = str(uuid.uuid4())
                 status = 'CONFIRMED'
                 # DB insert
                 cursor.execute(sql, [delivery_id, value, status])
                 conn.commit()
     
         threading.Timer(next_call_in - time.time(), fetch_latest_orders, [next_call_in]).start()
     
     next_call_in = time.time()
     fetch_latest_orders(next_call_in)
     ```

   - 도커 이미지 생성

   - ```
     $ docker build -t jslee6091/kafka_consumer_ms -f Dockerfile .  
     ```

   - 도커 컨테이너 빌드

   - ```
     $ docker run -d --network my-coffee-network --name kafka_consumer jslee6091/kafka_consumer_ms
     ```






#### postman으로 확인

- order_ms
  - GET 또는 POST 방식에 따라 적절한 URL과 데이터를 입력하여 데이터를 읽거나(GET), 데이터를 저장한다.(POST)
  - 제대로 실행되었다면 orders 테이블에 데이터가 저장되어있다. 
- kafka_consumer
  - order_ms로부터 데이터를 넘겨 받아 delivery_status 테이블에 저장한다.
  - order_ms를 실행하여 
- deliver_ms
  - URL을 입력하고 GET을 통해 저장된 데이터를 확인한다.