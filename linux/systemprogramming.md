### Shared Memory

- ```
  $ ipcs -m
  ```

  - 현재 사용중인 공유 메모리 정보 출력





### Process

- ```
  $ ps -el
  ```

  - 현재 실행중인 프로세스 정보 출력





### File descriptor

- ```
  $ sudo ls -trn /proc/[pid]/fd
  ```

  - `[pid]`의 file descriptor 정보 출력

