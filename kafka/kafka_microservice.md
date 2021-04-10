### 커피 주문 처리 Microservice 만들기



1. 커피 주문을 처리하는 MS

   - 사용자 요청으로 전달 된 커피 주문을 ORDER MS의 DB에 저장

   - endpoint: GET /order-ms/[user_id]/orders/

     - 주문 목록 보기

   - endpoint: GET /order-ms/[user_id]/orders/[order_id]

     - 주문 상세 보기

   - endpoint: POST /order-ms/[user_id]/orders/

     ```json
     {
         "coffee_name": "today's coffee",
         "coffee_price": "5000",
         "coffee_qty": "3"
     }
     ```

   - DB에 주문 정보 저장

   - 추가된 주문 정보를 kafka에 전송

2. ORDER MS에 전달 된 커피 주문 정보를 ORDER DELIVERY MS로 전달

   - ORDER MS의 DB에 저장된 커피 정보를 ORDER DELIVERY MS의 DB에 저장
   - endpoint: GET /delivery-ms/[status]
     - 현재 status(접수완료 ...)에 있는 주문을 모두 표시
   - endpoint: GET /delivery-ms/[user_id]/[order_id]
     - 커피의 주문 상태를 표시 ex) 접수완료, 제작중, 배송완료, 취소 ...







### 실습

1. anaconda prompt 실행

2. ```
   $ conda create -n msa python=3.8 flask
   ```

3. ```
   $ conda activate msa
   ```

4. ```
   $ mkdir flask_demo
   # cd flask_demo
   $ code .
   ```

5. ```python
   # app.py
   from flask import Flask
   
   app = Flask(__name__)
   
   @app.route('/')
   def index():
       return "Hello, World!"
   
   if __name__ == "__main__":
       app.run()
   ```

