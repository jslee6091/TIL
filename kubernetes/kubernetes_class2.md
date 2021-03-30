### 파일 전송

```
$ ansible nginx -m copy -a "src=./test.file dest=/tmp" -k
```

- `nginx` : 그룹명
- `copy` : copy module
- `./test.file` : ansible server의 원본 파일
- `/tmp` : ansible node에 파일이 복사될 위치



### 특정 서비스 설치

```
$ ansible nginx -m yum -a "name=httpd state=present" -k
```

- `yum`: centos의 패키지 설치 도구
- 서버에서 설치



### ansible server의 /etc/ansible/hosts의 [nginx]를 [centos]로 바꿈



### 각 그룹에 대한 ping 확인

- ansible centos -m ping
- ansible ubuntu -m ping
- ansible backup -m ping
- ansible webserver -m ping



### centos 서비스 설치

> 노드들을 ON 시켜야 함

- ansible-server의 root 계정 접속

  - ```
    $ ssh root@ansible-server
    ```

- centos 서비스 설치

  - ```
    $ ansible centos -m yum -a "name=httpd state=present" -k
    ```

  - ssh password 입력 : vagrant

- 각 노드에서 다음 명령어로 서비스 설치 여부 확인

  - ```
    $ yum list installed | grep httpd
    ```

- 서비스 상태 확인

  - ```
    $ systemctl status httpd
    ```

  - 상태 표시가 안된다면 start command 입력

  - ```
    $ systemctl start httpd
    ```

  - root 계정 비밀번호 입력

  - 다시 상태를 확인하면 `active` 상태임을 확인할 수 있음

- 브라우저에서 서버 접속하여 사이트 확인
  - `127.0.0.1:노드의 포트번호`입력
    - 포트 번호 : 노드 1의 경우 10080
- 해당 노드에서 서비스를 시작하지 않으면 포트번호를 입력해도 브라우저에서 확인이 안됨



### Ansible Playbook의 멱등성

> 사용자가 원하는 내용을 미리 작성을 해놓은 파일 - script 파일
>
> Docker의 Docker compose, Kubernetes의 Deployment와 유사함



- 멱등성 : 같은 설정을 여러번 적용하더라도 결과가 달라지지 않는 성질

- 멱등성이 적용되지 않는 예

  - 서버에서 다음 명령어 실행

  - ```
    $ echo -e "[mygroup]\n 172.20.10.11" >> /etc/ansible/hosts
    ```

  - ```
    $ tail -5 /etc/ansible/hosts
    ```

    - `tail -5` : 해당 파일의 가장 마지막 5줄 표시 (cat의 변형)

  - 다음 명령어 한번 더 실행

  - ```
    $ echo -e "[mygroup]\n 172.20.10.11" >> /etc/ansible/hosts
    ```

  - 이렇게 한 후 다음 명령어를 다시 실행하면 이전에 만든 것과 같은 [mygroup]이 추가되어있다.

  - ```
    $ tail -10 /etc/ansible/hosts
    ```

  - 잘못된 파일이므로 추가된 [mygroup]를 삭제함



- ansible-playbook을 이용하여 멱등성 적용 확인 예시

  - 서버로 이동 후 다음 명령어 실행

  - ```
    $ mkdir ansible-playbook
    $ cd ansible-playbook
    $ vi first-playbook.yml
    ```

  - ```yaml
    ---
    - name: Ansible_vim_test
      hosts: localhost
      tasks:
        - name: Add ansible hosts
          blockinfile:
            path: /etc/ansible/hosts
            block: |
              [mygroup]
              172.20.10.11
    ```

  - ```
    $ ansible-playbook first-playbook.yml
    ```

  - `$ cat first-playbook.yml`로 파일 확인

  - `$ tail -10 /etc/ansible/hosts`로 확인하면 아래와 같은 결과가 나옴

  - ```
    #BEGIN ANSIBLE MANAGED BLOCK
    [mygroup]
    172.20.10.11
    #END ANSIBLE MANAGED BLOCK
    ```

  - 이때 `$ ansible-playbook first-playbook.yml`을 실행하여도 /etc/ansible/hosts에는 [mygroup]이 더이상 추가되지 않는 것을 확인할 수 있다. (멱등성 성립)



