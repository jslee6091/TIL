### kafka basic

- 먼저 kafka 사이트에서 tgz파일을 다운받는다.

  - `kafka_2.13-2.7.0.tgz` 파일

- tgz파일 압축 해제 후 terminal 실행

- 첫번째 terminal에서 다음 명령어 실행

  - `kafka_2.13-2.7.0` 디렉터리
  
  - ```
  $ bin/windows/zookeeper-server-start.bat config/zookeeper.properties
    ```

  - zookeeper를 설치하는 명령어이다.
  
  - 자바가 설치되어 있어야 함.



- 두번째 terminal을 열어서 다음 명령어 실행

  - `kafka_2.13-2.7.0` 디렉터리
  
  - ```
    $ bin/windows/kafka-server-start.bat config/server.properties
    ```



- 세번째 terminal을 열어서 다음 명령어 실행하여 topic 생성

  - `kafka_2.13-2.7.0` 디렉터리
  
  - ```
  $ bin/windows/kafka-topics.bat --create --topic quickstart-events --bootstrap-server localhost:9092
    ```
  
  - ```
  Created topic quickstart-events.
    ```
  
  - `quickstart-events` 라는 이름의 topic이 생성됨



- 현재 생성된 topic 리스트 확인 명령어

  - `kafka_2.13-2.7.0` 디렉터리
  
  - ```
  $ bin/windows/kafka-topics.bat --list --bootstrap-server localhost:9092
    ```
  
  - ```
  quickstart-events
    ```
  
  - 현재 생성된 topic 리스트가 `quickstart-events` 하나이므로 이것만 보여준다.



- topic에 대한 상세 정보 확인

  - `kafka_2.13-2.7.0` 디렉터리
  
  - ```
  $ bin/windows/kafka-topics.bat --describe --topic quickstart-events --bootstrap-server localhost:9092
    ```
  
  - ```
    Topic: quickstart-events        PartitionCount: 1       ReplicationFactor: 1    Configs: segment.bytes=1073741824
          Topic: quickstart-events        Partition: 0    Leader: 0       Replicas: 0     Isr: 0
    ```
  
  - `quickstart-events` topic에 대한 상세 정보



- 구독 시작

  - `kafka_2.13-2.7.0` 디렉터리
  
  - ```
  $ bin/windows/kafka-console-consumer.bat --topic quickstart-events --from-beginning --bootstrap-server localhost:9092
    ```

  - 구독을 시작한다.
  
  - 메시지를 수신할 수 있는 상태이다.



- 네번째 terminal 열어서 다음 명령어 실행

  - `kafka_2.13-2.7.0` 디렉터리
  
  - ```
  $ bin/windows/kafka-console-producer.bat --topic quickstart-events --bootstrap-server localhost:9092
    ```
  
  - ```
    > hello
    > kafka
    ```
  - 명령어를 입력하면 다음과 같이 메시지를 전송할 수 있다. `hello` 와 `kafka` 라는 메시지를 입력하면 구독을 시작했던 세번째 terminal에서 이 메시지가 수신된다. 즉, 통신이 됨.



- topic 삭제하기

  - `kafka_2.13-2.7.0` 디렉터리
  
  - ```
  $ bin/windows/kafka-topics.bat --delete --topic quickstart-events --zookeeper localhost:2181
    ```

  - 이걸 입력하면 두번째 terminal 에서 shutdown 메시지가 뜨면서 종료됨

  - `C:\tmp` 디렉터리에서 kafka log 파일 삭제

  - 첫번째 terminal 에서 ctrl + c 버튼으로 종료시킨 후 zookeeper 파일 삭제

  - topic 삭제 완료.
  
  - topic을 삭제하기 위해서 tmp 디렉터리의 파일들을 삭제하는 과정은 windows 에서만 해야한다. linux, macOS에선는 삭제 명령어만 입력하면 된다.



