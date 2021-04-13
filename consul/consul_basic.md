### consul

- 설치 : https://www.consul.io/downloads

  - zip 파일 다운로드

- Consul 기동 

  - `consul_1.9.4_windows_amd64` 디렉터리로 이동

  - ```
    $ consul agent -dev -ui -datacenter zone1 -node host1
    ```

  - 127.0.0.1:8500 접속 -> 127.0.0.1:8500/ui/zone1/services 로 접속됨

- Dig 설치 : [Downloads - ISC](https://www.isc.org/download/)

  - Bind 9 에서 Current-Stable 의 zip 파일 다운로드 

- Dig 이용

  - `BIND9.16.13.x64` 디렉터리로 이동

  - ```
    $ dig www.naver.com
    ```

  - ```
    # 실행 결과
    ; <<>> DiG 9.16.13 <<>> www.naver.com
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52341
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 3, ADDITIONAL: 4
    
    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 4096
    ; COOKIE: 8d967ff80cbb83238936f80c6074eabbd04e2db87d6b4f15 (good)
    ;; QUESTION SECTION:
    ;www.naver.com.                 IN      A
    
    ;; ANSWER SECTION:
    www.naver.com.          18880   IN      CNAME   www.naver.com.nheos.com.
    www.naver.com.nheos.com. 126    IN      A       125.209.222.142
    www.naver.com.nheos.com. 126    IN      A       125.209.222.141
    
    ;; AUTHORITY SECTION:
    nheos.com.              171692  IN      NS      gns2.nheos.com.
    nheos.com.              171692  IN      NS      gns1.nheos.com.
    nheos.com.              171692  IN      NS      gns3.nheos.com.
    
    ;; ADDITIONAL SECTION:
    gns1.nheos.com.         18924   IN      A       103.6.174.86
    gns2.nheos.com.         19247   IN      A       210.89.165.22
    gns3.nheos.com.         19129   IN      A       125.209.246.230
    
    ;; Query time: 2 msec
    ;; SERVER: 168.126.63.1#53(168.126.63.1)
    ;; WHEN: Tue Apr 13 09:50:10 ;; MSG SIZE  rcvd: 241
    ```

  - naver.com에 대한 정보가 나온다.



- Consul members

  - `consul_1.9.4_windows_amd64` 디렉터리로 이동

  - ```
    $ consul members
    ```

  - ```
    # 실행 결과
    Node   Address         Status  Type    Build  Protocol  DC     Segment
    host1  127.0.0.1:8301  alive   server  1.9.4  2         zone1  <all>
    ```

  - consul의 member에 대한 정보가 나온다.



### python + flask microservice

- microservice 코드 - `order.py` 작성

- ```python
  from flask import Flask
  import requests, os
  
  app = Flask(__name__)
  
  @app.route("/")
  def get_order():
      
      service_address = '127.0.0.1'
      service_port = 15001
  
      url = "http://{}:{}".format(service_address, service_port)
  
      response = requests.get(url)
      ver = "1.0"
      payload = '{"Service":"Order", "Version":' + ver + '}\n'
      payload = payload + response.content.decode('utf-8')
      return payload
  
  if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=15000)
  ```

- 코드 실행

- ```
  $ python order.py
  ```

- 오류 발생함 (ConnectionError 등)-> 다른 서비스가 실행되지 않았기 때문



- `invoice.py` 작성

- ```python
  from flask import Flask
  import requests, os
  
  app = Flask(__name__)
  
  @app.route("/")
  def get_order():
      
      # Tax Service 정보
      service_address = '127.0.0.1'
      service_port = 15002
  
      url = "http://{}:{}".format(service_address, service_port)
  
      response = requests.get(url)
      ver = "1.0"
      payload = '{"Service":"Invoice", "Version":' + ver + '}\n'
      payload = payload + response.content.decode('utf-8')
      return payload
  
  if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=15001)
  ```



- `tax.py` 작성

- ```python
  from flask import Flask
  import requests, os
  
  app = Flask(__name__)
  
  @app.route("/")
  def get_order():
      
      ver = "1.0"
      payload = '{"Service":"Tax", "Version":' + ver + '}\n'
      return payload
  
  if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=15002)
  ```



- 코드 실행 후 서비스 작동 확인

  - 여러개의 terminal에서 order.py, invoice.py, tax.py 동시에 실행

  - ```
    $ python 파일이름.py
    ```

  - port 번호 15000 : order, 15001 : invoice, 15002 : tax

  - terminal 하나 더 열어서 서비스 작동 확인한다.

  - curl 명령어로 서비스 작동 확인 - order.py

  - ```
    $ curl http://127.0.0.1:15000
    {"Service":"Order", "Version":1.0}
    {"Service":"Invoice", "Version":1.0}
    {"Service":"Tax", "Version":1.0}
    ```

  - curl 명령어로 서비스 작동 확인 - invoice.py

  - ```
    $ curl http://127.0.0.1:15001
    {"Service":"Invoice", "Version":1.0}
    {"Service":"Tax", "Version":1.0}
    ```

  - curl 명령어로 서비스 작동 확인 - tax.py

  - ```
    $ curl http://127.0.0.1:15002
    {"Service":"Tax", "Version":1.0}
    ```

  - git bash 에서 실행하니까 아래처럼 나오는데 보기 불편함. 

  - ```
    # git bash 에서 실행한 것
    
    $ curl http://127.0.0.1:15000
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   105  100   105    0     0  13125      0 --:--:-- --:--:-- --:--:-- 13125{"Service":"Order", "Version":1.0}
    {"Service":"Invoice", "Version":1.0}
    {"Service":"Tax", "Version":1.0}
    ```

  - 먼저 실행한 것은 anaconda prompt 에서 실행한 것인데 json 데이터만 볼 수 있어서 결과가 더 깔끔하다.



### consul service 등록하기

1. `consul_1.9.4_windows_amd64` 디렉터리에서 `consul.d` 디렉터리를 만들고 이동.

   - ```
     $ mkdir consul.d
     $ cd consul.d
     ```

2. order.json 파일 작성

   - ```json
     {
         "service": {
             "name": "order",
             "tags": ["order"],
             "port": 15000
         }
     }
     ```

3. invoice.json 파일 작성

   - ```json
     {
         "service": {
             "name": "invoice",
             "tags": ["invoice"],
             "port": 15001
         }
     }
     ```

4. tax.json 파일 작성

   - ```json
     {
         "service": {
             "name": "tax",
             "tags": ["tax"],
             "port": 15002
         }
     }
     ```

5. consul 명령어 실행

   - `consul_1.9.4_windows_amd64` 디렉터리로 이동 후 아래 명령어 실행

   - ```
     $ consul agent -dev -ui -datacenter zone1 -node host1 -config-dir ./consul.d
     ```

6. `127.0.0.1:8500` 에 접속하여 결과 확인

   - Service : invoice, order, tax가 있다.
   - Nodes : host1에서 invoice, order, tax에 대한 정보를 볼 수 있다.

7. dig command 확인

   - `BIND9.16.13.x64` 디렉터리로 이동

   - ```
     $ dig @127.0.0.1 -p 8600 order.service.consul SRV
     ; (1 server found)
     ;; global options: +cmd
     ;; Got answer:
     ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 13076
     ;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 3
     ;; WARNING: recursion requested but not available
     
     ;; OPT PSEUDOSECTION:
     ; EDNS: version: 0, flags:; udp: 4096
     ;; QUESTION SECTION:
     ;order.service.consul.          IN      SRV
     
     ;; ANSWER SECTION:
     order.service.consul.   0       IN      SRV     1 1 15000 host1.node.zone1.consul.
     
     ;; ADDITIONAL SECTION:
     host1.node.zone1.consul. 0      IN      A       127.0.0.1
     host1.node.zone1.consul. 0      IN      TXT     "consul-network-segment="
     
     ;; Query time: 1 msec
     ;; SERVER: 127.0.0.1#8600(127.0.0.1)
     ;; WHEN: Tue Apr 13 11:28:18 ;; MSG SIZE  rcvd: 144
     ```





### port 번호를 동적으로 생성하여 활용하기

1. order.py 수정

   - ```python
     from flask import Flask
     import requests, os
     
     app = Flask(__name__)
     
     @app.route("/")
     def get_order():
         url = os.environ.get('INV_SVC_URL')
     
         # service_address = '127.0.0.1'
         # service_port = 15001
     
         # url = "http://{}:{}".format(service_address, service_port)
     
         response = requests.get(url)
         ver = "1.0"
         payload = '{"Service":"Order", "Version":' + ver + '}\n'
         payload = payload + response.content.decode('utf-8')
         return payload
     
     if __name__ == '__main__':
         app.run(debug=True, host='0.0.0.0', port=15000)
     ```

   - port 번호를 고정시키지 않고 동적으로 생성하도록 url에 대한 정보를 바꾸었다.

2. invoice.py 수정

   - ```python
     from flask import Flask
     import requests, os
     
     app = Flask(__name__)
     
     @app.route("/")
     def get_order():
         url = os.environ.get('TAX_SVC_URL')
     
         # Tax Service 정보
         # service_address = '127.0.0.1'
         # service_port = 15002
     
         # url = "http://{}:{}".format(service_address, service_port)
     
         response = requests.get(url)
         ver = "1.0"
         payload = '{"Service":"Invoice", "Version":' + ver + '}\n'
         payload = payload + response.content.decode('utf-8')
         return payload
     
     if __name__ == '__main__':
         app.run(debug=True, host='0.0.0.0', port=15001)
     ```

   - 여기도 마찬가지로 url 의 정보를 바꾸어 port 번호를 동적으로 생성하도록 했다.

3. tax.py

   - 이거는 수정하지 않는다.

4. order.py, invoice.py 종료 후 다시 실행

   - 이번에는 실행할 때 환경 변수를 넣어야 한다.

   - ```
     $ set INV_SVC_URL=http://127.0.0.1:15001
     $ python order.py
     ```

   - ```
     $ set TAX_SVC_URL=http://127.0.0.1:15002
     $ python invoice.py
     ```

5. curl 명령어로 확인

   - ```
     $ curl http://127.0.0.1:15000
     {"Service":"Order", "Version":1.0}
     {"Service":"Invoice", "Version":1.0}
     {"Service":"Tax", "Version":1.0}
     ```

   - ```
     $ curl http://127.0.0.1:15001
     {"Service":"Invoice", "Version":1.0}
     {"Service":"Tax", "Version":1.0}
     ```

   - ```
     $ curl http://127.0.0.1:15002
     {"Service":"Tax", "Version":1.0}
     ```

   - 정상 작동함을 확인할 수 있다. 이때 하나라도 작동 중지되면 connection 오류가 발생한다.





### proxy

> order, invoice, tax 등의 서비스의 포트번호를 가상의 번호로 바꿔 사용할때 쓰인다.



1. order.py, invoice.py, tax.py 중지 후 환경 변수를 바꿔서 다시 실행

   - 이때 환경 변수의 포트 번호를 다른 번호로 설정

   - ```
     $ set INV_SVC_URL=http://127.0.0.1:16001
     $ python order.py
     ```

   - ```
     $ set TAX_SVC_URL=http://127.0.0.1:16002
     $ python invoice.py
     ```

   - 이때 curl 명령어를 기존의 포트번호(15000, 15001)를 이용하여 실행하면 오류가 발생한다. (ConnectionError 등)

2. service 목록 확인 - 이건 그냥 확인하는 용도, proxy 와 관련은 없음

   - ```
     $ curl http://127.0.0.1:8500/v1/catalog/services
     {
         "consul": [],
         "invoice": [
             "invoice"
         ],
         "order": [
             "order"
         ],
         "tax": [
             "tax"
         ]
     }
     ```

   - 서비스 종류 확인 가능하다.

3. tax.json 파일 수정

   - ```json
     {
         "service": {
             "name": "tax", 
             "tags": ["tax"], 
             "port": 15002,
             "connect": {
                 "sidecar_service": {}
             }
         }
     }
     ```

4. invoice.json 파일 수정

   - ```json
     {
         "service": {
             "name": "invoice", 
             "tags": ["invoice"], 
             "port": 15001,
             "connect": {
               "sidecar_service": {
                 "proxy": {
                   "upstreams": [
                     {
                       "destination_name": "tax",
                       "local_bind_port": 16002
                     }
                   ]
                 }
               }
             }
         }
     }
     ```

5. order.py 수정

   - ```json
     {
         "service": {
             "name": "order", 
             "tags": ["order"], 
             "port": 15000,
             "connect": {
               "sidecar_service": {
                 "proxy": {
                   "upstreams": [
                     {
                       "destination_name": "invoice",
                       "local_bind_port": 16001
                     }
                   ]
                 }
               }
             }
         }
     }
     ```

6. 서버 중지후 다시 실행

   - ```
     $ consul agent -dev -ui -datacenter zone1 -node host1 -config-dir ./consul.d
     ```

   - order.py, invoice.py, tax.py 는 다시 실행할 필요 없다.

7. consul connect proxy 명령어 실행

   - ```
     $ consul connect proxy -sidecar-for order &
     ```

   - ```
     $ consul connect proxy -sidecar-for invoice &
     ```

   - ```
     $ consul connect proxy -sidecar-for tax &
     ```

8. order.py, invoice.py에서 port 번호 바꾸기

   - order.py와 invoice.py에서 `service_port = 16001`, `service_port = 16002`로 각각 바꾸기(order = 16001, invoice = 16002)
   - `url = os.environ.get('INV_SVC_URL')` 은 주석 처리

9. curl 명령어로 데이터 확인

   - ```
     $ curl http://127.0.0.1:16001
     {"Service":"Invoice", "Version":1.0}
     {"Service":"Tax", "Version":1.0}
     ```

   - ```
     $ curl http://127.0.0.1:16002
     {"Service":"Tax", "Version":1.0}
     ```

   - 16001과 16002 포트로 접속이 가능하다.

   - invoice와 tax 두개만 proxy로 넣었으므로 16000으로는 접근이 불가능하다.

10. 원래는 환경변수를 바꾸어서 실행하려고 했는데(`Section 1. Service Discovery.pdf` 파일 17쪽) 오류가 나서 직접 코드를 바꾸는 것으로 진행하였다.



### 접근 권한 제어

1. `consul_1.9.4_windows_amd64` 디렉터리로 이동

2. 각 서비스에 대한 접근 권한 확인하기

   - ```
     $ consul intention check order invoice
     Allowed
     ```

   - ```
     $ consul intention check invoice tax
     Allowed
     ```

   - ```
     $ consul intention check order tax
     Allowed
     ```

3. 서비스들에 대해 접근 못하도록 하기

   - ```
     $ consul intention create -deny invoice tax
     ```

   - 이렇게 하면 invoice에서 tax로 접근이 불가능해진다.

   - ```
     $ consul intention check invoice tax
     Denied
     ```

4. 웹 브라우저에서 서비스간 접근 권한 확인, 제어하기

   - 웹 페이지에 접속하면 페이지 상단의 `Services`로 들어간다.
   - 각 서비스 중 deny 했던 `invoice`에 들어가면 invoice에서 tax로 접근이 불가능함을 확인할 수 있다.
   - 다른 서비스들에 대해서도 접근이 가능한지 확인할 수 있다.
   - 페이지 상단의 `Intentions`에 들어가면 접근 권한을 설정할 수 있다.
   - 이미 invoice에서 tax로 접근을 못하게 deny 했으므로 이러한 내용을 볼 수 있다.
   - 다른 서비스들에 대해서도 접근 권한을 추가하기 위해서는 오른쪽 위의 `create` 버튼을 클릭하여 진행하면 된다.