- nginx 서비스에 대한 멱등성 확인

  - vi second-playbook.yml

  - ```yaml
    ---
    - name: Install nginx on CentOS
      hosts: centos
      remote_user: root
      tasks:
        - name: Install epel-release
          yum: name=epel-release state=latest
        - name: Install nginx web server
          yum: name=nginx state=present
        - name: Start nginx web server
          service: name=nginx state=started
    ```

  - `$ cat second-playbook.yml`로 확인

  - 아래 명령어를 실행하기 전에 노드에서 먼저 실행하고 있던 httpd 서비스가 있다면 모두 종료 시킴

  - ```
    $ systemctl stop httpd
    ```

  - ```
    $ ansible-playbook second-playbook.yml -k
    ```

    - tasks의 각 name 별 실행 결과를 확인할 수 있음

  - 노드에서 다음 명령어 실행

  - ```
    $ systemctl start nginx
    $ systemctl status nginx
    ```

  - 브라우저에서 `127.0.0.1:노드의 포트번호` 입력 하여 서비스 확인

  - httpd와 마찬가지로 멱등성이 성립함을 확인할 수 있다.




- nginx 홈페이지 url을 이용한 예시

  - ```
    $ curl -o index.html https://www.nginx.com/
    ```

  - vi second-playbook.yml -> yml 파일 수정

  - ```yaml
    ---
    - name: Install nginx on CentOS
      hosts: centos
      remote_user: root
      tasks:
        - name: Install epel-release
          yum: name=epel-release state=latest
        - name: Install nginx web server
          yum: name=nginx state=present
        - name: Upload default index.html for web server
          copy: src=index.html dest=/usr/share/nginx/html/ 
        - name: Start nginx web server
          service: name=nginx state=started
    ```

  - ```
    $ ansible-playbook second-playbook.yml -k
    ```

  - 위 명령어 실행 후 웹 브라우저로 확인하면 nginx의 홈페이지를 로컬에서 볼 수 있다.





### ansible playbook을 활용한 배포