- python으로 kafka 메시지 전송하기

  - ```
    $ cd ..
    $ mkdir kafka_client
    $ pip install kafka-python
    ```

  - `kafka_consumer.py` 작성

  - ```python
    from kafka import KafkaConsumer
    from json import loads
    import time
    
    consumer = KafkaConsumer('topic_users', bootstrap_servers=['127.0.0.1:9092'], auto_offset_reset='earliest', enable_auto_commit=True, group_id='my-group', value_deserializer=lambda x: loads(x.decode('utf-8')), consumer_timeout_ms=1000)
    
    start = time.time()
    
    for message in consumer:
    	topic = message.topic
    	partition = message.partition
    	offset = message.offset
    	key = message.key
    	value = message.value
    	print("Topic:{}, Partition:{}, Offset:{}, Key:{}, Value:{}".format(topic, partition, offset, key, value))
    
    print("Elapsed: ", (time.time() - start))
    ```

  - `topic_users` 라는 이름의 topic을 새로 생성한다.

  - 메시지가 전송되는 것을 확인

  - `kafka_producer.py` 작성

  - ```python
    from gzip import compress
    from kafka import KafkaProducer
    from json import dumps
    import time
    
    # dict (key, value) -> object
    # str -> string
    
    producer = KafkaProducer(acks=0, 
                compression_type='gzip', 
                bootstrap_servers=['127.0.0.1:9092'], 
                value_serializer=lambda x : dumps(x).encode('utf-8')) 
    
    start = time.time()
    for i in range(10):
        data = {'name': 'jaesung-' + str(i)}
        producer.send('topic_users', value=data)
        producer.flush()
    
    print("Done.  Elapsed time: ", (time.time() - start))
    ```

  - 실행하면 10개의 메시지가 전송된다.



### 로컬의 MariaDB을 이용한 Kafka source connect, sink connect



##### DB 테이블 생성

- 로컬의 MariaDB에 접속 후 mydb database 생성

- 다음과 같은 쿼리문 작성

  - ```mariadb
    use mydb;
    create table users(
    	id int auto_increment primary key,
    	user_id varchar(20) not null,
    	pwd varchar(20) not null,
	created_at datetime default now()
    );
    ```
    
  - users 테이블이 생성됨



##### kafka connect를 위한 설치 및 환경 설정

- confluent 설치

  - 아래 명령어로 tar.gz 파일 설치

  - ```
    $ curl -O http://packages.confluent.io/archive/6.1/confluent-community-6.1.0.tar.gz
    ```

  - 압축 해제

  - ```
    $ tar xvf confluent-community-6.1.0.tar.gz
    ```

  - `confluent-6.1.0` 디렉터리가 생성됨



- jdbc 설치

  - 다음 사이트에서 zip 파일 다운로드

  - ```
    https://docs.confluent.io/5.5.1/connect/kafka-connect-jdbc/index.html
    ```

  - Install the connector manually 의 zip file 다운로드를 클릭하면 나오는 웹 페이지에서 다운로드 실행
  
  - `unzip jdbc파일` 명령어로 압축 해제 하면 `confluentinc-kafka-connect-jdbc-10.1.0` 디렉터리가 생김



- kafka Connect 실행

  - ```
    ./bin/windows/connect-distributed.bat ./etc/kafka/connect-distributed.properties
    ```

  - `confluent-6.1.0` 디렉터리에서 실행

  - 아래와 같은 오류가 발생한다.

  - ```
    Classpath is empty. Please build the project first e.g. by running 'gradlew jarAll'
    ```

  - 오류 해결을 위해 코드를 수정한다.

  - ```
    $ code bin/windows/kafka-run-class.bat
    ```

  - ```
    # rem Classpath addition for core 바로 위쪽에 코드 추가
    
    rem classpath addition for LSB style path
    if exist %BASE_DIR%\share\java\kafka\* (
    	call:concat %BASE_DIR%\share\java\kafka\*
    )
    ```

  - 추가적으로 다음과 같이 jar 파일을 옮기고 plugin.path 코드를 수정한다.

  - `mariadb-java-client-2.7.2.jar` 파일을 복사하여 `confluent-6.1.0/share/java/kafka` 에 붙여넣기

  - terminal 에서 `$ code etc/kafka/connect-distributed.properties` 입력하여 코드 수정

  - ```properties
    # 맨 밑에 아래 구문 추가
    # 기존의 plugin.path 문장은 주석 처리
    plugin.path=\C:\\confluentinc-kafka-connect-jdbc-10.1.0\\lib
    ```





