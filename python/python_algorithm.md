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
  # ex
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

- 





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

- 