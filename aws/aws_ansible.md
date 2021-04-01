### ansible을 이용한 aws 인스턴스 생성 및 배포



- aws iam 이동

  - 사용자 만들기
  - 이름: ansible-user

  - 키 : Name 값 : ansible user
  - 권한
    - IAMFullAccess
    - AmazonEC2FullAccess
    - AmazonS3FullAccess
    - AmazonRDSFullAccess
    - AmazonVPCFullAccess

  - 액세스 키 csv 파일 다운로드

  

- aws ec2 이동

  - 보안 그룹으로 이동
  - 보안 그룹 생성 
  - 이름 : development
  - 설명 : security group for ansible ops
  - 인바운드 규칙 추가에서 유형은 사용자 지정 TCP이고 포트 범위는 0, 소스는 내 IP 주소로 설정하면 IP 주소를 얻을 수 있는데 이를 저장하고 규칙을 추가하지는 않는다.
    - 내 ip 주소 : 1.229.73.137/32
  - 보안 그룹 생성 버튼 클릭

  

- 인스턴스 생성
  - 단계 1: Amazon Linux 2 AMI (가장 위에 있는 거)

  - 단계 2: t2.micro
  - 단계 3: 변동사항 없음

  - 단계 4: 스토리지 크기 20GiB

  - 단계 5: Key는 Name, Value는 ansible-ec2

  - 단계 6: 새 보안 그룹 생성

  - 단계 7: 검토

  - 키페어 생성: 새로 만드시오

  
  
- 다운 받은 키를 이용하여 ssh 접속
  
  - 사용자 이름(ec2-user)과 호스트(인스턴스의 public ip) 주의하여 접속
  
  
  
- `$ sudo yum update`
  
  - `$ sudo yum install git`
  - `$ sudo amazon-linux-extras install ansible2`
  
  
  
- 인스턴스 중지 후 AMI 생성
  
  - 표시 여부를 퍼블릭으로 바꾸기


- vagrant의 ansible-server ssh 접속

  - `$ git clone 강사님_github_ansible_코드_주소`
  - `$ cd ansible_cloud`
  - `$ git checkout master`
  - `$ ll`
  - ansible_cloud 디렉터리 안에 amazon-ansible-playbook 디렉터리가 있으면 됨
  - `$ sudo yum install python-pip`
  - `$ pip install boto boto3`
  - `$ sudo pip install awscli`
  - `$ aws configure`
  - `$ export AWS_ACCESS_KEY_ID=AKIA2O3KVQTI5KC4YU5K`
  - `$ export AWS_SECRET_ACCESS_KEY=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`
  - `$ env | grep "AWS_"`
  - `$ aws s3 ls`
  - 이 명령어를 실행하면 4개의 구성요소가 나와야 한다.
  - `$ aws ec2 describe-images --owner 719093859537`
  - 맨 아래에 "Name" : "ansible-ec2-image" 가 나와야함
  
  
  
- AWS 에서 만든 인스턴스 키 파일을 vagrant에서 이용할 수 있도록 설정
  
  - `$ cd amazon-ansible-playbook`
  
  - `$ mv your-iam-key.pem ansible-keypair.pem`
  - `$ vi ansible-keypair.pem`
  - AWS 에서 다운로드 받은 key 파일을 열어서 복사한 후 붙여넣기
    - typora, 메모장 등으로 파일 열면 됨
  
  
  
- tree 설치 (선택사항)

  - `$ sudo yum install tree`

  - `$ tree roles`
  
  
  
- development 파일 작성
  
  - `$ vi development.yml`
  
  - vars: 부분에서 아래의 값들 수정 또는 확인하기
  - AMI ID값 복사해서 ami_image에 붙여넣기
  - key_name: ansible-keypair
  - my_ip: 아까 보안그룹때 복사한 ip주소
  - group_name: "development"
  
  
  
- 보안그룹의 `main.yml`파일 region 수정
    
    - `$ vi roles/security_group/tasks/main.yml`
    - region: us-east-1



- vagrant의 키파일과 ansible-playbook 명령어로 AWS ec2 인스턴스 생성

  - `$ cd amazon-ansible-playbook`

  - ```
    $ ansible-playbook -i hosts/development/ec2.py development.yml --private-key=ansible-keypair.pem
    ```

  - 오류가 걸리는게 맞음

  - EC2 보안 그룹에서 인바운드 규칙에 유형이 ssh이고 프로토콜이 TCP, 포트가 22번, 소스가 내 ip로 된 규칙이 추가되어있으면 됨

  