##### Kafka Source Connect 추가



- Kafka Source Connect를 MariaDB와 연동시키기

  - kafka topic을 생성한다.

    - ```
      $ bin/windows/kafka-topics.bat --create --topic my_topic_users --bootstrap-server localhost:9092
      ```
  
    - topic 이름은 `my_topic_users`
  
  - Source Connect는 kafka와 DB를 연동하는 것으로 DB의 특정 테이블의 데이터를 kafka로 보낼 수 있다.
  
  - kafka connect 를 위한 confluent 실행
  
    - ```
      .\bin\windows\connect-distributed.bat .\etc\kafka\connect-distributed.properties
      ```
  
    - 작업 디렉토리 : `confluent-6.1.0`
  
    - Error 뜨는데 무시해도 됨
  
  - postman에 접속
  
  - POST 방식으로 URL은 http://localhost:8083/connectors 입력
  
  - Body -> raw -> Text를 JSON으로 바꾸고 코드 추가
    - echo에 대한 부분만 입력 (curl 문장은 제외)
    
    - password는 본인에 맞게 수정 (없으면 지우기)
    
    - ```json
      {
          "name" : "my-source-connect",
          "config" : {
              "connector.class" : "io.confluent.connect.jdbc.JdbcSourceConnector",
              "connection.url":"jdbc:mysql://localhost:3306/mydb",
              "connection.user":"root",
              "connection.password":"mysql",
              "mode": "incrementing",
              "incrementing.column.name" : "id",
              "table.whitelist":"users",
              "topic.prefix" : "my_topic_",
              "tasks.max" : "1"
          }
      }
      
      ```
    
  - send 클릭
  
  - 이렇게 하면 `my_topic_users`라는 이름의 topic이 데이터베이스와 연결되어 데이터를 kafka로 보낼 수 있다.
  
  - GET 방식으로 URL은 동일하게 설정하여 send클릭하면 POST로 보낸 데이터를 받을 수 있음
  
  - 또는 kafka topic 구독하는 명령어로 topic에 들어오는 데이터를 확인할 수 있다.
  
    - ```
      $ bin/windows/kafka-console-consumer.bat --topic my_topic_users --from-beginning --bootstrap-server localhost:9092
      ```



- DB에 데이터를 추가하고 kafka에서 확인

  - MariaDB 데이터베이스에 데이터 추가

    - ```mariadb
      insert into users(user_id, pwd)
      values('user2', 'teset2222');
      ```


  - topic 확인 - kafka topic 구독 명령어로 확인
  - 추가된 데이터를 확인할 수 있다.



##### Kafka Sink Connect 추가



- sink connect는 kafka topic에 저장된 데이터를 다른 DB 테이블에 저장하는 기능을 수행한다.

- Postman에서 다음과 같은 JSON 파일 작성

- ```json
  {
      "name" : "JaeSungLee_sink_connect",
      "config" : {
          "connector.class" : "io.confluent.connect.jdbc.JdbcSinkConnector",
          "connection.url":"jdbc:mysql://multicampus-clouda.cgx0gwgzdjyz.us-east-1.rds.amazonaws.com/mydb",
          "connection.user":"admin",
          "connection.password":"test1357",
          "auto.create":"true",
          "auto.evolve":"true",
          "delete.enabled":"false",
          "tasks.max" : "1",
          "topics":"JaeSungLee_exam_topicusers"
      }
  }
  ```

- 이 파일은 수행평가 과제를 위해 만든 파일인데 aws에 존재하는 데이터베이스에 데이터를 저장하기 위한 것이다.

- URL은 http://localhost:8083/connectors 로 source connect와 동일하다.

- POST 방식으로 send 클릭

- 성공했다면 해당 데이터베이스 테이블에 kafka topic의 데이터가 저장되어있다.

- 만약 source connect와 연결된 DB에서 데이터를 추가하면 sink connector에 연결된 DB에서도 같은 데이터가 추가된다. 즉, DB가 서로 연결된다.





### source/sink connector 삭제

- 생성된 connector 삭제하기
- Postman에서 HTTP DELETE method로 send 클릭하면 된다.
- URL : http://localhost:8083/connectors/[생성한 source/sink connector의 이름]