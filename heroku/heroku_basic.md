### heroku 시작

> command 참고 URL : https://devcenter.heroku.com/articles/git



1. github에 heroku를 위한 repository 하나 생성

   - 아무 파일도 없는 상태

   

2. 로컬에 디렉터리 하나 만들고 생성한 repository 주소를 clone함

   

3. clone하여 생성된 디렉터리로 들어가서 npm init 입력

   ```
   $ npm init
   ```

   

4. ```
   $ npm install express --save
   ```

   

5. heroku 사이트에서 먼저 생성한 github repository 주소를 연결함

   

6. ```
   $ heroku login
   ```

   

7. heroku 내의 app 확인

   - ```
     $ heroku list
     ```

   

8. ```
   $ heroku git:remote app_name
   ```

   - app_name은 list 명령어로 확인한 app 이름

   

9. ```
   $ code. 입력 후 app.js 생성(json 파일이랑 같은 디렉토리)(app 이름 다르게 해도 됨)
   ```

   

10. `app.js` 소스코드 만들고 github에 저장

    - ```
      $ git add .
      $ git commit -m "comment"
      $ git push
      ```

    

11. heroku 사이트에서 manual deploy 클릭하면 됨

    - automatic deploy 기능도 있으나 manual deploy가 더 익숙함.
    - command도 있는데 잘 모르겠음 - 현재 알아보고 있는 중

    

12. 결과 확인은 다음 URL에서 확인할 수 있다.

    - ```
      app_name.herokuapp.com
      ```

    - 스마트폰에서도 같은 주소로 접속 가능하다.