6. ```
   $ flask run
   * Environment: production
     WARNING: This is a development server. Do not use it in a production deployment.
     Use a production WSGI server instead.
   * Debug mode: off
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

7. 웹브라우저에 `127.0.0.1:5000` 입력하면 다음 문장이 있는 웹페이지에 접속됨

   - ```
     # 실행 결과
     Hello, World!
     ```

8. ```python
   # app.py
   from flask import Flask
   
   app = Flask(__name__)
   
   @app.route('/')
   def index():
       return "Hello, World!"
   
   @app.route('/health-check')
   def health_check():
       return "Server is running on 5000 port"
   
   if __name__ == "__main__":
       app.run()
   ```

   - 위와 같이 app.py에 health-check 추가

9. Ctrl+c 누른후 `$ flask run` 실행하고 웹 브라우저에서 `127.0.0.1:5000/health-check`입력

   - ```
     # 실행 결과
     Server is running on 5000 port
     ```

10. ```python
    # app.py
    from flask import Flask
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return "Hello, World!"
    
    @app.route('/health-check')
    def health_check():
        return "Server is running on 5000 port"
    
    @app.route('/users')
    def users():
        return "** Users List"
    
    @app.route('/users/<userId>')
    def users_detail(userId):
        return "Welcome to Flask App, {}".format(userId)
    
    if __name__ == "__main__":
        app.run()
    ```

    - `app.py` 위와 같이 수정

11. Ctrl+c 누른후 `$ flask run` 실행하고 웹 브라우저에서  확인

    - `127.0.0.1:5000/users`

    - ```
      # 실행 결과
      ** Users List
      ```

    - `127.0.0.1:5000/users/user01`

    - ```
      # 실행 결과
      Welcome to Flask App, user01
      ```

12. ```
    $ flask run --port 3000
    ```

    - 앞서 만든 웹 페이지들을 3000번 포트로 접속하게 만듦

13. JSON 포멧처럼 데이터를 보내기

    - `app.py`에서 `users_detail(userId)`함수를 JSON 포멧을 return 하도록 바꾸기

    - ```python
      # app.py
      from flask import Flask
      
      app = Flask(__name__)
      
      @app.route('/')
      def index():
          return "Hello, World!"
      
      @app.route('/health-check')
      def health_check():
          return "Server is running on 5000 port"
      
      @app.route('/users')
      def users():
          return "** Users List"
      
      @app.route('/users/<userId>')
      def users_detail(userId):
          return "{\"name\":%s}" %(userId)
      	# return jsonify({"user_id": userId})
      
      if __name__ == "__main__":
          app.run()
      ```

    - 웹 브라우저에서 `127.0.0.1:5000/users/user01`을 입력하면 JSON 포멧으로 데이터를 볼 수 있다.

      - ```
        # 실행 결과
        {"name":user01}
        ```

    - 주석 처리된 `jsonify`를 이용하면 웹브라우저에서 더 보기 좋은 json 포멧으로 볼 수 있다. 이를 위해서는 chrome plugin을 설치해야 한다.

      - ```
        # 실행 결과
        {"user_id":"user01"}
        ```

      - postman으로 접속하면 chrome plugin이 있을때 처럼 json 파일을 볼 수 있다.

14. app.py 수정 - `userAdd()` 함수 추가

    - ```python
      # app.py
      from flask import Flask, jsonify, request
      
      app = Flask(__name__)
      
      @app.route('/')
      def index():
          return "Hello, World!"
      
      @app.route('/health-check')
      def health_check():
          return "Server is running on 5000 port"
      
      @app.route('/users')
      def users():
          return "** Users List"
      
      @app.route('/users/<userId>')
      def users_detail(userId):
          # return "{\"name\":%s}" %(userId)
          return jsonify({"user_id": userId})
      
      @app.route('/users', methods = ['POST'])
      def userAdd():
          user = request.get_json()
          # db에 추가
          # kafka에 전송
          return jsonify(user)
      
      if __name__ == "__main__":
          app.run()
      ```

15. user_id을 보내고 확인하기

    - ```python
      # app.py
      from flask import Flask, jsonify, request
      from datetime import datetime
      import uuid
      
      app = Flask(__name__)
      
      @app.route('/')
      def index():
          return "Hello, World!"
      
      @app.route('/health-check')
      def health_check():
          return "Server is running on 5000 port"
      
      @app.route('/users')
      def users():
          return "** Users List"
      
      @app.route('/users/<userId>')
      def users_detail(userId):
          # return "{\"name\":%s}" %(userId)
          return jsonify({"user_id": userId})
      
      @app.route('/users', methods = ['POST'])
      def userAdd():
          user = request.get_json()
          # user['user_id'] = 'USER-0001'
          user['user_id'] = uuid.uuid4() # uuid1() ~ uuid5()
          user['created_at'] = datetime.today()
          # user['created_at'] = "2021-04-05" <- 이렇게 날짜를 직접 입력해도 됨
          # db에 추가
          # kafka에 전송
          return jsonify(user)
      
      if __name__ == "__main__":
          app.run()
      ```

    - postman에서 `http://127.0.0.1:5000/users` 와 `POST`로 설정 후 Body의 raw 설정 후 JSON 데이터에서 다음과 같이 데이터 입력후 send 클릭

      - ```json
        {
            "name": "test1",
            "email": "test1@example.com"
        }
        ```

      - ```json
        # 출력 결과
        {
            "created_at": "Mon, 05 Apr 2021 11:33:21 GMT",
            "email": "test1@example.com",
            "name": "test1",
            "user_id": "3c55b5d4-0a26-4a3e-adbe-eefe025ea7b2"
        }
        ```

    - postman에서 결과 부분 우측 상단에 보면 `200 OK`라는 메시지가 있는데 이것을 `201 CREATED` 메시지로 수신받게 할 수 있다.
    
    - ```python
      # app.py 에서 UserAdd() 함수를 수정
      @app.route('/users', methods = ['POST'])
      def userAdd():
          user = request.get_json()
          # user['user_id'] = 'USER-0001'
          user['user_id'] = uuid.uuid4() # uuid1() ~ uuid5()
          user['created_at'] = datetime.today()
          # user['created_at'] = "2021-04-05" <- 이렇게 날짜를 직접 입력해도 됨
          # db에 추가
          # kafka에 전송
          # 200 OK -> 201 Created
          return jsonify(user), 201
      ```







### 커피 주문 Microservice에 대한 힌트

- 새로운 작업 디렉터리 생성하여 코드를 작성

  - ```
    $ mkdir flask_demo2
    $ cd flask_demo2
    $ code .
    ```

- 먼저 필요한 패키지 설치

  - ```
    $ pip install flask_restfull
    ```

  - ```
    $ pip install mariadb
    ```

