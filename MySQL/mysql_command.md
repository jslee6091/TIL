### MySQL 기본 명령어

#### Database

1. 생성

   - ```
     $ create database mydb;
     ```

   - mydb 데이터베이스 생성

2. 삭제

   - ```
     $ drop database mydb;
     ```

   - mydb 데이터베이스 삭제

3. 목록 조회

   - ```
     $ show databases;
     ```

   - 현재 생성된 데이터베이스 목록 조회

4. 선택

   - ```
     $ use mydb;
     ```

   - mydb 데이터베이스 선택

   - 데이터베이스 내의 테이블 조작이 가능



#### Table

1. 생성

   - ```
     $ create table member(id varchar(20), name varchar(20));
     ```

   - varchar(20) 타입의 id와 name을 column으로 가지는 member 테이블 생성

2. 목록 조회

   - ```
     $ show tables;
     ```

   - 현재 생성된 테이블 목록 조회

3. 데이터 조회

   - ```
     $ select * from member;
     ```

   - member 테이블 내의 모든 데이터 조회

   - ```
     $ select id from member;
     ```

   - member 테이블 내의 id column의 모든 데이터 조회

4. 데이터 삽입

   - ```
     $ insert into member(id, name) values('data1', 'data2');
     ```

   - member 테이블에 데이터 삽입

   - 데이터 타입을 맞춰야 함

5. 세부 정보 조회

   - ```
     $ desc member;
     ```

   - member 테이블의 상세 정보 조회

   - column의 종류와 크기, Primary Key, NOT NULL 속성 등 상세 정보를 알 수 있다.

6. 테이블 삭제

   - ```
     $ drop table member;
     ```

   - member 테이블 전체 삭제

7. Column 정보 변경

   - ```
     $ alter table member change name myname varchar(20);
     ```

   - member 테이블의 name 칼럼을 varchar(20) 타입의 myname 이름으로 변경



#### 조건문

- WHERE 사용

  - ```
    $ select id from member where name = data;
    ```

  - member 테이블의 id 칼럼의 데이터 중 name 의 값이 data인 데이터를 조회.



### Port Error Solution

1. 윈도우 검색에 서비스 앱 켜서 MySQL 을 찾아 선택
2. 우클릭 속성
3. 시작 유형(E): (자동 -> 사용안함)
4. 서비스 상태 중지