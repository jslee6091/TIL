### docker-compose 기본 명령어

1. ```
   $ docker-compose --version
   ```

   - 버전 확인

2. ```
   $ docker-compose --help
   ```

   - 각종 명령어 정보

3. ```
   $ docker-compose up
   ```

   - yml파일 작성 후 docker-compose 작동

4. ```
   $ docker-compose down
   ```

   - 작동 중인 docker-compose 프로세스 종료

5. ```
   $ docker-compose ps
   ```

   - 현재 동작중인 compose 프로세스 목록
   - `docker ps -a`로 해도 되지만 compose에서는 이게 더 편함

6. ```
   $ docker-compose --file file_name.yml up
   ```

   - 특정 yml 파일을 이용하여 docker-compose 작동

7. ```
   $ docker-compose --file file_name.yml down
   ```

   - 특정 yml 파일을 이용하여 작동시킨 docker-compose 작동 중지






### yml 파일

```yaml
version: "3.9"
services:
  my-mysql:
    container_name: mysql
    image: jslee6091/mynewsql:latest
    volumes:
      # - ../db_docker/docker_volume:/var/lib/mysql
      - ./mysql-volume:/var/lib/mysql
    ports:
      - 3306:3306
    environment:
      # MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: mydb
    networks:
      - my-network
  my-django:
    image: jslee6091/mydjango:latest
    ports:
      - 8000:8000
    depends_on:
      - my-mysql
    networks:
      - my-network
networks:
  my-network:
    driver: bridge
```

- my-mysql, my-django 는 실행되는 container의 이름을 말한다.
- networks 는 container 들이 연결되어있는 network에 대한 정보를 담고 있다.

