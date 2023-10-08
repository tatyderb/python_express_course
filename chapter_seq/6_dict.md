# Словарь (dict)

## Зачем нужны словари?

Если есть список дней недели, то мы по _номеру_ дня недели быстро получаем название дня недели.

Хотим решить обратную задачу - по строке названия дня недели получать его номер. Хотим решать быстрее, чем index.

Нужно получить пары "название дня недели" - "номер дня недели".

## Термины

Словарь - неупорядоченная коллекция пар ключ-значение.

Неупорядоченная - значит порядок перебора не определен, нет понятие i-того элемента или среза.

Ключ - **хешируемый** объект. Ключи **Уникальные**.

Значение - любой объект.

## Создание словаря

Пустой словарь:
```python
d1 = dict()
d2 = {}     # это словарь, а не множество
```
Непустой словарь:
**dict(d)** - shallow copy словаря d.

```python
d1 = dict({"id": 1948, "name": "Washer", "size": 3})        # литерал словаря
d2 = dict(id=1948, name="Washer", size=3)                   # именованные аргументы
d3 = dict([("id", 1948), ("name", "Washer"), ("size", 3)])  # из последовательности
d4 = dict(zip(("id", "name", "size"), (1948, "Washer", 3))) # из последовательности
d5 = {"id": 1948, "name": "Washer", "size": 3}              # из литерала словаря
```

Словарь страна-столица:
```python
capitals = {'Russia': 'Moscow', 'Ukraine': 'Kiev', 'USA': 'Washington', 'Myanmar':'Naypyidaw', 'Mongolia':'Ulaanbaatar', 'China':'Beijing'}
capitals = dict(Russia = 'Moscow', Ukraine = 'Kiev', USA = 'Washington', )
capitals = dict([("Russia", "Moscow"), ("Ukraine", "Kiev"), ("USA", "Washington")])
capitals = dict(zip(["Russia", "Ukraine", "USA"], ["Moscow", "Kiev", "Washington"]))
```
Пишем красиво:
```python
capitals = {
    'Russia': 'Moscow', 
    'Ukraine': 'Kiev', 
    'USA': 'Washington', 
    'Myanmar':'Naypyidaw', 
    'Mongolia':'Ulaanbaatar', 
    'China':'Beijing'
}
```
**d.fromkeys(s, v)** - Возвращает словарь типа dict, ключами которого являются элементы последовательности s, а значениями либо None, либо v, если аргумент v определен.

```python
d = {}.fromkeys ("ABCD", 3) # d == {'A': 3, 'B': 3, 'C': 3, 'D': 3}
```

## dict comprehensions

```python
cities = ["Moscow", "Kiev", "Washington"]
states = ["Russia", "Ukraine", "USA"]
capitalsOfState = {state: city for city, state in zip(cties, states)}
```
Сделаем словарь квадратов натуральных чисел:
```python
square1 = {x : x*x for x in range(10) }                             # dict comprehensions 
square2 = {0=0, 1=1, 2=4, 3=9, 4=16, 5=25, 6=36, 7=49, 8=64, 9=81}  # задаем явно пары ключ=значение
```

Выворачиваем словарь "наоборот":
```python
>>> StateByCapital = {CapitalsOfState[state]: state for state in CapitalsOfState}
>>> stateByCapital
{'Kiev': 'Ukraine', 'Moscow': 'Russia', 'Washington': 'USA'}
```
и квадраты:
```python
sqrts = {square1[x]:x for x in square1}
```

Этот код будет работать чуть-чуть быстрее:
```python
sqrts2 = {v:k for k,v in square1.items()}
```

if тоже поддерживается:
```python
file_sizes = {name: os.path.getsize(name) for name in os.listdir(".") if os.path.isfile(name)}
```

## Методы словаря

| Операция | Значение |
|--|---|
| value = A\[key\] | Получение элемента по ключу. Если элемента с заданным ключом в словаре нет, то возникает исключение KeyError |
| value = A.get(key) | Получение элемента по ключу. Если элемента в словаре нет, то get возвращает None. |
| value = A.get(key, *default_value*) | То же, но вместо None метод get возвращает default_value. |
| key in A | Проверить принадлежность ключа словарю. |
| key not in A | То же, что not key in A. |
| A\[key\] = value | Добавление нового элемента в словарь или изменяет старое значение на value |
| len(A) | Возвращает количество пар ключ-значение, хранящихся в словаре. |
| A.keys() | Возвращает список ключей |
| A.values() | Возвращает список значений (порядок в нем такой же, как для списка ключей) |
| A.items() | Возвращает список пар ключ, значение |

```python
d = {}.fromkeys ("ABCD", 3) # d == {'A': 3, 'B': 3, 'C': 3, 'D': 3}
s = set("ACX")              # s == {'A', 'C', 'X'}
matches = d.keys() & s      # matches == {'A', 'C'}
```

Методы **keys(), values(), items()** возвращают _представления_ словарей.

_Представление_ - это итерируемый объект +
* если представляемый объект изменяется, представление будет отражать эти изменения;
* поддерживает операции над множествами;

Пусть v - представление словаря, а x - множество или представление словаря. Определены операции:
```python
v & x # Пересечение
v | x # Объединение
v - x # Разность
v ^ x # XOR
```

| Операция | Значение |
|--|---|
| del A\[key\] | Удаление пары ключ-значение с ключом key. Возбуждает исключение KeyError, если такого ключа нет. |
| value = A.pop(key) | Удаление пары ключ-значение с ключом key и возврат значения удаляемого элемента. Если такого ключа нет, то возбуждается KeyError. |
| value = A.pop(key, default_value) | То же, но вместо генерации исключения возвращается default_value. |
| A.pop(key, None) | Это позволяет проще всего организовать безопасное удаление элемента из словаря. |

### Удаление ключа с проверкой

```python
if key in A:
    del A[key]
```
### Удаление ключа с перехватом исключения
```python
try:
    del A[key]
except KeyError:
    pass
```

## Перебор словаря

**При переборе словаря порядок ключей и пар может быть любой. Порядок может измениться со временем (а может остаться прежним).**

```python
In [12]: capital = {'Russia': 'Moscow', 'Ukraine': 'Kiev', 'USA': 'Washington',
    ...:  'Myanmar':'Naypyidaw', 'Mongolia':'Ulaanbaatar', 'China':'Beijing'}

In [13]: capital
Out[13]:
{'China': 'Beijing',
 'Mongolia': 'Ulaanbaatar',
 'Myanmar': 'Naypyidaw',
 'Russia': 'Moscow',
 'USA': 'Washington',
 'Ukraine': 'Kiev'}
```
по ключам (перебор словаря идет неявно по ключам):
```python
In [14]: for s in capital:
    ...:     print(s, capital[s])
    ...:
China Beijing
Mongolia Ulaanbaatar
Ukraine Kiev
Russia Moscow
USA Washington
Myanmar Naypyidaw
```
явно по ключам:
```python
In [15]: for s in capital.keys():
    ...:     print(s, capital[s])
China Beijing
Mongolia Ulaanbaatar
Ukraine Kiev
Russia Moscow
USA Washington
Myanmar Naypyidaw
```
отсортировать ключи:
```python
In [18]: for s in sorted(capital.keys()):
    ...:     print(s, capital[s])
China Beijing
Mongolia Ulaanbaatar
Myanmar Naypyidaw
Russia Moscow
USA Washington
Ukraine Kiev
```
только значения:
```python
In [19]: for c in capital.values():
    ...:     print(c)
    ...:
Beijing
Ulaanbaatar
Kiev
Moscow
Washington
Naypyidaw
```
Значения тоже можно отсортировать.

Если нам в цикле будет нужен и ключ, и значение, лучше перебирать по парам:

```python
In [20]: for s, c in capital.items():
    ...:     print(s, c)
China Beijing
Mongolia Ulaanbaatar
Ukraine Kiev
Russia Moscow
USA Washington
Myanmar Naypyidaw
```
Пары тоже можно отсортировать:
```python
In [21]: for s, c in sorted(capital.items()):
    ...:     print(s, c)
China Beijing
Mongolia Ulaanbaatar
Myanmar Naypyidaw
Russia Moscow
USA Washington
Ukraine Kiev
```
В обратном порядке reverse=True:
```python
In [22]: for s, c in sorted(capital.items(), reverse=True):
    ...:     print(s, c)
Ukraine Kiev
USA Washington
Russia Moscow
Myanmar Naypyidaw
Mongolia Ulaanbaatar
China Beijing
```

## defaultdict

Даны пары город и страна. Нужно построить словарь страна: список городов. 

```python
from collections import defaultdict

colours = (
    ('Yasoob', 'Yellow'),
    ('Ali', 'Blue'),
    ('Arham', 'Green'),
    ('Ali', 'Black'),
    ('Yasoob', 'Red'),
    ('Ahmed', 'Silver'),
)

favourite_colours = defaultdict(list)

for name, colour in colours:
    favourite_colours[name].append(colour)

print(favourite_colours)

# Вывод:
# defaultdict(<type 'list'>,
#    {'Arham': ['Green'],
#     'Yasoob': ['Yellow', 'Red'],
#     'Ahmed': ['Silver'],
#     'Ali': ['Blue', 'Black']
# })
```

Другим популярным случаем использования defaultdict является добавление элементов в список внутри словаря. Если ключ не существует в словаре, то вы упрётесь в KeyError. defaultdict позволяет обойти эту проблему аккуратным образом. Для начала, позвольте привести пример использования dict с исключением KeyError, а затем мы посмотрим на пример с defaultdict.

Ошибка:
```python
some_dict = {}
some_dict['colours']['favourite'] = "yellow"
# Вызывает KeyError: 'colours'
```
Решение:
```python
import collections
tree = lambda: collections.defaultdict(tree)
some_dict = tree()
some_dict['colours']['favourite'] = "yellow"
# Работает без ошибок
```