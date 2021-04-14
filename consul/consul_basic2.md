### consul & sidecar

> 강사님 github : https://github.com/joneconsulting/flask_msa 에서 clone 해서 사용

1. 이전에 만들었던 msa 가상환경에서 python-consul  설치 - anaconda prompt 사용 권장

   - ```
     $ pip install python-consul
     ```

2. (강사님의 파일) flask_msa/consul_demo 디렉터리로 이동 후 `consul_data` 디렉터리 생성

3. `docker-compose.yml` 파일을 이용하여 docker container 가동시키기

   - ```
     $ docker-compose up
     ```

   - `DEBUG agent: ~~~` 이런 메시지가 반복적으로 생성되면 된다.

4. anaconda prompt 하나 더 띄워서 BIND9.16.13.x64 디렉터리로 이동 후 다음 명령어 실행

   - ```
     $ curl http://localhost:8500/v1/catalog/service/order-ms
     ```

   - ```
     # 실행 결과
     [{"ID":"f700b41e-a8a0-b256-54e7-2afa2300dbda","Node":"ef79ef1194ac","Address":"10.5.0.2","Datacenter":"dc1","TaggedAddresses":{"lan":"10.5.0.2","lan_ipv4":"10.5.0.2","wan":"10.5.0.2","wan_ipv4":"10.5.0.2"},"NodeMeta":{"consul-network-segment":""},"ServiceKind":"","ServiceID":"order-ms","ServiceName":"order-ms","ServiceTags":["order-app"],"ServiceAddress":"10.5.0.3","ServiceTaggedAddresses":{"lan_ipv4":{"Address":"10.5.0.3","Port":5000},"wan_ipv4":{"Address":"10.5.0.3","Port":5000}},"ServiceWeights":{"Passing":1,"Warning":1},"ServiceMeta":{},"ServicePort":5000,"ServiceEnableTagOverride":false,"ServiceProxy":{"MeshGateway":{},"Expose":{}},"ServiceConnect":{},"CreateIndex":16,"ModifyIndex":16}]
     ```

5. consul_demo 디렉터리로 이동 후 servise_list.py 수정

   - ```python
     import requests
     import consul
     
     client = consul.Consul(host='localhost', port=8500)
     
     serviceName = "tax-ms"
     service_address = client.catalog.service(serviceName)[1][0]['ServiceAddress']
     service_port = client.catalog.service(serviceName)[1][0]['ServicePort']
     
     print(service_address)
     print(service_port)
     
     # request url
     # response = requests.get("http://{}:{}".format(service_address, service_port))
     # res = response.content.decode('utf-8')
     
     # print(res)
     ```

   - 코드 실행

   - ```
     $ python service_list.py
     ```

   - 결과

   - ```
     10.5.0.5
     5000
     ```

6. 각 서비스 확인

   - 전체 서비스

     - ```
       $ curl http://127.0.0.1:5000
       ```

     - ```
       {"Service":"Order", "Version":1.0}
       {"Service":"Invoice", "Version":1.0}
       {"Service":"Tax", "Version":1.0}
       ```

   - invoice 서비스

     - ```
       $ curl http://127.0.0.1:5001
       ```

     - ```
       {"Service":"Invoice", "Version":1.0}
       {"Service":"Tax", "Version":1.0}
       ```

   - tax 서비스

     - ```
       $ curl http://127.0.0.1:5002
       ```

     - ```
       {"Service":"Tax", "Version":1.0}
       ```

7. Key/Value 입력

   - kvs_put.py 실행

   - ```
     $ python kvs_put.py
     ```

   - http://127.0.0.1:8500 사이트의 `Key/Value`에 들어가면 새로운 key와 value가 등록되어있다.

8. Key/Value 확인

   - kvs_get.py 실행

   - ```
     $ python kvs_get.py
     ```

   - 이전에 등록했던 키와 값들을 출력할 수 있다.

