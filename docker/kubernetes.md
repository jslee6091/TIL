### kubernetes 동작 환경 구성

1. vagrant을 이용하여 가상환경 실행

   - ```
     $ vagrant on
     ```

   - ```
     $ vagrant status
     ```

     - 이 명령어로 동작 상태 확인

2. Xshell에 각각의 가상환경 정보 등록하여 운영체제에 접속

   - PW : vagrant

3. `su -` 명령어로 root 계정 접속



### 각종 명령어들

1. ```
   $ kubetcl get pods
   ```

   - default namespace에 대한 pod 정보 확인

2. ```
   $ kubetcl get pods --all-namespaces
   ```

   - default namespace이외의 모든 namespace 목록 확인

3. ```
   $ kubetcl get pods --namespace kube-system
   ```

   - 이름이 kube-system 인 namespace 목록 출력

4. ```
   $ $ kubetcl get pods -n kube-system
   ```

   - 3번과 기능은 똑같고 `-n`옵션으로 줄여서 표현 가능

5. ```
   $ kubectl get pods -o wide
   ```

   - namespace에 대한 더 많은 정보를 얻을 수 있음(ID, NODE, NOMINATED etc..)

6. ```
   $ kubectl get services
   ```

   - namespace의 IP, PORT 정보 확인

7. ```
   $ kubectl get svc
   ```

   - 6번과 기능은 같고 svc로 줄여서 사용 가능

8. ```
   $ kubectl edit service nginx-test
   ```

   - nginx-test의 정보 수정하기(Vi Editor)

9. ```
   $ curl -X GET http://127.0.0.1:30409
   ```

   - 할당된 포트번호로 접속하여 HTML 코드를 확인할 수 있다.
   - 이를 windows에서 browser로 확인하기 위해서는 port 설정을 추가적으로 해야한다.

10. ```
    $ netstat -ntpl
    ```

    - Internet connections 확인

    - ```
      $ yum install net-tools
      ```

      - 없을 시 위 command로 설치

11. ```
    $ kubectl get nodes
    ```

    - master에 접속한 node 들의 목록 확인
    - node 들이 master에 연결되어있기 때문에 master에서 사용해야한다.

12. 

