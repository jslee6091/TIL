### Linux Version 확인 명령어

- `uname` 활용

- ```
  $ uname
  Linux
  ```

  - 커널 이름 출력

- ```
  $ uname -a
  Linux 81bd63f964e1 5.4.72-microsoft-standard-WSL2 #1 SMP Wed Oct 28 23:40:43 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
  ```

  - 시스템의 모든 정보를 출력

- ```
  $ uname -s
  Linux
  ```

  - 커널 이름 출력
  - `$ uname`와 같음

- ```
  $ uname -n
  81bd63f964e1
  ```

  - 네트워크의 호스트이름

- ```
  $ uname -r
  5.4.72-microsoft-standard-WSL2
  ```

  - kernel의 release 정보

- ```
  $ uname -v
  #1 SMP Wed Oct 28 23:40:43 UTC 2020
  ```

  - kernel의 version 출력

- ```
  $ uname -m
  x86_64
  ```

  - 시스템의 하드웨어 타입(하드웨어 아키텍쳐)

- ```
  $ uname -p
  x86_64
  ```

  - 프로세서의 종류

- ```
  $ uname -o
  GNU/Linux
  ```

  - 운영체제 이름

- ```
  $ uname -i
  x86_64
  ```

  - `$ uname -p`와 같음

