# Обращение к элементу по индексу и итерации

## Доступ к элементам по индексу и извлечение срезов: \_\_getitem\_\_ и \_\_setitem\_\_

Класс возвращает квадрат значения индекса:
```python
>>> class Indexer:
...     def __getitem__(self, index):
...         return index ** 2
...
>>> X = Indexer()
>>> X[2]                     # Выражение X[i] вызывает X.__getitem__(i)
4
>>> for i in range(5):
...     print(X[i], end=' ') # Вызывает __getitem__(X, i) в каждой итерации
...
0 1 4 9 16
```
### Объект slice

При указании среза передается объект slice. 

`L = [5, 6, 7, 8, 9]`

| Срез | Объект slice | Результат |
|---|---|---|
| `L[2:4]` | `L[slice(2, 4)]` | `[7, 8]` |
| `L[1:]` | `L[slice(1, None)]` | `[6, 7, 8, 9]` |
| `L[:-1]` | `L[slice(None, -1)]` | `[5, 6, 7, 8]` |
| `L[::2]` | `L[slice(None, None, 2)]` | `[5, 7, 9]` |

```python
>>> class Indexer(object):
        data = [5, 6, 7, 8, 9]
        def __setitem__(self, index, value):    # Реализует присваивание
...                                             # по индексу или по срезу
            self.data[index] = value            # Приcваивание по индексу или по срезу
...     def __getitem__(self, index):           # Вызывается при индексировании или
...         print('getitem:', index)            # извлечении среза
...         return self.data[index]             # Выполняет индексирование
...                                             # или извлекает срез
>>> X = Indexer()
>>> X[0]                # При индексировании __getitem__ получает целое число
getitem: 0              
5
>>> X[1]
getitem: 1
6
>>> X[-1]
getitem: -1
9
>>> X[2:4]              # При извлечении среза __getitem__ получает объект среза
getitem: slice(2, 4, None)
[7, 8]
>>> X[1:]
getitem: slice(1, None, None)
[6, 7, 8, 9]
>>> X[:-1]
getitem: slice(None, -1, None)
[5, 6, 7, 8]
>>> X[::2]
getitem: slice(None, None, 2)
[5, 7, 9]
```

_До Python 3.0 были отдельные методы \_\_getslice\_\_, \_\_setslice\_\_. Сейчас вместо них используют \_\_getitem\_\_, \_\_setitem\_\_ (в них добавлена обработка объектов-срезов)_


## Преобразование в целое число \_\_index\_\_

Иногда объект могут использовать как индекс. Для работы такого синтаксиса переопределите \_\_index\_\_

```python
>>> class C:
...     def __index__(self):
...         return 255
...
>>> X = C()
>>> hex(X)          # Целочисленное значение
'0xff'
>>> bin(X)
'0b11111111'
>>> oct(X)
'0o377'
>>> ('C' * 256)[255]
'C'
>>> ('C' * 256)[X]  # X используется как индекс (не X[i])
'C'
>>> ('C' * 256)[X:] # X используется как индекс (не X[i:])
'C'
```

В Python 2.6 были отдельные методы \_\_hex\_\_ и \_\_oct\_\_.
 
## Итерация по индексам \_\_getitem\_\_

Операция **for** использует операцию индексирования к последовательности, где индексы от 0 и выше, пока не выйдет за границу последовательности (исключение, for его сам обработает).
То есть \_\_getitem\_\_ - один из способов реализовать перебор в for.

Что реализовано с использованием \_\_getitem\_\_:
* **for**
* **in**
* **map** (функция)
* генераторы списков (кортежей)
* присваивание списов (кортежей)

```python
>>> class stepper:
...     def __getitem__(self, i):
...         return self.data[i]
...
>>> X = stepper()       # X - это экземпляр класса stepper
>>> X.data = 'Spam'
>>>
>>> X[1]                # Индексирование, вызывается __getitem__
'p'
>>> for item in X:      # Циклы for вызывают __getitem__
...     print(item, end=' ')    # Инструкция for индексирует элементы 0..N
...
S p a m
>>> 'p' in X            # Во всех этих случаях вызывается __getitem__
True
>>> [c for c in X]      # Генератор списков
['S', 'p', 'a', 'm']
>>> list(map(str.upper, X)) # Функция map (в версии 3.0
['S', 'P', 'A', 'M']    # требуется использовать функцию list)
>>> (a, b, c, d) = X    # Присваивание последовательностей
>>> a, c, d
('S', 'a', 'm')
>>> list(X), tuple(X), ''.join(X)
(['S', 'p', 'a', 'm'], ('S', 'p', 'a', 'm'), 'Spam')
>>> X
<__main__.stepper instance at 0x00A8D5D0>
```

