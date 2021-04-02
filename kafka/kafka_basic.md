### kafka basic

- 먼저 kafka 사이트에서 tgz파일을 다운받는다.

- tgz파일 압축 해제 후 terminal 실행

- 첫번째 terminal에서 다음 명령어 실행

  - ```
    $ bin\windows\zookeeper-server-start.bat config\zookeeper.properties
    ```

  - zookeeper를 설치하는 명령어이다.

  - 자바가 설치되어 있어야 함.



- 두번째 terminal을 열어서 다음 명령어 실행

  - ```
    $ bin/windows/kafka-server-start.bat config/server.properties
    ```



- 세번째 terminal을 열어서 다음 명령어 실행하여 topic 생성

  - ```
    $ bin/windows/kafka-topics.bat --create --topic quickstart-events --bootstrap-server localhost:9092
    ```

  - ```
    Created topic quickstart-events.
    ```

  - `quickstart-events` 라는 이름의 topic이 생성됨



- 현재 생성된 topic 리스트 확인 명령어

  - ```
    $ bin/windows/kafka-topics.bat --list --bootstrap-server localhost:9092
    ```

  - ```
    quickstart-events
    ```

  - 현재 생성된 topic 리스트가 `quickstart-events` 하나이므로 이것만 보여준다.



- topic에 대한 상세 정보 확인

  - ```
    $ bin/windows/kafka-topics.bat --describe --topic quickstart-events --bootstrap-server localhost:9092
    ```

  - ```
    Topic: quickstart-events        PartitionCount: 1       ReplicationFactor: 1    Configs: segment.bytes=1073741824
            Topic: quickstart-events        Partition: 0    Leader: 0       Replicas: 0     Isr: 0
    ```

  - `quickstart-events` topic에 대한 상세 정보



- 구독 시작

  - ```
    $ bin/windows/kafka-console-consumer.bat --topic quickstart-events --from-beginning --bootstrap-server localhost:9092
    ```

  - 구독을 시작한다.

  - 메시지를 수신할 수 있는 상태이다.



- 네번째 terminal 열어서 다음 명령어 실행

  - ```
    $ bin/windows/kafka-console-producer.bat --topic quickstart-events --bootstrap-server localhost:9092
    ```

  - ```
    > hello
    > kafka
    ```

  - 명령어를 입력하면 다음과 같이 메시지를 전송할 수 있다. `hello` 와 `kafka` 라는 메시지를 입력하면 구독을 시작했던 세번째 terminal에서 이 메시지가 수신된다. 즉, 통신이 됨.



- topic 삭제하기

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





- MariaDB 생성
  - Docker로 MariaDB 이미지 설치해서 volume 옵션 등을 추가하여 mariadb 생성
- HeidiSQL을 이용하여 MariaDB에 접속
  - 호스트, 사용자, 비밀번호, 포트 번호 확인해서 접속
- mydb database 생성

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
    



- confluent 설치







- jdbc 설치







- mariadb-java-client-2.7.2.jar 파일을 복사하여 confluent-6.1.0/share/java/kafka 에 붙여넣기

- terminal 에서 `$ code etc/kafka/connect-distributed.properties` 입력하여 코드 수정

- ```python
  # 맨 밑에 아래 구문 추가
  # 기존의 plugin.path 문장은 주석 처리
  plugin.path=\C:\\confluentinc-kafka-connect-jdbc-10.1.0\\lib
  ```



- Kafka Source Connect 추가 (MariaDB)

  - kafka와 DB를 연동하는 것

  - postman을 사용
  - POST 방식으로 URL은 http://localhost:8083/connectors 입력
  - Body -> raw -> Text를 JSON으로 바꾸고 코드 추가
    - echo에 대한 부분만 입력 (curl 문장은 제외)
    - password는 본인에 맞게 수정 (없으면 지우기)
  - send 클릭
  - GET 방식으로 URL은 동일하게 설정하여 send클릭하면 POST로 보낸 데이터를 받을 수 있음



- Topic 생성후 데이터를 추가하여 확인

  - Topic 생성

    - ```
      $ bin/windows/kafka-topics.bat --create --topic my_topic_users --bootstrap-server localhost:9092
      ```

    - topic 이름은 `my_topic_users`로 정했음.

  - MariaDB 데이터베이스에 데이터 추가

    - ```mariadb
      insert into users(user_id, pwd)
      values('user2', 'teset2222');
      ```

    - 

  - topic 확인



HTTP DELETE method로 http://localhost:8083/connectors/[생성한 source connect의 이름]



- sink connect 추가
- 