- ec2의 `main.yml` 파일수정
  
  - `$ vi ./roles/ec2/tasks/main.yml`
  - ec2 모듈의 항목이 ansible에서 지원되는지 확인
    - playbook module 사이트로 이동하여 ec2 관련 모듈이 있는지 확인할 수 있다.
   - region: us-east-1 로 수정



- AWS ec2 인스턴스 생성 다시 도전

  - ```
    $ ansible-playbook -i hosts/development/ec2.py development.yml --private-key=ansible-keypair.pem
    ```

  - `$ ssh -i ansible-keypair.pem ec2-user@ec2인스턴스의_public_ip_주소`

  - yes 입력 -> 접속 안됨
    
  - 오류 메시지 : Permissions 0664 for 'ansible-keypair.pem' are too open.

   - `$ chmod 600 ansible-keypair.pem`
     
   - `$ ll`
     
   - ansible-keypair.pem 에 대한 권한이 바뀌어있음 (-rw---------)
     
   - `$ ansible-playbook -i hosts/development/ec2.py development.yml --private-key=ansible-keypair.pem`
     
   - `$ ssh -i ansible-keypair.pem ec2-user@ec2인스턴스의_public_ip_주소`
     
   - AWS EC2 인스턴스가 하나 생성되어있음

  

- 인스턴스 여러개 생성하기

  - `$ ansible-playbook -i hosts/development/ec2.py development.yml --private-key=ansible-keypair.pem`

  - `$ ssh -i ansible-keypair.pem ec2-user@ec2인스턴스의_public_ip_주소`
  - ansible-playbook 명령어를 한번 더 실행하면 ec2 인스턴스가 더 만들어짐
    - 이름, keypair는 다 똑같고 인스턴스 ID가 다름
   - 여러번 실행하면 실행한 횟수만큼 인스턴스가 만들어짐

  
  
- 3대의 ec2 인스턴스가 만들어지게 한 후 임의의 하나의 인스턴스를 ansible-server가 지정

  - 나머지 2개의 ec2 인스턴스를 ansible로 제어
  - 각 인스턴스의 private ip 를 ping으로 테스트함
    - `$ ping private_ip`
    - 실행이 되지 않는다.
    - 보안그룹에서 인바운드 규칙 편집 클릭 후 유형에서 ICMP - IPv4 선택 후 소스에서 development에 해당하는 것(sg-번호) 선택
    - 다시 ping 명령어를 입력하면 실행 성공
  - $ ssh 172.31.59.141(인스턴스의 private_ip) -> 아무것도 실행 안됨
    - development 보안 그룹의 인바운드 규칙에서 ssh 유형, TCP 프로토콜, 포트번호는 22번, 소스는 development에 해당하는거 선택하고 추가
    - `$ ssh 172.31.58.141(인스턴스의 private_ip)` 
    - permission denied 문제 발생
  
  
  
- permission denied 문제 해결을 위한 public_key 생성

  - public_key 생성 위해 `$ ssh-keygen` 입력 -> 키 생성됨
  - `$ ssh-copy-id 인스턴스의_private_ip`
  - permission denied 문제 다시 발생
  - `$ cd ~`
  - `$ cd .ssh`
  - `$ ll `
  - id_rsa와 id_rsa.pub파일이 있음
    - id_rsa : private_key
    - id_rsa.pub : public_key
   - `$ cat id_rsa.pub`
   - 각 노드인스턴스에서 `$ cat authorized_keys` 입력
   - 키 값이 서로 다른 것을 확인
   - ansible-ec2 인스턴스에서 `$ cat id_rsa.pub`을 통해 나온 키 값을 복사해서 노드 인스턴스에 저장. 노드 인스턴스의 기존의 키 값은 삭제 함
   - 다시 `$ ssh 각노드인스턴스의_private_ip` 입력 -> 성공




- 각 노드 인스턴스에 대한 그룹 추가 후 ping, uptime, 메모리 용량, df -h 테스트 실행

  - `$ sudo vi /etc/ansible/hosts`

  - 맨 밑에 다음 문장 추가

  - ```
    [ec2]
    각 인스턴스노드의 private_ip
    
    [node1]
    인스턴스노드1의 private_ip
    
    [node2]
    인스턴스노드2의 private_ip
    ```

  - `$ ansible ec2 -m ping` -> 둘다 성공함

  - `$ ansible ec2 -m shell -m "uptime"` -> 둘다 성공함

  - `$ ansible node1 -m shell -a "free -h"` -> 1번 노드의 메모리 용량 확인 가능

  - `$ ansible node2 -m shell -a "df -h"` -> 2번 노드의 df -h 명령 실행