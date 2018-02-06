## �������������� ����������������

**�������������� ����������������** � ������ ���������� ���������� � ��������� ����������������, � ������� ������� ���������� ���������� ��� ���������� �������� ������� � �������������� ��������� ��������� (� ������� �� ������� ��� ����������� � ����������� ����������������).[wiki](https://ru.wikipedia.org/wiki/%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)

**������� ������� �������** � � ���������������� �������, ����������� � �������� ���������� ������ ������� ��� ������������ ������ ������� � �������� ����������.

### map\(\) - ��������� ������� �� ���� ��������� ������

**map**\(_function_to_apply_, _list_of_inputs_\) - ��������� ������� _function_to_apply_ �� ���� ��������� ������ _list_of_inputs_

```python
a = map(int, input().split())  # 3 14 27 -1
```

����� �� ����������� ������� ���� map ����� �������������.
```python
for x in a:
    print(x)
# 3 
# 14 
# 27 
# -1 
```

��� � ��������� map � list:
```python
>>> a = map(int, input().split())
3 14 27 -1                              # ����� ��� �����
>>> a                                   # map - ��� �� ������
<map object at 0xffd87170>
>>> print(a)
<map object at 0xffd87170>
>>> b = list(a)                         # �� �� map ����� �������� list
>>> b
[3, 14, 27, -1]
>>> c = list(a)                       
>>> c                                   # ������������� ����� ������ ���� ���!!!
[]
```

#### map - ������: �������� �����

��������� �������� �����, �������� � ������.

������� �������:
```python
items = [1, 2, 3, 4, 5]
squared = []
for i in items:
    squared.append(i**2)    
```

map:
```python
items = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, items))
```

#### map - ������ ������� ������ ����� ���� ������� �������

```python
def multiply(x):
    return (x*x)
def add(x):
    return (x+x)

funcs = [multiply, add]
for i in range(5):
    value = list(map(lambda x: x(i), funcs))
    print(value)

# �����:
# [0, 0]
# [1, 2]
# [4, 4]
# [9, 6]
# [16, 8]
```

### filter\(\) - �������� �� ��������, ��� ������� True ����������� �������

**filter**\(_filter_function_, _list_of_inputs_\) - �������� ������ �� �������� ������ _list_of_inputs_, � ������� ���������� ������� _filter_function_ ������� _True_.

```python
number_list = range(-5, 5)
less_than_zero = list(filter(lambda x: x < 0, number_list))
print(less_than_zero)

# �����: [-5, -4, -3, -2, -1]
```

**filer ����� �� ����, �� �� �������� ���������� �������� � �������� �������.**

### reduce\(\) - ������� ������ � ������� �������

� Python 3 ���������� ������� reduce() ���, �� � ����� ����� � ������ _functools_.

**reduce**\(_function_to_apply_, _list_of_inputs_, _init_value_\) - ����������� �������� ������ _list_of_inputs_ � ���� ������, �������� _function_to_apply_ �� ������� � ���������������� ����� ���������. ����������� ��� ������ ���� _init_value_ - �������������� ��������.

������ ������������ ����� �� ������. 
������������ �������:
```python
product = 1
list = [1, 2, 3, 4]
for num in list:
    product = product * num

# product = 24
```

� reduce:
```python
from functools import reduce
product = reduce((lambda res, x: res * x), [1, 2, 3, 4])    # 24
product = reduce((lambda res, x: res * x), [1, 2, 3, 4], 1) # ������������
```

������� ����������:
```python
(((2*3)*4)*5)*6
```

������� ������� ����������� � ������� �������������� ���������� (res). ���� ������ ������, ������ ������������ ������ �������� (� ������ ������������ ���� ���������� ��� 1):
```python
reduce(lambda res, x: res*x, [], 1)    # 1
```

������ ������ (���� ������ ��� ������� _reversed_):
```python
>>> reduce(lambda res, x: [x]+res, [1, 2, 3, 4], [])
[4, 3, 2, 1]
```

### sum - ����� ��������� ������
