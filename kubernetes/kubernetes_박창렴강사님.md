### kubernetes cluster



#### 이론



- 마스터 노드(master node)
  - 전체 쿠버네티스 시스템을 제어하고 관리하는 ***<u>쿠버네티스 컨트롤 플레인(control plane)</u>***을 실행
    - 쿠버네티스 API 서버
    - 스케줄러(scheduler)
    - 컨트롤러 매니저(controller manager)
    - etcd



- 워커 노드
  - 실제 배포되는 컨테이너 애플리케이션을 실행
    - 컨테이너 런타임
    - kubelet
    - kube-proxy



- 포드(pod)
  - 컨테이너 애플리케이션의 기본 단위
  - 1개 이상의 컨테이너로 구성된 컨테이너 집합
  - 여러 개의 컨테이너를 추상화해서 하나의 애플리케이션으로 동작하도록 만드는 컨테이너 묶음



#### 실습

> vagrant을 이용하여 master, node1, node2 를 작동시키고 실습 진행

- nginx 컨테이너로 구성된 포드를 생성

  - nginx-pod.yml 작성 (manifest file)

  - ```yaml
    apiVersion: v1 # YAML 파일에서 정의한 오브젝트의 API 버전
    kind: Pod # 리소스의 종류 (kubectl api-resources 명령의 KIND 항목)
    metadata: # 리소스의 부가 정보 (이름, 네임스페이스, 라벨, 주석)
      name: my-nginx-pod
      labels:
        name: myapp
    spec: # 리소스 생성을 위한 정보
      containers:
      - name: my-nginx-pod
        image: nginx:latest
        ports:
          - containerPort: 80
            protocol: TCP
    ```



- master 노드에 nginx-pod.yaml 파일(매니페스트 파일)을 생성 후 새로운 포드를 생성

  - ```
    $ kubectl apply -f nginx-pod.yml
    ```

  - ```
    pod/my-nginx-pod created
    ```

- 생성된 포드 확인

  - ```
    $ kubectl get pods
    ```

  - ```
    NAME           READY   STATUS    RESTARTS   AGE
    my-nginx-pod   1/1     Running   0          9s
    ```



- 생성된 리소스의 상세 정보를 확인

  - ```
    $ kubectl describe pods my-nginx-pod
    ```

  - ```
    $ kubectl get pods -o wide
    ```

  - ```
    NAME           READY   STATUS    RESTARTS   AGE     IP                NODE    NOMINATED NODE   READINESS GATES
    my-nginx-pod   1/1     Running   0          10m     192.168.166.143   node1   <none>           <none>
    ```

  - ip 주소 : 192.168.166.143



- 클러스터 내부에 테스트용 포드를 임시로 생성해서 nginx 동작을 확인

  - ```
    $ kubectl run -it --rm debugpod --image=alicek106/ubuntu:curl --restart=Never bash
    ```

  - ```
    If you don't see a command prompt, try pressing enter.
    ```

  - 명령어를 입력하면 debugpod의 root 계정으로 접속함

  - ```
    $ curl 192.168.166.143
    ```

  - ```
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>
    
    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>
    
    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```

  - 다른 terminal에서 master에 접속 후 실행 상태 확인

  - ```
    $ kubectl get pods
    ```

  - ```
    NAME           READY   STATUS             RESTARTS   AGE
    debug          0/1     ImagePullBackOff   0          9m7s		
    debugpod       1/1     Running            0          39s
    ```

  - 테스터용 포드를 중지

  - ```
    $ exit
    ```

  - 이렇게 하면 테스터용 포드인 `debugpod`가 삭제되어있고 `debug`는 `ErrImagePull` 상태가 되어있음. 이것도 삭제하면 됨



- 포드 삭제 명령어

  - ```
    $ kubectl delete pod POD_NAME
    ```

  - ```
    $ kubectl delete -f YAML_FILE
    ```

- 포드의 로그 확인

  - ```
    $ kubectl logs my-nginx-pod
    ```





- nginx와 ubuntu 두개의 컨테이너를 하나의 포드로 구성

  - nginx-pod-with-ubuntu.yml 파일 작성

  - ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: my-nginx-pod
    spec:
      containers:
      - name: my-nginx-container
        image: nginx:latest
        ports:
          - containerPort: 80
            protocol: TCP
      - name: ubuntu-sidecar-container
        image: alicek106/rr-test:curl
        command: ["tail"]
        args: ["-f", "/dev/null"]
    ```

  - `$ kubectl apply -f nginx-pod-with-ubuntu.yml` 명령어로 포드 생성

  - 생성된 포드에 접속

  - ```
    $ kubectl exec -it my-nginx-pod -c ubuntu-sidecar-container -- bash
    ```

  - 로컬 호스트 정보 가져오기

  - ```
    $ curl localhost
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>
    
    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>
    
    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```





### 사이드카 패턴

- 웹 서버 컨테이너와 최신 컨텐츠로 깃허브에서 가져오는 컨테이너를 하나의 파드로 묶음



- 깃허브에서 정기적으로 컨텐츠 다운받는 쉘을 작성 

  - `contents-cloner` 파일 작성

  - ```shell
    #!/bin/bash
    
    # CONTENTS_SOURCE_URL 환경변수가 설정되어 있는지 확인
    # 없는 경우 에러 종료
    if [ -z $CONTENTS_SOURCE_URL ]; then
        exit 1
    fi
    
    # 처음에는 git clone을 통해서 컨텐츠를 가져옮
    git clone $CONTENTS_SOURCE_URL /data
    
    # 이후부터는 60초 마다 깃헙에서 컨텐츠를 가져옮
    cd /data
    while true
    do
        date
        sleep 60
        git pull
    done
    ```

  - 깃허브에서 정기적으로 컨텐츠를 다운받는 컨테이너 이미지 작성을 위한 `Dockerfile`을 작성

  - ```dockerfile
    FROM ubuntu:16.04
    RUN apt-get update && apt-get install -y git
    COPY ./contents-cloner /contents-cloner
    RUN chmod a+x /contents-cloner
    WORKDIR / 
    CMD [ "/contents-cloner" ]
    ```

  - 이미지 빌드 후 레지스트리(도커허브)에 등록

    ```
    docker build --tag dockerhub-계정/c-cloner:0.1 .
    ```

  - 도커 이미지가 생성됨

  - ```
    $ docker images
    REPOSITORY                  TAG          IMAGE ID       CREATED              SIZE
    myanjini/c-clone            0.1          9b8402d0a260   About a minute ago   252MB
    ```

  - 