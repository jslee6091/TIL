# 리눅스 명령어

> 리눅스에서 사용하는 기본 명령어 정리 
>
> 윈도우 - > git bash 프로그램 사용



### pwd 

* `print working directory`의 약자
* 현재 나의 디렉터리 위치를 출력



### cd

- `change directory`의 약자
- 폴더 이동을 위해 사용하는 명령어



### ls

- list의 약자

- 현재 폴더에 있는 파일, 문서 출력

- -a 옵션

  - hidden file인 .파일들까지 모두 보여줌

- -l 옵션

  - 디렉터리의 자세한 정보를 보여줌

  - ```
    ex) drwxr-xr-x 2 cloud_user cloud_user 4096 Feb 22  2019 Desktop
    d : 디렉터리
    rwxr-xr-x : 권한
    2 : 링크 개수
    cloud_user(첫번째): 소유자
    cloud_user(두번째): 소유자의 그룹
    4096 : 사이즈
    Feb 22 2019 : 생성시간
    ```
    
  - 권한 정보
  
  - ```
    첫 3자리 : 소유자
    가운데 3자리 : 소유자 그룹
    마지막 3자리 : 기타 그룹
    ```
  
- -al 옵션

  - 숨김 파일 또는 디렉터리 까지 보여줌

- -lh 옵션

  - 파일의 용량을 K, M, G 단위로 알기쉽게 표시



### which

> which <command>

- command가 설치된 디렉터리의 경로를 찾아줌

- ```
  ex) $ which rmdir
  /bin/rmdir
  ```



### whereis

> whereis <command>

- command가 설치된 경로를 `which`보다 더 자세히 알려줌

  - 실행 파일, 소스 파일, man 페이지 파일 위치 까지

- ```
  ex) whereis rmdir
  rmdir: /bin/rmdir /usr/share/man/man2/rmdir.2.gz /usr/share/man/man1/rmdir.1.gz
  ```

- 옵션

  - -b : 실행 파일(바이너리 파일)만 출력
  - -m : 매뉴얼 파일만 출력
  - -s : 소스 파일만 출력



### 리눅스 시스템

- `.` : 현재 폴더
- `..` : 상위 폴더
- 앞에 `.`이 있는 폴더 또는 파일: 숨겨진 것



### 디렉토리 삭제

- 비어있는 디렉토리 삭제

  - ```
    $ rmdir directory_name
    ```

- 디렉토리 내의 모든 파일, 하위 디렉토리 삭제

  - ```
    $ rm -rf directory_name
    ```

  - ```
    $ rm -r directory_name
    ```

  - -r 과 -rf의 차이는 크게 없는 것 같다.





### cat

- ```
  cat file_name.file
  ```

- 원하는 파일의 내용을 terminal 창에 그대로 보여줌

- 파일을 열 필요 없음

- ```
  cat file_name | grep search_word
  ```

- file_name 내의 searc_word라는 단어를 검색해서 보여줌

- ```
  $ cat /etc/group | grep cloud_user
  ```

- 유저가 속한 그룹에서 cloud_user를 검색함

- ```
  $ cat /etc/issue
  ```

- 현재 사용하고 있는 리눅스 베포판의 이름과 버전을 보여줌



### 파일/디렉토리 이동

- 파일을 원하는 디렉토리에 이동

  - ```
    $ mv file_name dir_name/
    ```

- 디렉토리를 원하는 디렉토리에 이동

  - ```
    $ mv dir_name/ dir_name/
    ```



### groups

- ```
  $ groups
  ```

- 유저가 속한 그룹의 리스트를 보여줌



### history

- ```
  $ history
  ```

- 지금까지 입력했던 명령어 기록을 보여줌

- ```
  $ history | grep search_word
  ```

- 명령어 기록중 search_word을 입력했던 기록만 보여줌



### 메모리 정보

- ```
  $ free -h
  ```

- 현재 사용 가능한 메모리와 사용중인 메모리 등 메모리 사용 정보를 확인할 수 있다.



### tar.gz , tgz , gz , bz2 파일 압축 해제

- tar.gz 확장자 압축 해제

  - ```
    $ tar xvzf 파일명.tar.gz
    ```

- tgz 확장자 압축 해제

  - ```
    $ tar xvzf 파일명.tgz
    ```

- gz 확장자 압축 해제

  - ```
    $ gzip -d 파일명.gz
    ```

- bz2 확장자 압축 해제

  - ```
    $ bzip2 -kd 파일명.bz2
    ```



### 파일 이름 바꾸기 & 이동

- ```
  $ mv file new_file
  ```

  - `file` 이름을 `new_file` 이름으로 바꾸기
  
- ```
  $ mv file /directory
  ```

  - `file`을 원하는 디렉터리 내부로 이동
  - 한번에 여러 파일 가능



### 파일 복사

- ```
  $ cp file1 file2
  ```

  - `file1`을 복사해서 `file2`로 만든다.
  - 원하는 파일 위치를 잘 설정해야 함