- 코드 작성 (`rest1.py`)

  - ```python
    from flask import Flask, jsonify
    import flask_restful
    from flask_restful import reqparse
    
    app = Flask(__name__)
    app.config["DEBUG"] = True
    api = flask_restful.Api(app)
    
    def multiply(param1, param2):
        return param1 * param2
    
    @app.route('/')
    def index():
        return "Hello, Flask!"
    
    class HelloWorld(flask_restful.Resource):
        def get(self):
            parser = reqparse.RequestParser()
            
            # Query String
            # GET /api/multiply?param1=3&param2=4
            parser.add_argument('param1')
            parser.add_argument('param2')
            args = parser.parse_args()
    
            param1 = args['param1']
            param2 = args['param2']
    
            if (not param1) or (not param2):
                return {
                    'state': 0,
                    'response': None
                }
            
            param1 = int(param1)
            param2 = int(param2)
    
            result = multiply(param1, param2)
            return {
                'state': 1,
                'response': result
            }
    
    # GET, POST, PUT, DELETE ...
    # /api/multiply -> GET, POST
    # 주문 목록 /orders (GET)
    # 주문 하기 /orders (POST)
    # 주문 상세보기 /orders/ID (GET)
    # 주문 수정하기 /orders/ID (PUT)
    # 주문 삭제하기 /orders/ID (DELETE)
    
    api.add_resource(HelloWorld, '/api/multiply')
    
    if __name__== '__main__':
        app.run()
    ```

- 코드 실행

  - ```
    $ set FLASK_APP=rest1.py
    ```

  - ```
    $ flask run --port 8000
    ```

  - 웹 브라우저에 `127.0.0.1:8000/api/multiply?param1=3&param2=4`입력

  - ```
    # 실행 결과
    {"state": 1, "response": 12}
    ```

  - postman에서도 실행하면 같은 결과 얻을 수 있음



- 단위 테스트 만들기

  - `rest1_test.py`작성

  - ```python
    import unittest
    import json
    import rest1
    
    class FlaskTest(unittest.TestCase):
        # 테스트를 위한 초기화 작업들
        def setUp(self):
            rest1.app.testing = True
            self.client = rest1.app.test_client()
    
        # # 리소스 반환
        # def tearDown(self):
        #     pass
    
        def test_index(self):
            self.assertTrue(True)
    
    if __name__ == '__main__':
        unittest.main()
    ```

  - 단순히 test.py 코드가 잘 작동하는지 확인하기 위한 코드임
  - `test_index`함수에서 `assertTrue(True)`는 무조건 `True`를 반환함

- 코드 실행

  - ```
    $ python rest1_test.py
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.004s
    
    OK
    ```

  - 만약 `assertTrue(False)`로 설정했다면 다음과 같은 결과가 나옴

  - ```
    $ python rest1_test.py
    Traceback (most recent call last):
      File "rest1_test.py", line 16, in test_index
        self.assertTrue(False)
    AssertionError: False is not true
    
    ----------------------------------------------------------------------
    Ran 1 test in 0.002s
    
    FAILED (failures=1)
    ```

- 반환이 제대로 되는지 확인하는 테스트

  - ```python
    import unittest
    import json
    import rest1
    
    class FlaskTest(unittest.TestCase):
        # 테스트를 위한 초기화 작업들
        def setUp(self):
            rest1.app.testing = True
            self.client = rest1.app.test_client()
    
        # # 리소스 반환
        # def tearDown(self):
        #     pass
    
        def test_index(self):
            response = self.client.get('/')
    
            # response code : 200
            self.assertEqual(response.status_code, 200)
            # content type : test/html; charset=utf-8
            # self.assertEqual("text/html; charset=utf-8", response.content_type)
            self.assertIn("text/html", response.content_type)
    
    
    if __name__ == '__main__':
        unittest.main()
    ```

  - 실행 결과
  
  - ```
    $ python rest1_test.py
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.008s
    
    OK
    ```
  
  - 반환 데이터 확인 위한 코드 - `test_index(self)` 함수만 수정
  
  - ```python
    def test_index(self):
    	response = self.client.get('/')
    
    	# response code : 200
    	self.assertEqual(response.status_code, 200)
    	# content type : test/html; charset=utf-8
    	# self.assertEqual("text/html; charset=utf-8", response.content_type)
    	self.assertIn("text/html", response.content_type)
        self.assertEqual(response.charset, 'utf-8')
    
        content = response.data
            
        # 반환 데이터 확인
        # Hello, Flask! 와 같은지 여부를 알려준다.
        self.assertEqual(content.decode('utf-8'), 'Hello, Flask!')
    ```
  
  - 실행 결과
  
  - ```
    $ python rest1_test.py
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.005s
    
    OK
    ```
  
  - 이때 `assertEqual`함수에서 `utf-8`로 decode를 해주어야 한다. 그렇지 않으면 에러가 발생함.
  
  - 'Hello, Flask!'를 제대로 입력 하지 않으면 `Failed` 되므로 정확한 결과 확인을 위해 오타를 방지 해야함
  
