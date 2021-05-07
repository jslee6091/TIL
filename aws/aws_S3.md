### Creating a Basic Amazon S3 Lifecycle Policy

- 개인, 어플리케이션, AWS 서비스의 데이터(=파일)를 보관
  - 백업, 로그 파일, 재해 복구 이미지 유지 관리
  - 분석을 위한 빅데이터 저장
  - 정적 웹 사이트 호스팅
    - 99.999999999%의 내구성을 제공 → AWS 리전 내에서 최소 3개의 물리적 가용영역에 분산해서 저장
    - 99.5% ~ 99.99%의 가용성을 제공



**![img](aws_S3.assets/g04gHt7qkPcOfj6nB_-Xu_RwldA3pGmR2PWbfSXOqyz1wOPBVDt6aY59LhiDyQVO6mxuaATcXHdaIqOv5ZZZfxV3XWsMJb5rrZLjxPXbI68K1QubklB3lUtUgyZsd0-nTYwpToEw)**



**Amazon S3**

- 객체 기반의 무제한 파일 저장 스토리지
- 99.999999999% 내구성
- 사용한 만큼만 지불 (GB 당 과금)
- 객체 URL을 통해 쉽게 파일을 공유
- *정적 웹 사이트 호스팅* 가능



**Amazon Glacier**

- 99.999999999% 내구성
- 아카이브 및 백업 용도
- S3 대비 1/5 비용





### Configuring Amazon S3 Buckets to Host a Static Website with a Custom Domain



![img](aws_S3.assets/UcXKEk_87DCXS2E6IjnrCQCZeWyhxNxLz5wtzm6KvF1eDYjZ8ReaJ4CgzN5lNK30Jd8m2Ps9kobU02uOsYvKVTs65vJNxOxWz4OMx7XK2pz4hV-7I9J9bpS-xdQDq9Xn-DHN6MTa)



#### S3 Bucket을 생성하고 정적 웹 사이트 호스팅 설정

1. S3 Bucket 생성
   - 주의
     - 연동할 도메인 이름으로 버킷을 생성
     - 버킷에 퍼블릿 접근이 가능하도록 설정

2. S3 Bucket에 아무 html 파일을 업로드
3. 정적 웹 사이트 호스팅 설정
   - 정적 웹 사이트 호스팅 활성화
   - 호스팅 유형 : 정적 웹 사이트 호스팅
   - 인덱스 문서 : 원래 보여주고 싶은 html 파일
   - 오류 문서 : 오류 발생 시 보여주고 싶은 html 파일
4. 버킷에 등록된 객체(HTML)를 public 접근 가능하도록 변경
5. 버킷 웹 사이트 엔드포인트로 접근 확인



#### DNS 레코드에 Bucket 웹 사이트 엔드포인트 등록

- DNS 레코드
  - DNS 서버 명령
  - 도메인에 연계된 IP주소와 해당 도메인에 대한 요청의 처리 방법에 대한 정보를 제공
  - A 레코드 : 도메인의 IP 주소를 갖고 있는 레코드
- 버킷 웹 사이트 엔드포인트(http://cmcloudlab788.info.s3-website-us-east-1.amazonaws.com/)는 이용하기에 복잡하고 불편하다.



1. 레코드 추가
   - 레코드 이름의 오른쪽 칸에 .cmcloudlab788.info(강사님 예제) 입력
   - 값/트래픽 라우팅 대상
     - S3 웹 사이트 엔드포인트에 대한 별칭
     - 미국 동부(버지니아 북부)[us-east-1]
     - s3-website-us-east-1.amazonaws.com
2. 도메인으로 접속
   - cmcloudlab788.info 입력하여 접속 확인
3. www 추가
   - 현재는 www.cmcloudlab788.info 를 입력하면 연결이 안됨
   - 새로운 S3 Bucket 생성
     - 이름: www.cmcloudlab788.info
     - 퍼블릭 액세스 차단 해제
   - 정적 웹 사이트 호스팅 설정
     - 호스팅 유형 - 객체에 대한 요청 리디렉션
     - 호스트 이름 - cmcloudlab788.info
   - 버킷 웹 사이트 엔드포인트로 접속
     - http://www.cmcloudlab788.info.s3-website-us-east-1.amazonaws.com 로 접속
     - 기존의 cmcloudlab788.info 주소로 redirect 됨
4. 레코드 추가
   - 레코드 이름의 왼쪽 칸에 www 입력
   - 레코드 이름의 오른쪽 칸에 .cmcloudlab788.info(강사님 예제) 입력
   - 값/트래픽 라우팅 대상
     - S3 웹 사이트 엔드포인트에 대한 별칭
     - 미국 동부(버지니아 북부)[us-east-1]
     - s3-website-us-east-1.amazonaws.com
5. www.cmcloudlab788.info 접속 여부를 확인
   - 기존의 cmcloudlab788.info 주소로 redirect 됨