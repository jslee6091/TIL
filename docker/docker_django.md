### Django Project를 Docker Container에 올리기



1. Django Project 생성

   - 기존의 Django Project 활용

2. Dockerfile 작성

   - django와 mysql 사용을 위해서는 패키지 설치가 필요하다.

   - ```
     $ pip install django
     $ pip install mysqlclient
     ```

   - 이를 Dockerfile에서 작성한다.

   - ```
     RUN pip install django
     RUN pip install mysqlclient
     ```

     

3. Docker image build 

   - ```
     $ docker build --no-cache=true -t mydjango .
     
     # 최초 생성 시
     $ docker build -t mydjango .
     ```

4. Docker run

   - ```
     $ docker run -v C:\Users\jslee\Desktop\docker_django\django_docker_comb:/mydjango -it -P mydjango
     ```

   - `-P` 옵션을 통해 Port 번호를 지정하는 것이 아닌 Random 하게 부여한다.

5. 웹 브라우저에서 확인

   - `docker ps -a` 명령어를 입력하여 현재 실행되는 프로세스의 포트를 확인한다.
   - 브라우저에서 `127.0.0.1:port` 주소를 입력하여 접속

6. 전체 Dockerfile 코드

   - ```dockerfile
     FROM python:3.7.9-stretch
     
     WORKDIR /mydjango
     
     RUN pip install django
     RUN pip install mysqlclient
     
     EXPOSE 8000
     
     CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
     ```

   - 



- /bin/bash 에 직접 들어가서 설치하는 경우

  1. Dockerfile 코드 수정

  ```dockerfile
  FROM python:3.7.9-stretch
  
  WORKDIR /mydjango
  
  EXPOSE 8000
  
  CMD ["python", "--version"]
  ```

  - django, mysqlclient 패키지 설치를 하지 않는다.

  

  2. Docker image build

  - ```
    $ docker build --no-cache=true -t mydjango .
    
    # 최초 생성 시
    $ docker build -t mydjango .
    ```

  3. Docker run

     - ```
       $ docker run -v C:\Users\jslee\Desktop\docker_django\django_docker_comb:/mydjango -it -P mydjango /bin/bash
       ```

     - 뒤에 /bin/bash 를 붙여야 이곳에 접속이 가능하다.

  4. django, mysqlclient 패키지 설치

     - ```
       pip install django
       pip install mysqlclient
       ```

  5. 서버 구동

     - ```
       python manage.py runserver 0.0.0.0:8000
       ```

  6. 브라우저에서 확인

     - Port 번호를 꼭 확인한다.

  

- Dockerfile에서 직접 설치와 실행을 하도록 하는 것이 편리하다. 왜냐하면 2번째 방법은 매번 이미지를 build 할 때마다 수작업으로 설치를 진행하는 번거로움이 있기 때문이다.





### Django & MySQL

- ```
  $ docker network create network_name
  ```

- ```
  $ docker build -t mydjango .
  ```

- ```
  $ docker run -d -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true -e MYSQL_DATABASE=mydb --network djangomysql mysql:5.7
  ```

- ```
  $ docker run -d -p 8000:8000 --network djangomysql -it mydjango:latest
  ```

- ```
  $ docker exec -it mysql /bin/bash
  ```

- 

