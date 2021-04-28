### Vagrant Ansible

- Vagrantfile로 `$ vagrant up` 실행
  - Vagrantfile은 강사님 Github 주소 (`https://github.com/joneconsulting/ansible_cloud`)의 master branch에서 clone 받으면 됨
- 만약 public network에 문제가 생겼을 경우 Vagrantfile에서 public_network 주석처리
- 설치 중간에 선택하는 사항 생기면 1번 선택



- ssh 실행 후
  - sudo yum install -y net-tools
  - sudo yum install -y epel-release
  - sudo yum install -y ansible



- vagrant 종료 후 Vagrantfile에서 public_network와 bootstrap.sh 주석 해제

- bootstrap.sh 파일 작성

  - ```sh
    yum install -y epel-release
    yum install -y ansible
    ```

  - `ping 서버주소`로 서버와 연결이 잘 되는지 확인



- ansible-server의 /etc/ansible/hosts 파일 수정

  - 마지막에 다음 코드 추가

  - ```
    [nginx]
    172.20.10.11
    172.20.10.12
    ```

  - 172.20.10.11은 ansible-node01의 주소

  - 172.20.10.12은 ansible-node02의 주소



- node2 실행 - vagrant up을 통해서

- ping ip주소(node1, node2) 확인

  - 확인이 안됨. /etc/hosts 파일에서 node1, node2 에 대한 정보를 추가하지 않았기 때문

  - /etc/hosts 파일 수정(server에서)

  - ```
    172.20.10.10 ansible-server
    172.20.10.11 node1
    172.20.10.12 node2
    ```

  - 즉, host에 node를 추가하는 것임

  - 이렇게 하면 ping으로 서버에서 노드로 접속이 가능



- 각 노드에 접속
  - ssh ansible-node01 입력 -> 노드1에 접속 (pw : vagrant)
  - ssh ansible-node02 입력 -> 노드 2에 접속 (pw : vagrant)
  - 접속할때마다 비밀번호를입력해야함
- 키를 통해 노드에 비밀번호 입력 없이 바로 접속하기
  - ssh-keygen 입력 -> 엔터키누름 -> 키 생성(private key, public key 생성됨)
  - ssh-copy-id root@ansible-node01 입력
  - ssh-copy-id root@ansible-node02 입력
  - 키를 복사하여 각 노드에 전달
  - ssh root@ansible-node01 입력 -> 추가적으로 묻는것없이 바로 접속됨
  - ssh root@ansible-node02 입력 -> 추가적으로 묻는것없이 바로 접속됨



- 새로운 키 만들고 접속하기
  - ssh-keygen입력 -> 기존의 키파일에 overwrite 할 건지 묻는 질문에 yes 입력 -> 키 생성 됨
  - ssh-copy-id root@ansible-node01 입력 -> root password: vagrant
  - ssh-copy-id root@ansible-node02 입력 -> root password: vagrant
  - ssh-copy-id vagrant@ansible-node01 입력 -> password 없음
  - ssh-copy-id vagrant@ansible-node02 입력 -> password 없음
  - ssh vagrant@ansible-node01입력하면 여기에 바로 접속이 되야함
  - ssh root@ansible-node01 입력하면 여기에 바로 접속이 되야함
  - 노드 2도 마찬가지임



- server에서 vi /etc/ansible/hosts 입력 -> 맨 밑에 각 노드의 ip 주소가 추가되어있어야 함([nginx] 아래에)



- ping 테스트 명령어
  - `ansible all -m ping ` 입력 -> SUCCESS 가 나옴 -> 각 노드에 ping 한 결과가 모두 성공했음을 의미함
  - `ansible nginx ping` 입력 -> nginx에 대한 ping 결과 조회 가능



- 각 노드와 서버에 대한 정보
  - ansible-server
    - server의 /etc/hosts : 127.0.0.1 localhost 가 있음
    - server의 hostname : ansible-server
    - server의 ip 주소 : 172.20.10.10
  - ansible-node01
    - node01의 /etc/hosts : 127.0.0.1 localhost 가 있음
    - node01의 hostname : ansible-node01
    - node01의 ip 주소 : 172.20.10.11
  - ansible-node02
    - node02의 /etc/hosts : 127.0.0.1 localhost 가 있음
    - node02의 hostname : ansible-node02
    - node02의 ip 주소 : 172.20.10.12



- ping - server에서 실행할 때
  1. ping 172.20.10.10 : 자기 자신에 대한 연결 확인
  2. ping 172.20.10.11 : node 1 에 대한 연결 확인
  3. ping 172.20.10.12 : node 2 에 대한 연결 확인

  

- ping - server에서 실행할 때 - hostname 이용

  1. ping ansible-server : 자기 자신에 대한 연결 확인
  2. ping ansible-node01 : node 1 에 대한 연결 확인
  3. ping ansible-node02 : node 2 에 대한 연결 확인



- /etc/ansible/hosts 파일: ansible의 대상을 등록하는 파일
  - server에서 파일을 열어서 노드에 대한 정보를 등록
  - 노드의 ip 주소로 등록할수도 있고 hostname으로도 등록할 수 있음
  - hostname의 경우 /etc/hosts 에서 등록해야함



- `$ ansible 172.20.10.11 -m shell -a "uptime"`



