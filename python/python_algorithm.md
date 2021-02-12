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



### Dictionary 

1. 모든 key 값 조회

   ```python
   dict.keys()
   # if idx in dict.keys() 구문으로 조회가 가능
   ```

2. 모든 value 값 조회

   ```python
   dict.values()
   # if idx in dict.values() 구문으로 조회가 가능
   ```





### Dictionary 정렬

> value로 정렬



- sorted(), items() 함수와 lambda 이용.

- 여러 개의 tuple로 이루어진 리스트가 반환된다.

- ```python
  dict_test = {'e': 1, 'w': 3, 'q': 7, 't': 2}
  tuple_test = sorted(dict_test.items(), key=lambda x:x[1])
  print(tuple_test)
  ```

- ```python
  # output - 오름차순
  [('e',1),('t',2),('w',3),('q',7)]
  ```

- ```python
  tuple2 = sorted(dict_test.items(), key=lambda x:x[1], reverse=True)
  print(tuple2)
  ```

- ```python
  # output - 내림차순
  [('q',7),('w',3),('t',2),('e',1)]
  ```



### 비어있는 리스트 만들기

- for문을 이용하여 num개의 공백 요소를 갖는 리스트 만들기

- ```python
  [[] for _ in range(num)]
  ```



### 연속된 숫자를 입력받아 리스트에 저장하기

- text file에 `12345` 가 저장되어있고 이를 입력받아 리스트에 저장하는 코드

- ```python
  list_ex = [list(map(int, list(input())))]
  ```

- text file에 다음과 같은 2차원 배열이 저장되어있고 이를 입력받아 2차원 리스트를 만드는 코드

- ```python
  # text file
  12345
  67890
  24679
  13578
  46891
  ```

- ```python
  list_2d_ex = [list(map(int, list(input()))) for _ in range(5)]
  ```



### 리스트의 특정 위치에 데이타 삽입

- python list의 *insert 함수*를 이용한다.

- ```python
  # insert(index, data)
  ```

- ```python
  test = [1,2,3,4,5]
  print(test)
  test.insert(3,55)
  print(test)
  ```

- ```python
  # output
  [1, 2, 3, 4, 5]
  [1, 2, 3, 55, 4, 5]
  ```





