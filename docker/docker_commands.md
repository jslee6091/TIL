

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
   $ docker pull ubuntu:18.04
   ```

   - ubuntu 18.04 image download

4. ```
   $ docker images
   ```

   - image 목록

5. ```
   $ docker image ls
   ```

   - image 목록

6. ```
   $ docker stop container_id
   ```

   - id가 container_id인 container 작동 중지

7. ```
   $ docker rm container_id
   ```

   - id가 container_id인 container 제거

8. ```
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
    - exited된 container만 제거 가능
    
11. ```
    $ docker image rmi image_id
    ```

    - id가 image_id인 image 제거
    
13. ```
    $ docker image rm -f image_id
    ```

    - ID가 image_id 인 이미지를 실행중이어도 강제로 삭제

14. ```
    $ docker container run ubuntu:18.04
    ```

    - ubuntu:18.04 이미지를 작동시켜서 container 하나 생성 후 작동

15. ```
    $ docker container create ubuntu:18.04
    ```

    - ubuntu:18.04 이미지 컨테이너 생성

16. ```
    $ docker container run -it ubuntu:18.04 /bin/bash
    ```

    - container 만든 후 콘솔에 들어가서 작동시키는 명령어
    - exited 상태가 되지 않고 계속 동작중이다.

17. ```
    $ docker container run -t ubuntu:18.04 /bin/bash
    ```

    - container 만든 후 콘솔에 들어가서 작동이 되지만 명령어를 입력할 수 없는 상태
    - 명령창을 하나 더 띄운 후 rm 명령어로 없애야 한다.

18. ```
    $ docker container rm -f container_id
    ```

    - 작동 중인 container 강제 종료
    - 사용을 권하지는 않음

19. ```
    $ docker container run --rm -it ubuntu:18.04 /bin/bash
    ```

    - container 만들어서 콘솔 창에 입력이 가능하도록 작동시킨 후 콘솔 종료 시 container 자동 제거

20. ```
    $ docker rm container_name
    ```

    - container_name 으로 container 지우기

25. ```
    $ docker container run --volume C:\Users\jslee\Desktop\docker_volume:/var/lib/mysql -d -p 13306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysql mysql:5.7
    ```

    - docker container volume 생성
    - 로컬의 데이터와 컨테이너가 실시간으로 연동할 수 있다.
    - 특정 디렉토리 내에서 생성하였다.

26. ```
    $ docker volume ls
    ```

    - docker volume list 보기

27. ```
    $ docker volume rm volume_id
    ```

    - 특정 volume 제거

28. prune commands

    - ```
      $ docker container prune
      ```

      - 중지된 모든 container 삭제

    - ```
      $ docker image prune
      ```

      - 이름 없는 모든 image 삭제

    - ```
      $ docker network prune
      ```

      - 사용되지 않는 network 삭제

    - ```
      $ docker volume prune
      ```

      - container에서 사용되지 않는 volume 삭제

    - ```
      $ docker system prune
      ```

      - 중지된 모든 container, image, network, volume 들을 모두 삭제

29. ```
    $ docker ps
    ```

    - 현재 실행중인 프로세스들을 모두 보여줌
    - `-a`옵션을 추가하면 중지된 프로세스까지 보여줌
    
30. ```
    $ docker run -d -p 23306:3306 --network project_network --name mysql2 -e MYSQL_ALLOW_EMPTY_PASSWORD=true -e LC_ALL=C.UTF-8 mysql:5.7
    ```

    - 한글 입력이 가능하고 깨짐을 방지하는 docker mysql run 명령어
    - LC_ALL 을 C.UTF-8로 설정하면 된다.
    - mysql에 접속해서 `$ locale` 명령어를 통해 C.UTF-8이 있는지 확인해야한다.



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





### Dockerfile 생성 후 image build

- ```
  $ docker image pull ubuntu
  ```

  - 위 명령어로 ubuntu latest 버전의 image download

- ```
  $ docker image build -t fromtest:1.0 .
  ```
  
- repository 이름이 fromtest 이고 TAG가1.0인 이미지를 build함
  
  - build 하기 전에 Dockerfile을 생성해야 한다.
  
  - 만든 Dockerfile로 이미지 빌드하는 방법
  
  - ```
    $ docker build -t fromtest -f Dockerfile .
    ```
  
- ```
  $ docker run -it fromtest:1.0
  ```

  - fromtest 이미지를 실행
  