1. Vagrantfile 수정

   - ansible-server의 주석 5개 해제

   - bootstrap.sh을 다음과 같이 변경

   - ```sh
     #! /usr/bin/env bash
     
     yum install -y epel-release
     yum install -y ansible 
     
     mkdir -p /home/vagrant/.vim/autoload /home/vagrant/.vim/bundle
     touch /home/vagrant/.vimrc
     touch /home/vagrant/.bashrc
     ```

   - Ansible_env_ready.yml 파일 vagrantfile과 같은 디렉터리에 추가 - 강사님 제공

   - ```yaml
     ---
     - name: Setup for the Ansible's Environment
       hosts: localhost
       gather_facts: no
     
       tasks:
         - name: Install vim-enhanced
           yum:
             name: vim-enhanced
             state: present
         
         - name: Install git
           yum:
             name: git
             state: present
         
         - name: Install pathogen.vim
           shell: "curl -fLo /home/vagrant/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim"
         
         - name: Git clone vim-ansible-yaml
           git:
             repo: 'https://github.com/chase/vim-ansible-yaml.git'
             dest: /home/vagrant/.vim/bundle/vim-ansible-yaml
         
         - name: Configure vimrc
           lineinfile:
             dest: /home/vagrant/.vimrc
             line: "{{ item }}"
           with_items:
             - "set number"
             - "execute pathogen#infect()"
             - "syntax on"
           
         - name: Configure Bashrc
           lineinfile: 
             dest: /home/vagrant/.bashrc
             line: "{{ item }}"
           with_items:
             - "alias vi='vim'"
             - "alias ans='ansible'"
             - "alias anp='ansible-playbook'"
     ```

   - 서비스가 작동중이라면 종료 후 vagrant 재생성

   - ```
     $ vagrant halt ansible-server
     $ vagrant destroy ansible-server
     $ vagrant up ansible-server
     ```

   - destroy를 하면 기존에 사용하던 키는 없어지므로 새로 발급받은 키를 사용해야함

   - ssh 접속을 하면 이전에 만든 Ansible_env_ready.yml 파일이 저장되어있음

   - vi 에디터로 열면 색상이 구분되어 코드를 보기가 편함

   - 버전 확인

     - `$ ans --version`
     - `$ anp --version`

   - /etc/hosts 파일과 /etc/ansible/hosts 파일 확인

     - `$ cat /etc/hosts`
     - `$ tail -10 /etc/ansible/hosts`

   - vi Ansible_env_version.yml 수정

   - ```yaml
     ---
     - name: Setup for the Ansible's Environment
       hosts: localhost
       gather_facts: no
     
       tasks:
       	- name: Change "/etc/hosts"
       	  blockinfile: |
       	    dest=/etc/hosts
       	    content="
       	      172.20.10.10 ansible-server
       	      172.20.10.11 ansible-node01
       	      172.20.10.13 ansible-node03"
       	  
       	- name: Change "/etc/ansible/hosts"
       	  blockinfile: |
       	  	dest=/etc/ansible/hosts
       	  	content="
       	  	  [centos]
       	  	  ansible-node01
       	  	  [ubuntu]
       	  	  ansible-node03"
       	  
       	- name: Install sshpass for Authentication
       	  yum:
       	    name: sshpass
       	    state: present
       	    
       	- name: Install vim-enhanced
           yum:
             name: vim-enhanced
             state: present
         
         - name: Install git
           yum:
             name: git
             state: present
         
         - name: Install pathogen.vim
           shell: "curl -fLo /home/vagrant/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim"
         
         - name: Git clone vim-ansible-yaml
           git:
             repo: 'https://github.com/chase/vim-ansible-yaml.git'
             dest: /home/vagrant/.vim/bundle/vim-ansible-yaml
         
         - name: Configure vimrc
           lineinfile:
             dest: /home/vagrant/.vimrc
             line: "{{ item }}"
           with_items:
             - "set number"
             - "execute pathogen#infect()"
             - "syntax on"
           
         - name: Configure Bashrc
           lineinfile: 
             dest: /home/vagrant/.bashrc
             line: "{{ item }}"
           with_items:
             - "alias vi='vim'"
             - "alias ans='ansible'"
             - "alias anp='ansible-playbook'"
     ```

   - 다음 명령어실행 - Vagrantfile 의 디렉터리에서

   - ```
     $ vagrant provision ansible-server
     ```

   - `$ ansible centos -m ping`

   - `$ ansible ubuntu -m ping`
   
   - 두 명령어가 오류 없이 실행되기 위해서는 `ssh-copy-id vagrant@ansible-node01`과 `ssh-copy-id vagrant@ansible-node03`을 해줘야 한다. (node01은 centos, node03은 ubuntu)



- 외부에서 ansible server의 접속 권한 허용

  - ```
    $ sudo vi /etc/ssh/sshd_config
    ```

  - passwordauthentication 을 no 에서 yes로 변경

  - vi Ansible_ssh_conf_4_CentOS.yml 실행

  - ```yaml
    - name: Ansible set ssh configuration for CentOS
      hosts: localhost
      gather_facts: no
      
      tasks:
        - name: PasswordAuthentication change from no to yes
          replace: 
            dest=/etc/ssh/sshd_config
            regexp='PasswordAuthentication no'
            replace='PasswordAuthenticatioin yes'
            backup=yes
            
            
        - name: SSHD restart to apply "PasswordAuthentication"
          service:
            name: sshd
            state: restarted
    ```

  - ```
    $ sudo ansible-playbook Ansible_ssh_conf_4_CentOS.yml -k
    ```





- centos인 노드에 nginx 설치하는 yml 파일

  - cd /vagrant

  - vi nginx_install.yml

  - ```yaml
    ---
    - name: install nginx on CentOS
      hosts: centos
      gather_facts: no
      become: yes
      
      tasks:
        - name: install epel-release
          yum: name=epel-release state=latest
        - name: install nginx web server
          yum: name=nginx state=present
        - name: upload default index.html for web server
          get_url: url=https://www.nginx.com dest=/usr/share/nginx/html/
        - name: start nginx web server
          service: name=nginx state=started
    ```

  - `ansible-playbook nginx_install.yml -k`



