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

3. Key를 이용하여 value 값 조회

   ```python
   # Key가 'item'인 경우 해당하는 Value 반환
   # 'item'인 Key가 없는 경우 None 반환
   dict.get('item')
   # 'item'인 Key가 없는 경우 None 대신 0을 반환
   dict.get('item', 0)
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
  # 또는
list_ex = [list(map(int, input()))]
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
  # 또는
  list_2d_ex = [list(map(int, input())) for _ in range(5)]
  ```

- ```python
  # output
  [[1,2,3,4,5],[6,7,8,9,0],[2,4,6,7,9],[1,3,5,7,8],[4,6,8,9,1]]
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



### 리스트의 원소들을 괄호 없이 출력

- `*`사용

- ```python
  # ex1
  a = [1,2,3,4,5]
  print(a)
  print(*a)
  ```

- ```python
  # output
  [1,2,3,4,5]
  1 2 3 4 5
  ```
  
  
  
- asterisk는 print에서 변수 하나만 입력이 가능하다. 즉, 다음과 같은 문장은 SyntaxError가 발생한다.

- ```python
  # ex2
  a = [1,2,3,4,5]
  print(f'#{test_case} {*a}')
  b = *a
  print(b)
  ```

- ```python
  # output
  SyntaxError: cannot use starred expression here
  -> 두 print 문 모두 Syntax Error 발생
  ```

- 결론적으로 asterisk 는 변수 삽입이 불가하고 print 안에서 다른 변수와 함께 출력이 되는 것도 불가능하다.



### 여러 타입의 원소들을 한 리스트에 입력 받기

> 문자열, 정수 등이 혼합된 리스트

- `input().split()`만을 사용하여 간단히 구현 가능

- ```python
  # ex
  # input.txt 파일 
  I 5 7
  
  # python code
  a = input().split()
  print[a]
  ```

- ```python
  # output
  ['I','5','7']
  ```

- 문자열, 정수 여부 관계없이 무조건 문자열 타입으로 리스트에 저장됨





### 리스트에서 원하는 인덱스의 데이터 삭제

> 원하는 위치의 데이터 삭제하기

- `del` 활용

- 특정 위치의 데이터 삭제 후 뒤의 데이터들이 한칸씩 앞으로 당겨진다.

- ```python
  # ex 1
  a = [1,2,3,4,5]
  print(a)
  del a[3]
  print(a)
  ```

- ```python
  # output
  [1,2,3,4,5]
  [1,2,3,5]
  ```

- 리스트 슬라이싱을 활용하여 한번에 여러 개의 데이터를 삭제할 수 있다.

- ```python
  # ex 2
  a = [1,2,3,4,5]
  print(a)
  del a[1:3] # 인덱스 1,2의 원소가 삭제됨
  print(a)
  ```

- ```python
  # output
  [1,2,3,4,5]
  [1,4,5]
  ```

- 




### 정수 문자열을 리스트로 변환

> 정수를 원소로 하는 리스트

- list()와 map() 활용

- ```python
  # ex
  a = "100"
  print(a, type(a))
  
  b = list(map(int, list(a)))
  print(b, type(b[0]))
  ```

- ```python
  # output
  100 <class 'str'>
  [1,0,0] <class 'int'>
  ```

- 만약 a = "011"인 경우에는 [0,1,1]로 변환된다.





### 순열(permutation)과 문자열

> 길이가 n인 문자열 중 n이하의 개수를 뽑는 순열



- 직접 구현하는 방법도 있지만 코드의 길이가 매우 길다.

- 따라서 itertools 모듈의 permutations 함수를 사용하면 된다.

- ```python
  from itertools import permutations
  
  a = "102"
  b = permutations(a, 2)
  c = list(b)
  print('b is ', b)
  print('c is ', c)
  for j in c:
      d = ''.join(j)
      print(d)
  ```

- ```python
  # output
  b is  <itertools.permutations object at 0x000001BD1C773770>
  c is  [('1', '0'), ('1', '2'), ('0', '1'), ('0', '2'), ('2', '1'), ('2', '0')]
  10
  12
  01
  02
  21
  20
  
  ```

- ```python
  a = [2,3]
  b = list(permutations(a))
  print(b)
  ```

- ```python
  # output
  [(2,3), (3,2)]
  ```





### 문자열이 포함된 리스트 거꾸로 뒤집기

- reversed()와 list() 이용

- ```python
  # ex1 - string
  a = 'hello'
  b = list(reversed(a))
  print(b)
  ```

- ```python
  # output
  ['o', 'l', 'l', 'e', 'h']
  ```

- ```python
  # ex2 - list
  a = ['h', 'e', 'l', 'l', 'o']
  b = list(reversed(a))
  print(b)
  ```

- ```python
  # output
  ['o', 'l', 'l', 'e', 'h']
  ```

- ```python
  # ex3 - list() 안했을 때
  a = 'hello'
  b = reversed(a)
  print(b)
  ```

- ```python
  # output
  <reversed object at 0x00000223317D1220>
  ```






### 리스트에 특정값이 있는지 확인

- `if element in list` 활용

- ```python
  # ex
  a = [1,2,3,4,5]
  if 3 in a:
      print('yes')
  else:
      print('no')
  
  if 7 in a:
      print('yes')
  else:
      print('no')
  ```

- ```python
  # output
  yes
  no
  ```






### 2차원 리스트 정렬

> 특정 원소를 기준으로 오름차순 또는 내림차순 정렬

- ```python
  a = [[20, 23], [17, 20], [23, 24], [4, 14], [8, 18]]
  # 첫번째 원소를 기준으로 오름차순 정렬
  a.sort(key=lambda x:x[0])
  print(a)
  ```

- ```python
  # output
  [[4, 14], [8, 18], [17, 20], [20, 23], [23, 24]]
  ```

- ```python
  # 첫번째 원소를 기준으로 내림차순 정렬
  a.sort(key=lambda x:-x[0])
  print(a)
  ```

- ```python
  # output
  [[23, 24], [20, 23], [17, 20], [8, 18], [4, 14]]
  ```

- ```python
  # 첫번째 원소가 같을 때는 두번째 원소를 이용해 정렬할 수 있다.
  # 두번째 원소로 정렬을 하지 않으면 정렬이 되지 않은 상태이다.
  b = [[18, 19], [2, 7], [11, 15], [13, 16], [23, 24], [2, 14], [13, 22], [20, 23], [13, 19], [7, 15], [5, 21], [20, 24], [16, 22], [17, 21], [9, 24]]
  b.sort(key=lambda x:x[0])
  ```

- ```python
  # output
  [[2, 7], [2, 14], [5, 21], [7, 15], [9, 24], [11, 15], [13, 16], [13, 22], [13, 19], [16, 22], [17, 21], [18, 19], [20, 23], [20, 24], [23, 24]]
  ```

- ```python
  # 첫번째 원소가 같을 시 두번째 원소를 기준으로 오름차순 정렬
  b.sort(key=lambda x:(x[0], x[1]))
  ```

- ```python
  # output
  [[2, 7], [2, 14], [5, 21], [7, 15], [9, 24], [11, 15], [13, 16], [13, 19], [13, 22], [16, 22], [17, 21], [18, 19], [20, 23], [20, 24], [23, 24]]
  ```

- ```python
  # 첫번째 원소가 같을 시 두번째 원소를 기준으로 내림차순 정렬
  b.sort(key=lambda x:(x[0], -x[1]))
  ```

- ```python
  # output
  [[2, 14], [2, 7], [5, 21], [7, 15], [9, 24], [11, 15], [13, 22], [13, 19], [13, 16], [16, 22], [17, 21], [18, 19], [20, 24], [20, 23], [23, 24]]
  ```






### Deque

> Queue와 Stack의 혼합형태



- 자료의 앞, 뒤 양쪽 방향에서 element를 추가하거나 삭제할 수 있는 자료구조

- Queue와 Stack에 사용되는 List에 비해 훨씬 빠르다.

  - List : O(n)
  - Deque : O(1)

- 간단한 사용법

  - ```python
    from collections import deque
    
    deque.append(item) # item을 오른쪽에서 삽입
    deque.appendleft(item) # item을 왼쪽에서 삽입
    deque.pop() # 가장 오른쪽 요소를 제거 후 가져옴
    deque.popleft() # 가장 왼쪽 요소를 제거 후 가져옴
    deque.extend(array) # array를 오른쪽에 추가
    deque.extendleft(array) # array를 왼쪽에 추가
    deque.remove(item) # item을 제거
    deque.rotate(num) # deque를 num 만큼 회전 (num이 양수면 오른쪽, 음수면 왼쪽)
    ```



### 리스트 내 문자열 정렬

- `sorted()` 또는 `sort()` 이용

- ```python
  a = ['ae', 'bx', 'tl', 'cpoi', 'xwtd', 'dx', 'dzd', 'dfg']
  a.sort(key=lambda x: x)
  print(a)
  ```

- ```
  # output
  ['ae', 'bx', 'cpoi', 'dfg', 'dx', 'dzd', 'tl', 'xwtd']
  ```

- 비교하려는 자리의 문자가 같은 경우 그 다음 자리의 문자를 비교하여 정렬한다.





### 리스트 원소의 중복 없애기

- `set` 이용

- ```python
  a = [1,2,3,4,5,5,5,3]
  print(a)
  ```

- ```
  [1, 2, 3, 4, 5, 5, 5, 3]
  ```

- ```
  b = set(a)
  print(b, type(b))
  ```

- ```
  {1, 2, 3, 4, 5} <class 'set'>
  ```

- ```
  c = list(b)
  print(c, type(c))
  ```

- ```
  [1, 2, 3, 4, 5] <class 'list'>
  ```



