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
     - `git log --oneline` 
     - 가장 최근의 log만 출력



6. remote
   
   - `git remote -v`
   - 현재 디렉터리와 연결된 github repository 주소 확인
   - `git remote add origin <url>`
   - 원격저장소 주소 저장
   - `git remote set-url origin <url>`
   - 원격저장소 주소 변경
   - `git remote remove origin`
   - 원격저장소 연결 삭제



7. branch
   - `git branch name`
   - name 이름의 새로운 branch 생성



8. branch 변경
   - `git checkout branch_name`
   - branch_name인 branch로 변경함



9. branch 조회
   - `git branch`
   - 현재 생성되어있는 branch 목록 조회



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



4. clone
   - `git clone email@email.com` 
   - email주소의 repository를 그대로 복사함



5. pull
   - `git pull origin master` 
   - github의 repository의 최신 정보를 업데이트함



### 협업

1. 충돌
   - 개발 현업에서는 다른 사람들과 깃허브 소스코드를 공유하며 협업을 하게 된다.
   - 이때 동시에 같은 소스를 수정하는 과정에서 충돌(conflict) 가 발생할 수 있다.
2. 충돌 해결
   - 충돌을 해결하기 위해서는 우선 본인의 브랜치에 소스를 push 한다.
   - Github 원격저장소에 가서 pull request를 만든다. 이때 자신의 브랜치를 메인 브랜치와 코드를 합치도록 설정한다.
   - merge를 위해 코드를 변경한다.
   - 충돌이 해결되었으면 마무리된다.
3. 주의사항
   - 원격저장소의 메인 브랜치 코드가 변경되었을때 이를 pull 받기 위해서는 우선 본인이 로컬에서 변경한 코드를 자신의 브랜치에 먼저 올려야한다.
   - 그렇지 않고 pull을 받으면 자신이 변경한 코드를 전부 잃어버리게 된다.
   - 항상 원격저장소의 최신 코드를 로컬에 pull 받아놓도록 하는 것이 좋다.



### Whitespace Error

- ```
  warning: LF will be replaced by CRLF in 디렉터리내 파일명
  solution: git config --global core.autocrlf true (--global은 선택사항)을 입력
  ```

- Mac 또는 Linux를 쓰는 개발자와 Windows를  쓰는 개발자가 Git으로 협업할때 발생한다.

- Unix 시스템에서는 한 줄의 끝이 LF(Line Feed) 로 이루어지고 Windows에서는 줄 하나가  CRUF로 이루어져 있기 때문이다. 

- 이를 해결하기 위해 `core.autocrlf`을 true로 만들어주면 된다.

- CRUF = CR(Carriage Return), LF(Line Feed)





### Github 저장소에 새로운 branch 만들기

1. 로컬에서 branch를 새로 만든다.

   - ```
     $ git branch my_branch
     ```

2. 새로 만든 브랜치로 변경한다.

   - ```
     $ git checkout -b my_branch
     ```

3. add, commit 한다.

   - ```
     $ git add .
     ```

   - ```
     $ git commit -m "message"
     ```

4. branch 에 push 한다.

   - ```
     $ git push origin my_branch
     ```

   - upstream branch가 없다는 오류가 발생할 때는 `--set-upstream` 옵션을 추가해야한다.

   - ```
     $ git push --set-upstream origin my_branch
     ```

   - 보통 처음 push 할때 이런 오류가 발생한다.