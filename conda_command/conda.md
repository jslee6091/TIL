## conda commands

- anaconda 가상환경 목록

  `$ conda info --evns` 

- anaconda 가상환경 생성

  `$ conda create --name [가상환경이름]` 

- anaconda 가상환경 삭제

  `$ conda remove --name [가상환경이름] --all` 

- 가상환경 실행/종료

  ````
  $ conda activate [가상환경이름]
  $ conda deactivate
  ````

- 가상환경 내 포함된 라이브러리 목록

  ```
  $ conda list
  ```

- base 가상환경 

  ```
  별도의 가상환경을 만들지 않았을 경우 default로 존재하는 가상환경이다.
  ```

- 가상환경 만들때

  ```
  가상환경을 새로 만들면 라이브러리가 전혀 없는 상태이므로 새로 설치를 진행해야한다.
  anaconda에서 기본적으로 제공하는 여러 라이브러리들은 base 가상환경에만 존재하기 때문이다.
  ```

  

