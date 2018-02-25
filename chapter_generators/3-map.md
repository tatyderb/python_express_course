## Функциональное программирование

**Функциональное программирование** — раздел дискретной математики и парадигма программирования, в которой процесс вычисления трактуется как вычисление значений функций в математическом понимании последних (в отличие от функций как подпрограмм в процедурном программировании).[wiki](https://ru.wikipedia.org/wiki/%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)

**Функция высшего порядка** — в программировании функция, принимающая в качестве аргументов другие функции или возвращающая другую функцию в качестве результата.

### map\(\) - применить функцию ко всем элементам списка

**map**\(_function_to_apply_, _iterable_, _...\) - применяет функцию _function_to_apply_ ко всем элементам последовательности _iterable_. Если заданы дополнительные аргументы (последовательности), то функция _function_to_apply_ должна принимать столько аргументов, сколько последовательностей переданно далее в map.

```python
a = map(int, input().split())  # 3 14 27 -1
```

Далее по полученному объекту типа map можно итерироваться.
```python
for x in a:
    print(x)
# 3 
# 14 
# 27 
# -1 
```

Еще о различиях map и list:
```python
>>> a = map(int, input().split())
3 14 27 -1                              # ввели эти числа
>>> a                                   # map - это не список
<map object at 0xffd87170>
>>> print(a)
<map object at 0xffd87170>
>>> b = list(a)                         # но из map можно получить list
>>> b
[3, 14, 27, -1]
>>> c = list(a)                       
>>> c                                   # итерироваться можно только ОДИН раз!!!
[]
```

#### map - пример: квадраты чисел

Посчитаем квадраты чисел, заданных в списке.

Обычная функция:
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

#### map - пример: задаем числа и их степени

Возведем числа из списка в степени, которые тоже заданы списком

Обычная функция:
```python
items = [10, 2, 3, 4]
n     = [ 3, 1, 2, 0]
res = []
for i, x in enumerate(items):
    res.append(x**n[i]))
```

map:
```python
items = [10, 2, 3, 4]
n     = [ 3, 1, 2, 0]
res = list(map((lambda x, i: x**i), items, n))
```

#### map - список входных данных может быть списком функций

```python
def multiply(x):
    return (x*x)
def add(x):
    return (x+x)

funcs = [multiply, add]
for i in range(5):
    value = list(map(lambda x: x(i), funcs))
    print(value)

# Вывод:
# [0, 0]
# [1, 2]
# [4, 4]
# [9, 6]
# [16, 8]
```

### filter\(\) - оставить те элементы, для которых True фильтрующая фукнция

**filter**\(_filter_function_, _list_of_inputs_\) - оставить только те элементы списка _list_of_inputs_, у которых применение функции _filter_function_ вернуло _True_.

```python
number_list = range(-5, 5)
less_than_zero = list(filter(lambda x: x < 0, number_list))
print(less_than_zero)

# Вывод: [-5, -4, -3, -2, -1]
```

**filer похож на цикл, но он является встроенной функцией и работает быстрее.**

### reduce\(\) - свертка списка с помощью функции

В Python 3 встроенной функции reduce() нет, но её можно найти в модуле _functools_.

**reduce**\(_function_to_apply_, _list_of_inputs_, _init_value_\) - сворачивает элементы списка _list_of_inputs_ в один объект, применяя _function_to_apply_ по очереди к последовательным парам элементов. Предполагая для первой пары _init_value_ - необязательный параметр.

Найдем произведение чисел из списка. 
Классический вариант:
```python
product = 1
list = [1, 2, 3, 4]
for num in list:
    product = product * num

# product = 24
```

С reduce:
```python
from functools import reduce
product = reduce((lambda res, x: res * x), [1, 2, 3, 4])    # 24
product = reduce((lambda res, x: res * x), [1, 2, 3, 4], 1) # эквивалентно
```

Порядок вычислений:
```python
(((2*3)*4)*5)*6
```

Цепочка вызовов связывается с помощью промежуточного результата (res). Если список пустой, просто используется третий параметр (в случае произведения нуля множителей это 1):
```python
reduce(lambda res, x: res*x, [], 1)    # 1
```

Реверс списка (если забыли про функцию _reversed_):
```python
>>> reduce(lambda res, x: [x]+res, [1, 2, 3, 4], [])
[4, 3, 2, 1]
```

### sum - сумма элементов списка

### all

**all**(iterable) - возвращает True если все элементы в iterable истины (или этот iterable пустой). 
То же самое, что:
```python
def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True
```

### any

**any**(iterable) - возвращает True если хоть один элемент в iterable истин (если этот iterable пустой, возвращается False). 
То же самое, что:
```python
def any(iterable):
    for element in iterable:
        if element:
            return True
    return False
```



