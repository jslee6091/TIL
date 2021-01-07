# git command

> git 명령어 정리



### 설정

1. init
   - `git init` : 현재 폴더를 `git`으로 관리하는 명령어 -> `.git`폴더를 생성
   - 최초 한번만 실행

2. config
   - `git config --global user.email "email@email.com"`
   - `--global` 옵션과 `--local` 둘 중 하나 선택하여 사용
     - 일반적으로 global 설정을 해놓으면 내 컴퓨터에서 추가적으로 변경할 필요 없음

3. status
   - `git status`
   - 현재 git의 상태를 출력



4. diff
   - `git diff`
   - 마지막 commit과 현재 폴더 상태를 비교해서 차이점을 출력



5. log
   - `git log`
   - commit history를 출력



6. remote add
   - `git remote add origin <url>`
   - 원격저장소 주소 저장



### 저장

1. add
   - `git add <파일>`
     - `git add .` : 모든 파일과 폴더를 add
   - `working directory`에서 변경점을 `staging area`로 이동



2. commit
   - `git commit - m "메시지"` : 한번에 메시지 까지 남김



3. push
   - `git push origin master`
   - 원격저장소(github repository)에 파일 추가