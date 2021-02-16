### Vagrant Commands



1. ```
   $ vagrant up
   ```

   - virtualbox의 운영체제 생성 후 동작시키기
   - 전원 off 되어있던 운영체제 on 시키기
   
2. ```
   $ vagrant status
   ```

   - vagrant 의 상태 표시
   
3. ```
   $ vagrant ssh
   ```

   - 운영체제 접속
   
4. ```
   $ vagrant halt
   ```

   - 운영체제 동작 중단

5. ```
   $ vagrant destroy
   ```

   - 운영체제 삭제

6. ```
   $ vagrant init
   ```

   - vagrant 시작

7. 특정 운영체제만 제어하기 위해서는 각 명령어의 뒷부분에 운영체제 이름을 입력하면 됨

8. ```
   $ vagrant reload
   ```

   - halt와 up을 동시에 함
   - Vagrantfile을 수정했을 때 이를 반영하여 새로운 운영체제를 생성할 수 있음

9. ```
   $ vagrant ssh-config name
   ```

   - name의 host, port number 등 각종 정보 확인

10. 
