### NFS 서버, 클라이언트 테스트

- 서버 파일 만들기

  - `$ vi nfs.yml`

  - ```yaml
    ---
    - name: setup for nfs server
      hosts: localhost
      gather_facts: no
      
      tasks:
        - name: make nfs_shared directory
          file:
            path: /home/vagrant/nfs_shared
            state: directory
            mode: 0777
        
        - name: configure /etc/exports
          become: yes
          lineinfile:
            path: /etc/exports
            line: /home/vagrant/nfs_shared/ 172.20.10.0/24(rw, sync)
        
        - name: nfs service restart
          become: yes
          service:
            name: nfs
            state: restarted
    ```

  - `$ ansibe-playbook nfs.yml -k`
  - `nfs_shared` 라는 비어있는 디렉터리가 만들어짐

  

- 클라이언트 파일 만들기

- > centos node

  - `$ vi nfs_client.yml`

  - ```yaml
    ---
    - name: setup for nfs clients
      hosts: centos
      gather_facts: no
      
      tasks:
        - name: make nfs_client directory
          file:
            path: /home/vagrant/nfs
            state: directory
        
        - name: mount point directory as client
          become: yes
          mount:
            name: /home/vagrant/nfs
            src: 172.20.10.10:/home/vagrant/nfs_shared
            fstype: nfs
            opts: nfsvers=3
            state: mounted
    ```

  - `$ ansible-playbook nfs_client.yml -k`

  - 각 클라이언트 노드에 `nfs`라는 이름의 비어있는 디렉터리가 만들어짐

  

- 파일 생성하여 서버, 클라이언트 사이의 공유가 되는지 확인하기

  - 각 클라이언트 노드에서 `touch $HOSTNAME` 입력
  - 서버의 `nfs_shared` 디렉터리에 각 노드의 hostname에 해당하는 파일이 만들어짐
  - 클라이언트의 `nfs` 디렉터리에도 각 노드의 hostname에 해당하는 파일이 만들어짐
  - 서버에서 `touch $HOSTNAME` 입력
  - 서버의 `nfs_shared`와 클라이언트의 `nfs` 디렉터리에 서버의 hostname에 해당하는 파일이 생성되어있음
  - 즉, 서버와 클라이언트 사이에 파일 공유가 진행되고 있다.

  

- 클라이언트 파일 만들기

- > Ubuntu node

  - `$ vi nfs_client.yml`

  - `hosts` 부분을 수정

  - ```yaml
    ---
    - name: setup for nfs clients
      hosts: centos:ubuntu
      gather_facts: no
      
      tasks:
        - name: make nfs_client directory
          file:
            path: /home/vagrant/nfs
            state: directory
        
        - name: mount point directory as client
          become: yes
          mount:
            name: /home/vagrant/nfs
            src: 172.20.10.10:/home/vagrant/nfs_shared
            fstype: nfs
            opts: nfsvers=3
            state: mounted
    ```

  - `$ ansible-playbook ubuntu.yml -k`

  - ubuntu node에 `nfs`디렉터리가 생성됨

    - 기존의 centos만으로는 ubuntu node에 `nfs` 디렉터리가 생성되지 않음

  - 여기에는 이미 centos 노드로 만든 파일과 서버로 만든 파일들이 들어있음

  - `$ touch $HOSTNAME`을 입력하면 ubuntu node의 hostname을 이름으로 하는 파일이 생성되고 이것은 centos node와 서버에서도 확인이 가능함



#### 실습 과제

- ansible server에서 ansible을 통해 각 노드에 docker를 설치
- docker에 이미지 설치(컨테이너 배포)
  - edowon0623/my-user-service:1.1

- 설치 후 각 노드에서 msa가 정상 작동 되는지 확인
  - ex) http://172.20.10.11:8088/users
  - ex) http://127.0.0.1:18088/users
- edowon0623@gmail.com 로 오늘 저녁까지



### Microservice