- multiply 테스트

  - postman 에서 얻은 아래 결과에 대한 테스트를 진행하는 것이다.

  - ```json
    {
        "state": 1,
        "response": 12
    }
    ```

  - 코드 수정 - 아래 메소드를 `FlaskTest` 클래스에 추가

  - ```python
    def test_multiply(self):
        response = self.client.get('/api/multiply?param1=3&param2=4')
    
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
    
        # TDD(Test Driven Development)
        json_result = json.loads(response.data)
        self.assertEqual(json_result.get('state'), 1)
        self.assertEqual(json_result.get('response'), 12)
    ```

  - ```
    # 실행 결과
    $ python rest1_test.py
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.008s
    
    OK
    ```






### 커피 주문 Microservice

- 앞서 만든 test 코드를 기반으로 작성

- `order_ms.py`작성

  - ```python
    from flask import Flask, jsonify, request
    from datetime import datetime
    import uuid, json, mariadb, flask_restful
    from flask_restful import reqparse
    
    app = Flask(__name__)
    app.config["DEBUG"] = True
    api = flask_restful.Api(app)
    
    @app.route('/order-ms')
    def index():
        return "Welcome to ORDER Microservice!"
    
    class Order(flask_restful.Resource):
        def get(self, user_id):
            return {'user_id':user_id}
        def post(self, user_id):
            return {'user_id':user_id}, 201
    
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

  - 코드 실행

    - ```
      $ python order_ms.py
      ```

    - 다른 서버 실행중인거 종료시킨 후 실행

    - 코드를 실행하면 서버가 실행됨

  - 

  - 웹 브라우저에서 결과 확인

    - Order의 GET 확인 : 주소창에 `127.0.0.1:5000/order-ms/USER0001/orders` 입력

    - ```json
      # 실행 결과
      {
          "user_id": "USER0001"
      }
      ```

    - Order의 POST 확인 : postman 에서 URL을 `127.0.0.1:5000/order-ms/USER0001/orders`입력 후 JSON 파일로 값을 입력 후 send

    - OrderDetail의 GET 확인 : 주소창에 `127.0.0.1:5000/order-ms/USER0001/orders/ORD0001` 입력

    - ```json
      # 실행 결과
      {
          "user_id": "USER0001",
          "order_id": "ORD0001"
      }
      ```

  - postman 에서도 같은 방식으로 결과를 확인할 수 있다. 이때 `127.0.0.1:5000/order-ms/USER0001/orders/ORD0001`에 대한 결과 상태 코드는 `201 CREATED` 이다.



- DB 연동

  > 로컬의 MySQL 사용하거나 Docker로 MySQL DB 만들고 사용함

- mydb database 생성 후 쿼리문 작성

  - ```mysql
    create table orders (
    	id int auto_increment primary key,
        user_id varchar(100) not null,
    	order_id varchar(100) not null,
    	coffee_name varchar(100) not null,
    	coffee_price int not null,
    	coffee_qty int default 1,
    	ordered_at varchar(50)
    )
    ```

- `order_ms.py` 수정

  - ```python
    from flask import Flask, jsonify, request
    from datetime import datetime
    import uuid, json, mariadb, flask_restful
    from flask_restful import reqparse
    
    app = Flask(__name__)
    app.config["DEBUG"] = True
    api = flask_restful.Api(app)
    
    config = {
        'host': '',
        'port': 3306,
        'user': 'root',
        'password': 'mysql',
        'database': 'mydb'
    }
    
    @app.route('/order-ms')
    def index():
        return "Welcome to ORDER Microservice!"
    
    class Order(flask_restful.Resource):
        def get(self, user_id):
            # config 데이터 매개변수로 전달
            conn = mariadb.connect(**config)
            cursor = conn.cursor()
            # 최신 데이타 반환 - user_id 만 반환
            sql = "select * from orders orders where user_id=? order by id desc"
            cursor.execute(sql, [user_id])
            result_set = cursor.fetchall()
    
            json_data = []
            for result in result_set:
                json_data.append(result)
            
            return jsonify(json_data)
        
        def post(self, user_id):
            return {'user_id':user_id}, 201
    
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

  - 코드 실행

  - ```
    $ python order_ms.py
    ```

  - 웹 브라우저 또는 postman에서 `127.0.0.1:5000/order-ms/USER0001/orders` 입력

  - 아직 데이터를 입력하지 않았으므로 아래와 같이 비어있는 데이터가 출력된다.

  - ```
    # 결과
    []
    ```

 - DB에 데이터 입력하기 (POST 방식 이용)

   - 코드 수정

   - ```python
     from flask import Flask, jsonify, request
     from datetime import datetime
     import uuid, json, mariadb, flask_restful
     from flask_restful import reqparse
     
     app = Flask(__name__)
     app.config["DEBUG"] = True
     api = flask_restful.Api(app)
     
     config = {
         'host': '',
         'port': 3306,
         'user': 'root',
         'password': 'mysql',
         'database': 'mydb'
     }
     
     @app.route('/order-ms')
     def index():
         return "Welcome to ORDER Microservice!"
     
     class Order(flask_restful.Resource):
         def get(self, user_id):
             # config 데이터 매개변수로 전달
             conn = mariadb.connect(**config)
             cursor = conn.cursor()
             # 최신 데이타 반환 - user_id 만 반환
             sql = "select * from orders orders where user_id=? order by id desc"
             cursor.execute(sql, [user_id])
             result_set = cursor.fetchall()
     
             json_data = []
             for result in result_set:
                 json_data.append(result)
             
             return jsonify(json_data)
         
         def post(self, user_id):
             # 데이터 보내는 방법 1
             # parser = reqparse.RequestParser()
     
             # parser.add_argument('coffee_name')
             # parser.add_argument('coffee_price')
             # parser.add_argument('coffee_qty')
            
             # args = parser.parse_args()
     
             # coffee_name = args['coffee_name']
             # coffee_price = args['coffee_price']
             # coffee_qty = args['coffee_qty']
     
             # 데이터 보내는 방법 2 -> postman에서 JSON 데이터 잘못 보내면 500 오류 발생
             # 이것이 더 간단해보임
             json_data = request.get_json()
             
             coffee_name = json_data['coffee_name']
             coffee_price = json_data['coffee_price']
             coffee_qty = json_data['coffee_qty']
     
             # DB insert
     
             return {'coffee_name': coffee_name, 'coffee_price': coffee_price, 'coffee_qty': coffee_qty}, 201
             
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

   - 코드 실행

     - 데이터 보내는 두가지 방법 모두 실행 방식은 같음

     - postman 에서 `127.0.0.1:5000/order-ms/USER0001/orders` 주소 입력 후 다음 데이터를 입력 후 send 클릭

     - ```json
       {
           "coffee_name": "jslee",
           "coffee_price": "1000",
           "coffee_qty": "5"
       }
       ```

     - 실행 결과 post 함수에서 반환하는 데이터들이 나타난다.

     - ```json
       {
           "coffee_name": "jslee",
           "coffee_price": "1000",
           "coffee_qty": "5"
       }
       ```

     - 입력 했던 데이터들이 그대로 출력됨을 알 수 있다.

   - 코드 수정

   - ```python
     # post 함수를 다음과 같이 수정
     # 데이터 보내는 방법 1
             # parser = reqparse.RequestParser()
     
             # parser.add_argument('coffee_name')
             # parser.add_argument('coffee_price')
             # parser.add_argument('coffee_qty')
            
             # args = parser.parse_args()
     
             # coffee_name = args['coffee_name']
             # coffee_price = args['coffee_price']
             # coffee_qty = args['coffee_qty']
     
             # 데이터 보내는 방법 2 -> postman에서 JSON 데이터 잘못 보내면 500 오류 발생
             # 이것이 더 간단해보임
             json_data = request.get_json()
             
             json_data['user_id'] = user_id
             json_data['order_id'] = str(uuid.uuid4()) # randomo
             json_data['ordered_at'] = str(datetime.today())
     
             # coffee_name = json_data['coffee_name']
             # coffee_price = json_data['coffee_price']
             # coffee_qty = json_data['coffee_qty']
     
             # DB insert
     
             # return {'coffee_name': coffee_name, 'coffee_price': coffee_price, 'coffee_qty': coffee_qty}, 201
             response = jsonify(json_data)
             response.status_code = 200
             return response
     ```

   - 실행 결과

   - 이전과 똑같은 데이터를 POST로 전송

   - ```json
     {
         "coffee_name": "jslee",
         "coffee_price": "1000",
         "coffee_qty": "5",
         "order_id": "7b26f3d1-7df3-4374-92fe-33a1bc1a5362",
         "ordered_at": "2021-04-05 17:59:02.321874",
         "user_id": "USER0001"
     }
     ```

   - 실행 결과 위와 같은 데이터가 출력된다.
   
   - 하지만 DB에 insert 하지 않았기 때문에 Mariadb에서는 데이터가 저장되지 않는다.
