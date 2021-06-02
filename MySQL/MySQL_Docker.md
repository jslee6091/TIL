### Mysql Docker Image 활용하여 컨테이너 실행



1. 비밀번호가 없는 Mysql Docker 컨테이너 생성

   - ```
     $ docker run -d -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysql mysql:5.7
     ```

   - `-d`: background 설정. 없으면 컨테이너가 생성될 때의 log가 모두 명령창에 보여진다.

   - `-p`: port forwarding
   - `3306(앞부분)`: host port
   - `3306(뒷부분)`: container port
   - `-e`: env
   - `mysql:5.7`: 이미지:Tag
   - `MYSQL_ALLOW_EMPTY_PASSWORD`: mysql에 접속 시 password 없음



2. 비밀번호가 있는 Mysql Docker 컨테이너 생성

   - 비밀번호를 먼저 설정하기

     - ```
       $ docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=mydb --name mysql mysql:5.7
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



