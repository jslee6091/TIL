### Mysql Docker Image 활용하여 컨테이너 실행



1. 비밀번호가 없는 Mysql Docker 컨테이너 생성

   - ```
     $ docker run -d -p 13306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysql mysql:5.7
     ```

   - `-d`: background 설정. 없으면 컨테이너가 생성될 때의 log가 모두 명령창에 보여진다.

   - `-p`: port forwarding 옵션
   - `13306:3306` : 로컬 또는 host port 번호 13306과 MySQL 컨테이너 port 3306번이 서로 연결되어있다. 즉, MySQL 컨테이너에서 3306번호에서 작동중인 데이터베이스로 로컬에서 연결하려면 13306번 포트를 사용해야한다.
   - `-e`: 환경변수 옵션
   - `mysql:5.7`: 이미지:Tag
   - `MYSQL_ALLOW_EMPTY_PASSWORD`: mysql에 접속 시 password 없음



2. 비밀번호가 있는 Mysql Docker 컨테이너 생성

   - 비밀번호를 먼저 설정하기

     - ```
       $ docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret --name mysql mysql:5.7
       ```

     - mysql 접속 시 password가 `secret`이 됨

   - 비밀번호를 임의로 생성하기

     - ```
       $ docker run -d -p 33306:3306 -e MYSQL_RANDOM_ROOT_PASSWORD=true --name mysql_client_rand mysql:5.7
       ```

     - `MYSQL_RANDOM_ROOT_PASSWORD`를 `true`로 설정하면 임의의 password가 생성된다.

   - 임의로 생성된 비밀번호를 확인하는 방법

     - ```
       $ docker logs mysql_container
       ```

     - 생성된 mysql_container의 log를 확인한다.

     - 중간의 `GENERATED ROOT PASSWORD` 에서 비밀번호를 확인할 수 있다.



3. Mysql volume mount 생성

   - ```
     $ docker container run --volume C:\Users\jslee\Desktop\docker_volume:/var/lib/mysql -d -p 13306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysql mysql:5.7
     ```

   - 로컬의 `C:\Users\jslee\Desktop\docker_volume` 디렉터리와 Mysql container의 `/var/lib/mysql` 디렉터리를 서로 연결

   - 로컬의 데이터와 컨테이너가 실시간으로 연동할 수 있다.



4. 특정 데이터베이스를 생성하는 옵션 붙이기

   - ```
     $ docker run -d -p 13306:3306 -e MYSQL_DATABASE=mydb -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql:5.7
     ```

   - Mysql 컨테이너 생성 시 `mydb` 데이터베이스가 이미 생성되어있음



5. MySQL 컨테이너를 특정 네트워크에 연결하여 생성

   - ```
     $ docker run -d -p 13306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysql_client --network my-network mysql:5.7
     ```

   - `my-network` 라는 도커 네트워크에 mysql 컨테이너를 포함시켜 생성

   - 이 네트워크와 연결된 다른 컨테이너와 연결하여 데이터가 전송되게 할 수 있다.



6. MySQL에 한글 입력이 가능하고 깨짐을 방지하기 위한 옵션

   - `LC_ALL` 옵션을 설정한다.

   - ```
     $ docker run -d -p 23306:3306 --network project_network --name mysql2 -e MYSQL_ALLOW_EMPTY_PASSWORD=true -e LC_ALL=C.UTF-8 mysql:5.7
     ```

   - `LC_ALL` 옵션을 `C.UTF-8`로 설정해놓으면 한글이 깨짐없이 MySQL 컨테이너에 저장된다.

   - 생성된 MySQL 컨테이너에서 `$ locale` 명령어를 입력하면 C.UTF-8로 설정되어 있다.



7. 생성된 MySQL 컨테이너에 접속하기

   - ```
     $ docker exec -it mysql_name /bin/bash
     ```

   - 이름이 `mysql_name`인 MySQL 컨테이너에 접속하는 명령어



### 서로 다른 mysql 컨테이너에 접속하기

> 두 mysql 컨테이너가 실행중이고 같은 도커 네트워크에 연결되어야한다.

- mysql1 의 도커 네트워크 주소 : 172.17.0.1
- mysql2의 도커 네트워크 주소 : 172.17.0.2



1. 자신의 mysql 데이터베이스에 접속하기

   - ```
     $ docker exec -it mysql1 /bin/bash
     $ mysql -h127.0.0.1 -uroot -p
     ```

   - mysql container에 접속 후 mysql1 자신의 mysql 데이터베이스에 접속한다.

   - 자신의 DB에 접속할 때는 로컬 호스트를 입력한다. (생략도 가능)

   - mysql 데이터베이스, 테이블 등 DB를 생성하고 조작할 수 있다.



2. 서로 다른 mysql 데이터베이스에 접속하기

   - mysql1 컨테이너에서 mysql2 데이터베이스 접속하기

   - ```
     $ docker exec -it mysql1 /bin/bash
     $ mysql -h127.0.0.2 -uroot -p
     ```

   - mysql2의 도커 네트워크 주소인 172.17.0.2 를 입력하여 접속

   - mysql2의 DB를 조회할 수 있다.

   - mysql1에서 mysql2 DB로 접속할 때도 주소만 바꿔서 접속하면 가능하다.



3. 두 명령어 한번에 실행

   - ```
     $ docker container exec -it mysql /bin/bash -c mysql -h127.0.0.1 -uroot -p
     ```

   - `-c` 옵션을 추가해야함



### MySQL Dockerfile 만들기

```dockerfile
# docker run -d -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true -e MYSQL_DATABASE=mydb mysql:5.7
FROM mysql:5.7

ENV MYSQL_ALLOW_EMPTY_PASSWORD true
ENV MYSQL_DATABASE mydb

COPY docker_volume /var/lib/mysql
EXPOSE 3306

CMD ["mysqld"]
```