- centos 와 ubuntu 인 노드에 nginx, apache 설치하는 yml 파일

  - nginx_install.yml 파일 수정

  - vi nginx_install.yml 

  - ```yaml
    ---
    - name: install nginx on CentOS
      hosts: centos
      gather_facts: no
      become: yes
      
      tasks:
        - name: install epel-release
          yum: name=epel-release state=latest
        - name: install nginx web server
          yum: name=nginx state=present
        - name: upload default index.html for web server
          get_url: url=https://www.nginx.com dest=/usr/share/nginx/html/
        - name: start nginx web server
          service: name=nginx state=started
    
    - name: install nginx on Ubuntu
      hosts: ubuntu
      gather_facts: no
      become: yes
      
      tasks:
        - name: install nginx web server
          apt: pkg=nginx state=present update_cache=yes
        - name: upload default index.html for web server
          get_url: url=http://www.apache.com dest=/usr/share/nginx/html/
        - name: start nginx web server
          service: name=nginx state=started
    ```

  - `ansible-playbook nginx_install.yml -k`

  - 원래 ubuntu 에도 nginx 를 설치하려 했으나 오류가 발생하여 apache로 변경함
  
  - apache는 https 가 아닌 http 로 접속한다.
  
    - https 로 접속하려 했으나 443 오류 발생, 접근이 불가능하다.





- 노드에서 서버의 시간을 확인하는 방법

  - `$ vi timezone.yml`

  - ```yaml
    ---
    - name: setup timezone
      hosts: centos:ubuntu
      gather_facts: no
      become: yes
    
      tasks:
        - name: set timezone to Asia/Seoul
          timezone: name=Asia/Seoul
    ```

  - `$ ansible-playbook timezone.yml -k`

  - 노드에서 서버에 접속

  - `$ date` 입력 후 시간 확인



- 로컬의 시간을 확인하는 방법

  - `$ vi timezone.yml`

  - 위의 timezone.yml 코드에서 localhost 관련 내용 아래에 추가

  - ```yaml
    ---
    - name: setup timezone
      hosts: centos:ubuntu
      gather_facts: no
      become: yes
    
      tasks:
        - name: set timezone to Asia/Seoul
          timezone: name=Asia/Seoul
    
    - name: setup timezone for localhost
      hosts: localhost
      gather_facts: no
      become: yes
    
      tasks:
        - name: set timezone to Asia/Seoul
          timezone: name=Asia/Seoul
    ```

  - 노드에서 로컬(노드)의 시간 확인 가능 - `$ date` 입력으로 확인



- centos 노드에 설치된 nginx 삭제하기

  - `$ vi nginx_remove.yml`
  - 기존의 nginx_install.yml 에서 centos 관련 부분만 가져옴

  - ```yaml
    ---
    - name: remove nginx on CentOS
      hosts: centos
      gather_facts: no
      become: yes
      
      tasks:
        - name: install epel-release
          yum: name=epel-release state=absent
        - name: install nginx web server
          yum: name=nginx state=absent
    ```

  - nginx_install.yml 과 다른 점은 state=present 또는 state=latest 를 모두 state=absent로 바꾼 것이다.

  - `$ ansible-playbook nginx_remove.yml -k`

  - 노드에서 ` $ systemctl status nginx` 실행

  - 아무 것도 없음을 확인



- ubuntu 노드에 설치된 nginx 삭제하기

  - `$ vi nginx_remove.yml`

  - 기존 파일의 아랫부분에 ubuntu 삭제 코드 추가

  - ```yaml
    ---
    - name: remove nginx on CentOS
      hosts: centos
      gather_facts: no
      become: yes
      
      tasks:
        - name: install epel-release
          yum: name=epel-release state=absent
        - name: install nginx web server
          yum: name=nginx state=absent
    
    - name: remove nginx on Ubuntu
      hosts: ubuntu
      gather_facts: no
      become: yes
      
      tasks:
        - name: remove nginx web server
          apt:
            name: nginx
            state: absent
        - name: remove useless packages from the cache
          apt:
            autoclean: yes
        - name: remove dependencies that are no longer required
          apt:
            autoremove: yes
    ```

  - centos의 tasks의 yum처럼 한줄로 작성해도 되고 ubuntu의 tasks의 apt 처럼 여러줄로 작성해도 된다.

  - `$ ansible-playbook nginx_remove.yml -k`

  - ubuntu 노드의 nginx 서비스가 종료된 것을 브라우저를 통해 확인할 수 있다.