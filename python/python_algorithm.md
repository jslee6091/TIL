### 리스트를 문자열로 변환

- join() 함수를 이용

- ```python
  list = ['e','t','u','j','g']
  str_list = "".join(list)
  print(str_list)
  ```

- ```python
  # output
  etujg
  ```

- ```python
  # 쉼표로 구분할 경우
  str_list2 = ",".join(list)
  print(str_list2)
  ```

- ```python
  # output
  e,t,u,j,g
  ```



### 2차원 리스트 회전

- zip() 과 unpacking 을 이용

- unpacking에는 asterisk(*) 으로 한다.

- ```python
  list = [['e','d','s','v','x'],['y','j','k','l','o'],['p','g','b','h','t']]
  for var in zip(*list):
      print(var)
  ```

- ```python
  # output
  (e,y,p)
  (d,j,g)
  (s,k,b)
  (v,l,h)
  (x,o,t)
  ```

- ```python
  # zip은 tuple을 반환하므로 list로 변환 후 2차원 리스트 생성
  new_list = []
  for var in zip(*list):
      new_list.append(list(var))
  ```

- ```python
  # output
  [['e','y','p'],['d','j','g'],['s','k','b'],['v','l','h'],['x','o','t']]
  ```