- ```
  $ docker run -it --name frontname fromtest:1.0
  ```

  - 이미지 실행하는 프로세스의 이름을 부여할 수 있음

- ```
  $ docker run -it nodejstest:1.0 /bin/sh
  ```

  - nodejstest 이미지 실행 후 `docker exec -it container_ID /bin/sh` 명령어를 실행하는 것을 한번에 해줌
  - /bin/bash로 해도 되는데 거의 대부분의 리눅스 버전에서 sh가 많이 있으므로 이것을 사용한다.
  
  - 왜 갑자기 sh를 사용하는지 자세히는 모름
- ```
  $ docker run -p 8080:8080 -d nodejstest:1.0
  ```

  - 이미지 실행 시 인터넷 포트와 연결할때 따로 포트번호르 지정하는 명령어 



### Docker 계정의 내 repository 생성 후 이미지 업로드 하기



- ```
  $ docker tag nodejstest:1.0 jslee6091/nodejstest:1.0
  ```

  - tag 와 repository 이름을 docker 사이트의 내 계정과 연결하기 위한 목적으로 지정하는 명령어

- ```
  $ docker login
  ```

  - docker 로그인 명령어 - 비밀번호 같은 정보 입력 없이 자동으로 이루어진다.

- ```
  $ docker image push jslee6091/nodejstest:1.0
  ```

  - docker 계정의 repository에 이미지를 push

- ```
  $ docker image pull jslee6091/nodejstest:1.0
  ```

  - docker 계정의 repository에 있는 이미지를 로컬로 pull






### Ubuntu 관련 명령어

- process 관련

```
$ ps -aux
```

```
$ ps -aex
```

```
$ ps -aef
```

```
$ ping 127.0.0.1
```

- ping package 설치

  - ```
    $ sudo apt-get install iputils-ping
    ```






- shell 파일 실행 관련

  ```
  /mydata/test.sh
  ```

  - mydata 디렉터리 내의 test.sh 파일 실행 명령어
  - mydata 디렉터리에들어가서 test.sh 실행은 안됨



### Dockerfile로 파이썬 실행

- 임의의 python 파일 생성

  - ex) test.py

- Dockerfile 생성 - 파이썬 이미지 다운로드 및 명령어 실행

- build과 run 실행

- test.py 실행

  - ```
    python test.py
    ```

- 이미지 파일 내에서 numpy 다운 받기
  
  - 해당 container에 접속하여 `pip install numpy`를 실행하면 된다.



### Dockerfile에 volume mount 하여 로컬과 연동

- 로컬의 파일을 docker container에도 설치하고 실시간으로 연동하는 과정

- Dockerfile에서 test.py를 volume mount 하기 위한 코드 작성

- ```
  $ docker run -v C:\Users\jslee\Desktop\docker_file:/mydata -e EXEC_FILE=test.py pythonnew
  ```

  - container에서 test.py를 실행하는 명령어

- ```
  $ docker run -v C:\Users\jslee\Desktop\docker_file:/mydata -it pythonnew /bin/bash
  ```

  - container에 접속하는 명령어

- container에 접속하여 test.py를 실행할 수 있다.

  - ```
    $ python test.py
    ```

    

- 로컬에서 test.py를 수정하거나 새로운 파일을 만들면 run 하지 않고 바로 container에서 변경 사항이 반영된다.



### Docker Network

- ```
  $ docker network ls
  ```

  - docker에 설치되어있는 네트워크 리스트

- ```
  $ docker network create network_name
  ```

  - 새로운 네트워크 만들기

- ```
  $ docker network connect network_name process_name
  ```

  - network에 process를 연결한다. (process = container)

- inspect 명령어로 네트워크 ip 정보들을 확인하여 process 와 연결할 수 있다.

- ```
  $ docker network disconnect network_name process_name
  ```

  - process와 network의 연결 끊기

- mysql 이미지를 run 할때 네트워크와 연결시키기

  - ```
    $ docker run -d -p 13306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysql_client --network my-network mysql:5.7
    ```

  - `--network network_name` 옵션을 추가해야한다.

  - 이때 직접 만든 network에 연결하고 그 이후 network를 삭제하면 어느 곳도 연결된 곳이 없는 상태가 된다.

  - 이를 bridge에 연결하면 된다.

  - ```
    $ docker network connect bridge process_name
    ```

- ```
  $ docker network rm network_name
  ```

  - docker network 삭제