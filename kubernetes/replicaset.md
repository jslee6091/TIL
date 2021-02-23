### ReplicaSet 생성 및 삭제



1. 여러 개의 컨테이너를 실행하는 포드를 yml에서 일일이 정의하는 것은 비효율 적이다.

   - ```yaml
     # pod yml file example
     apiVersion: v1
     kind: Pod
     metadata:
       name: my-nginx-pod-a
     spec:
       containers:
       - name: my-nginx-container
         image: nginx
         ports:
         - containerPort: 80
           protocol: TCP
     ---
     apiVersion: v1
     kind: Pod
     metadata:
       name: my-nginx-pod-b
     spec:
       containers:
       - name: my-nginx-container
         image: nginx
         ports:
         - containerPort: 80
           protocol: TCP
     ```

2. ReplicaSet을 이용하면 효율적으로 할 수 있다.

   - ```yaml
     # replicaset yml file example
     apiVersion: apps/v1
     kind: ReplicaSet
     metadata:
       name: replicaset-nginx
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: my-nginx-pods-label
       template: # 포드 스펙, 탬플릿 => 생성할 포드를 명시
         metadata:
           name: my-nginx-pod
           labels:
             app: my-nginx-pods-label
         spec:
           containers:
             - name: my-nginx-container
               image: nginx:latest
               ports:
               - containerPort: 80
                 protocol: TCP
     ```

3. ReplicaSet 생성 및 확인

   - ```
     $ kubectl apply -f replicaset-nginx.yml
     ```

   - ```
     $ kubectl get replicaset
     ```

     - replicaset이 하나 생성되었고 3개의 포드를 형성했으므로 pod에는 같은 이름의 pod 3개가 생성되어있다.

4. 포드 개수 증가시키기

   - yml file에서 `replicas: 4`로 수정 후 apply
   - 기존의 3개에서 한개가 추가되었으므로 pod가 하나 더 생성된다.

5. 삭제

   - ```
     $ kubectl delete rs replicaset-nginx
     ```

   - ```
     $ kubectl delete -f replicaset.yml
     ```

     - replicaset-nginx를 정의한 yml 파일을 이용해서 삭제가 가능하다.



### ReplicaSet 동작 원리



1. my-nginx-pods-label 라벨을 가지는 pod 생성

   - ```yaml
     # yml 파일
     apiVersion: v1
     kind: Pod
     metadata:
       name: my-nginx-pod
       labels:
         app: my-nginx-pods-label
     spec:
       containers:
         - name: my-nginx-container
           image: nginx:latest
           ports:
           - containerPort: 80
     ```

2. pod 생성 후 라벨 확인

   - ```
     $ kubectl apply -f nginx-pod-without-rs.yml
     $ kubectl get pods --show-labels
     ```

   - `--show-labels`옵션을 통해 pod의 라벨도 함께 확인할 수 있다.

3. 같은 이름의 라벨을 가지는 pod 3개 생성

   - ```yaml
     apiVersion: apps/v1
     kind: ReplicaSet
     metadata:
       name: replicaset-nginx
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: my-nginx-pods-label
       template:
         metadata:
           name: my-nginx-pod
           labels:
             app: my-nginx-pods-label
         spec:
           containers:
             - name: my-nginx-container
               image: nginx:latest
               ports:
               - containerPort: 80
                 protocol: TCP
     ```

   - 이때 1번에서 먼저 생성한 pod와 같은 이름의 pod가 1개 있으므로 2개만 추가로 생성된다.

   - 만약 먼저 생성한 pod를 지우면 replicaset이 1개의 pod를 자동으로 하나 더 생성하여 3개를 맞춘다.

4. label 주석처리시 발생하는 일

   - ```
     $ kubectl edit pods replicaset-nginx-d2fw8
     ```

   - 특정 pod 이름을 입력하면 vi 에디터가 뜨고 정보를 수정할 수 있다.

   - 이때 label 관련된 부분을 주석처리하면 이에 대한 정보가 완전히 사라진다.

   - 실행되는 pod도 종료되어 자동으로 새로운 pod가 생성된다.

5. ReplicaSet 삭제

   - ```
     $ kubectl delete replicaset replicaset-nginx
     ```

   - 이때 라벨이 삭제된 포드는 직접 삭제한다.