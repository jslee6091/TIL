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
    또는
$ kubectl get no
    ```
    
- master에 접속한 node 들의 목록 확인
    - node 들이 master에 연결되어있기 때문에 master에서 사용해야한다.
    
12. ```
    $ kubectl describe pod pod_name
    ```

    - pod_name 의 더 자세한 정보 확인
    
13. ```
    $ kubectl explain pods
    ```

    - pods에 대한 설명
    
14. ```
    $ kubectl api-resources
    ```

    - kubernetes에서 사용 가능한 api resource 들을 확인한다.



### node 실행 후 STATUS = Ready 상태로 만들기

> master에서 get node 명령어로 확인

1. ```
   $ systemctl status kubelet
   ```

   - 우선 kubelet이 활성화 되어있는지 확인한다.

2. ```
   $ systemctl start kubelet
   ```

   - 비활성화 되어있다면 활성화시킨다. 

3. ```
   $ kubectl get node
   ```

   - master에서 이 명령어를 실행하여 node 의 STATUS 가 Ready 상태로 된 것을 확인한다.




### yaml 파일 다운받기



```
$ kubectl get services -o yaml > nginx-service.yml
```

- nginx-service.yml 파일을 다운받음





### yml파일을 이용한  pod 생성

1. 리눅스에 nodejs 설치

   ```
   $ yum install epel-release
   $ yum install -y gcc-c++ make
   $ curl -sL https://rpm.nodesource.com/setup_12.x | sudo -E bash -
   $ yum install nodejs
   ```

   

2. hello.js 작성 후 실행

   ```
   $ node hello.js
   ```

3. Dockerfile 작성

4. 도커 이미지 빌드

   ```
   $ docker build -t jslee6091/hello .
   ```

5. 도커 이미지 실행

   ```
   $ docker run -d -p 8001:8000 jslee6091/hello
   ```

6. 도커 허브에 올리기

   ```
   $ docker push jslee6091/hello
   ```

7. yml 작성

   ```
   $ vi my_hello_pod.yml
   ```

8. pod 생성

   ```
   $ kubectl create -y my_hello_pod.yml 
   또는
   $ kubectl apply -f my_hello_pod.yml
   ```

   - yml에 작성된 내용에 맞게 쿠버네티스 객체를 생성한다.

9. 생성된 container에 들어가서 curl을 통한 확인

   ```
   $ kubectl exec -it hello-pod /bin/bash
   # hello-pod는 pod 이름
   ```

10. container에서 curl 실행

    ```
    $ apt-get update 
    $ apt-get install -y curl
    ```

11. 생성된 파일 지우기 (필요시 사용)

    ```
    $ kubectl delete pod hello-pod
    ```

    

### yml파일을 이용한  서비스 생성

1. yml 파일 생성

2. apply

   ```
   $ kubectl apply -f my_hello_pod.yml
   ```

3. port 확인

   ```
   $ docker get svc -o wide
   ```

4. curl로 확인

   ```
   $ curl -X GET http://127.0.0.1:8001
   $ curl -X GET http://127.0.0.1:31775
   ```

   - 31775는 바뀔 수 있음





```
$ kubectl annotate deployment/echo kubernetes.io/change-cause="not exists environment variables"
```

- ???



```
$ kubectl get pods -o=custom-columns='NameSpec:.metadata.namespace, Name:.metadata.name, Containers:.spec.containers[*].name'
```

- ???