## Итераторы \_\_iter\_\_ и \_\_next\_\_

На самом деле, сначала пытается вызваться \_\_iter\_\_, а если его нет, то метод \_\_getitem\_\_

Как перебирается последовательность:
* вызывается iter(), которая вызывает \_\_iter\_\_() - возвращает объект итератора.
  * вызывается метод next(it) (который вызывает it.\_\_next\_\_()), пока не получим исключение StopIteration.
* иначе вызывается getitem(), пока не получим исключение IndexError.

## Можно определить свои итераторы

Можно определить итерацию по циклу (уже есть в `itertools.cycle`

```python
from itertools import cycle

li = [0, 1, 2, 3]

running = True
licycle = cycle(li)
while running:
    elem = next(licycle)
```

Можно возвращать квадраты индексов:
```python
class Squares:
    def __init__(self, start, stop): # Сохранить состояние при создании
        self.value = start - 1
        self.stop = stop
    def __iter__(self):             # Возвращает итератор в iter()
        return self
    def __next__(self):             # Возвращает квадрат в каждой итерации
        if self.value == self.stop: # Также вызывается функцией next
            raise StopIteration
        self.value += 1
        return self.value ** 2
```
использование:
```python
>>> from iters import Squares
>>> for i in Squares(1, 5):         # for вызывает iter(), который вызывает __iter__()
...     print(i, end=' ')           # на каждой итерации вызывается __next__()
...
1 4 9 16 25
>>> X = Squares(1, 5)               # Выполнение итераций вручную: эти действия выполняет
                                    # инструкция цикла
>>> I = iter(X)                     # iter вызовет __iter__
>>> next(I)                         # next вызовет __next__
1
>>> next(I)
4
...часть строк опущена...
>>> next(I)
25
>>> next(I)                         # Исключение можно перехватить с помощью инструкции try
StopIteration
```
Заметим, что реализация такого поведения через \_\_getitem\_\_ будет сложнее (индексы start..stop придется отображать на 0..stop-strart)

\_\_iter\_\_ предназначена для обхода **один раз**. \_\_getitem\_\_ - для множественного обращения к элементу.

Квадраты проще реализовать через написание генератора, а не через определение нового класса с итератором.
```python
>>> def gsquares(start, stop):
... for i in range(start, stop+1):
... yield i ** 2
...
>>> for i in gsquares(1, 5): # или: (x ** 2 for x in range(1, 5))
... print(i, end=' ')
...
1 4 9 16 25
>>> [x ** 2 for x in range(1, 6)]
[1, 4, 9, 16, 25]
```

## Несколько итераторов в одном объекте

В строках можно сделать несколько итераторов по одной и той же строке. Заметим, что они работают независимо:
```python
>>> S = ‘ace’
>>> for x in S:
... for y in S:
... print(x + y, end=’ ‘)
...
aa ac ae ca cc ce ea ec ee
```
* как внешний, так и внутренний цикл получает _свой_ итератор, вызывая `iter()`
* каждый итератор хранит свою информацию о положении в строке (не зависит от других циклов).

* Однократные проходы:
  * функции-генераторы и выражения-генераторы;
  * map, zip
* Многократные (независимые) проходы:
  * range
  * list, tuple и тп
  
**Для независимых итераторов \_\_iter\_\_() должен не просто возвращать self, а создавать новый объект со своей информацией о состоянии.**

```python
class SkipIterator:
    def __init__(self, wrapped):
        self.wrapped = wrapped              # Информация о состоянии
        self.offset = 0
    def next(self):
        if self.offset >= len(self.wrapped): # Завершить итерации
            raise StopIteration
        else:
            item = self.wrapped[self.offset] # Иначе перешагнуть и вернуть
            self.offset += 2
            return item
            
class SkipObject:
    def __init__(self, wrapped):            # Сохранить используемый элемент
        self.wrapped = wrapped
    def __iter__(self):
        return SkipIterator(self.wrapped)   # Каждый раз новый итератор

if __name__ == '__main__':
    alpha = 'abcdef'
    skipper = SkipObject(alpha)             # Создать объект-контейнер
    I = iter(skipper)                       # Создать итератор для него
    print(next(I), next(I), next(I))        # Обойти элементы 0, 2, 4
    for x in skipper:                       # for вызывает __iter__ автоматически
        for y in skipper:                   # Вложенные циклы for также вызывают __iter__
            print(x + y, end=' ')           # Каждый итератор помнит свое состояние, смещение
```
Напечатает:
```python
a c e
aa ac ae ca cc ce ea ec ee
```
Сравним с кодом, который использует уже существующие инструменты:
```python
>>> S = 'abcdef'
>>> S = S[::2]                              # Новый объект
>>> for x in S:
...     for y in S:
...         print(x + y, end=' ')
...
aa ac ae ca cc ce ea ec ee
```
* Код уже написан и отлажен (плюс).
* Создаются новые объекты (срезы), а не честная итерация в том же объекте (минус).

Где нужно писать такие множественные итераторы? Итерации по выборке из БД.
  
## Проверка на вхождение: \_\_contains\_\_, \_\_iter\_\_, \_\_getitem\_\_

Проверку на вхождение можно организовать через \_\_iter\_\_ или \_\_getitem\_\_, но лучше реализовать специальный метод \_\_contains\_\_.

Посмотрим, что когда вызывается (для этого сделаем класс на с хорошо итерируемыми данными, например, list):
```python
class Iters:
    def __init__(self, value):
        self.data = value
    def __getitem__(self, i):           # Крайний случай для итераций
        print('get[%s]:' % i, end='')   # А также для индексирования и срезов
        return self.data[i]
    def __iter__(self):                 # Предпочтительный для итераций
        print('iter=> ', end='')        # Возможен только 1 активный итератор
        self.ix = 0
        return self
    def __next__(self):
        print('next:', end='')
        if self.ix == len(self.data): 
            raise StopIteration
        item = self.data[self.ix]
        self.ix += 1
        return item
    def __contains__(self, x):          # Предпочтительный для оператора 'in'
        print('contains: ', end='')
        return x in self.data

X = Iters([1, 2, 3, 4, 5])      # Создать экземпляр
print(3 in X)                   # Проверка на вхождение
for i in X:                     # Циклы
    print(i, end=' | ')
print()
print([i ** 2 for i in X])      # Другие итерационные контексты
print( list(map(bin, X)) )
I = iter(X)                     # Обход вручную (именно так действуют
while True:                     # другие итерационные контексты)
    try:
        print(next(I), end=' @ ')
    except StopIteration:
        break
```
Напечатает:
```python
contains: True
iter=> next:1 | next:2 | next:3 | next:4 | next:5 | next:
iter=> next:next:next:next:next:next:[1, 4, 9, 16, 25]
iter=> next:next:next:next:next:next:[‘0b1’, ‘0b10’, ‘0b11’, ‘0b100’, ‘0b101’]
iter=> next:1 @ next:2 @ next:3 @ next:4 @ next:5 @ next:
```
Теперь закоментируем метод \_\_contains\_\_ и запустим код еще раз:
```python
iter=> next:next:next:True
iter=> next:1 | next:2 | next:3 | next:4 | next:5 | next:
iter=> next:next:next:next:next:next:[1, 4, 9, 16, 25]
iter=> next:next:next:next:next:next:[‘0b1’, ‘0b10’, ‘0b11’, ‘0b100’, ‘0b101’]
iter=> next:1 @ next:2 @ next:3 @ next:4 @ next:5 @ next:
```
Видим `iter=> next:next:next:True`, что проверка делается через \_\_iter\_\_.

Если закоментируем и \_\_contains\_\_, и \_\_iter\_\_, то будет вызываться \_\_getitem\_\_:
```python
get[0]:get[1]:get[2]:True
get[0]:1 | get[1]:2 | get[2]:3 | get[3]:4 | get[4]:5 | get[5]:
get[0]:get[1]:get[2]:get[3]:get[4]:get[5]:[1, 4, 9, 16, 25]
get[0]:get[1]:get[2]:get[3]:get[4]:get[5]:['0b1', '0b10', '0b11', '0b100','0b101']
get[0]:1 @ get[1]:2 @ get[2]:3 @ get[3]:4 @ get[4]:5 @ get[5]:
```
