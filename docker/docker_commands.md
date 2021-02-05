

### Docker Commands



1. ```
   $ docker container run -d -p 80:80 docker/getting-started
   ```

   - container 생성

2. ```
   $ docker version
   ```

   - 버전 확인

3. ```
   $ docker images
   ```

   - image 목록

4. ```
   $ docker images ls
   ```

   - image 목록

5. ```
   $ docker stop container_id
   ```

   - id가 container_id인 container 작동 중지

6. ```
   $ docker rm container_id
   ```

   - id가 container_id인 container 제거

7. ```
   $ docker container stop container_id
   ```

   - id가 container_id인 container 작동 중지
- 작동 중인 container를 제거하고자 할 때 먼저 수행해야 함
   
8. ```
   $ docker container ls
   ```

   - 현재 작동중인 container 출력

9. ```
   $ docker container ls -a
   ```

   - 현재 작동중인 container 뿐만 아니라 작동 중지된 container까지 출력

10. ```
    $ docker container rm container_id
    ```

    - id가 container_id인 container 제거
- 제거하고자 하는 container가 여러개일 때는 container_id를 원하는 만큼 뒤에 이어서 붙이면 됨
    -  exited된 container만 제거 가능
    
11. ```
    $ docker image rm image_id
    ```

    - id가 image_id인 image 제거
    
12. ```
    $ docker container run ubuntu:18.04
    ```

    - ubuntu:18.04 이미지를 작동시켜서 container 하나 생성 후 작동

13. ```
    $ docker container create ubuntu:18.04
    ```

    - ubuntu:18.04 이미지 컨테이너 생성

14. ```
    $ docker container run -it ubuntu:18.04 /bin/bash
    ```

    - container 만든 후 콘솔에 들어가서 작동시키는 명령어
    - exited 상태가 되지 않고 계속 동작중이다.

15. ```
    $ docker container run -t ubuntu:18.04 /bin/bash
    ```

    - container 만든 후 콘솔에 들어가서 작동이 되지만 명령어를 입력할 수 없는 상태
    - 명령창을 하나 더 띄운 후 rm 명령어로 없애야 한다.

16. ```
    $ docker container rm -f container_id
    ```

    - 작동 중인 container 강제 종료
    - 사용을 권하지는 않음

17. ```
    $ docker container run --rm -it ubuntu:18.04 /bin/bash
    ```

    - container 만들어서 콘솔 창에 입력이 가능하도록 작동시킨 후 콘솔 종료 시 container 자동 제거

18. ```
    $ docker rm container_name
    ```

    - container_name 으로 container 지우기

19. ```
    $ docker run -d -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysql mysql:5.7
    ```

    - `-d`: background 설정
    - `-p`: port forwarding
    - `3306(앞부분)`: host port
    - `3306(뒷부분)`: container port
    - `-e`: env
    - `mysql:5.7`: 이미지:Tag
    - `MYSQL_ALLOW_EMPTY_PASSWORD`: mysql에 접속 시 password 입력을 안해도 됨

    

20. ```
    $ docker container inspect mysql
    ```

    - 이름이 mysql인 container의 상세정보를 보여줌
    - docker 사용시 중요한 정보가 많다.

21. ```
    $ docker run -d -p 33306:3306 -e MYSQL_RANDOM_ROOT_PASSWORD=true --name mysql_client_rand mysql:5.7
    ```

    - `MYSQL_RANDOM_ROOT_PASSWORD`: mysql 접속 시 random 하게 생성된 password를 입력해야 함

    - password 확인하는 법 - 1

      > `-d`옵션을 제거한 경우

      - ```
        $ docker run -p 33306:3306 -e MYSQL_RANDOM_ROOT_PASSWORD=true --name mysql_client_rand mysql:5.7
        ```

      - `-d` 옵션을 제거한 채로 container 생성하면 container 생성과정이 모두 나오는데 여기에서 중간의 `GENERATED ROOT PASSWORD` 에 password 정보가 있다.

      - 이것을 복사해서 mysql 접속 시 입력하면 됨

    - password 확인하는 법 - 2

      > `-d`옵션을 넣은 경우

      - `-d`옵션을 그대로 입력하여 container 생성한 후 docker log를 확인하면 됨

      - ```
        $ docker logs container_id
        ```

      - log를 통해 `-d`옵션을 제거했을 때 보이는 정보들을 확인할 수 있다.

      - 마찬가지로 중간의 `GENERATED ROOT PASSWORD` 를 확인하면 된다.





### mysql

```
$ mysql -h127.0.0.1 -uroot -p
```

- mysql 접속



```
show databases;
```

- DB 목록보기



```
create database mydb;
```

- mydb 이름의 DB 만들기



```
use mydb;
```

- mydb 선택



```
show tables;
```

- 테이블 목록 보기



```
create table member(id varchar(20), name varchar(20));
```

- 테이블 생성



```
insert into member(id,name) values('data1','data2')
```

- 테이블 추가



```
select * from member
```

- member table의 정보를 모두 선택



- Port Error Solution

- ```
  윈도우 검색에 서비스 앱 켜서 MySQL 을 찾아 선택 -> 우클릭 속성 -> 시작 유형(E): (자동 -> 사용안함) -> 서비스 상태 중지
  ```



mysql_client

ef5212fa0e - networkid

172.17.0.1 - gateway

172.17.0.3 - ipaddress



mysql

ef5212fa0e - networkid

172.17.0.1 - gateway

172.17.0.2 - ipaddress



-> gateway 주소와 networkid 주소는 같음을 알 수 있다.



### mysql 으로 동작시킨 서버에 mysql_client 가 접속하기



```
$ docker exec -it mysql /bin/bash
$ mysql -h127.0.0.1 -uroot -p
```

- mysql container를 동작시켜 서버를 생성한다.
- mysql 의 database 를 만들기 위해서는 로컬 주소로 mysql 에 접속하면 된다.

```
$ docker exec -it mysql_client /bin/bash
$ mysql -h172.17.0.2 -uroot -p
```

- mysql_client container를 동작시켜 mysql 서버에 접속한다.
- 이때 mysql 의 주소는 mysql container의 ipaddress를 입력해야 한다.
- 즉, mysql container의 ip 주소로 접근하는 것이다. 
- 그러면 mysql 서버에서 만들었던 database를 확인할 수 있다.