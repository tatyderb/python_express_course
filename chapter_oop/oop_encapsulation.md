# Инкапсуляция

**В python НЕТ возможности полностью ограничить доступ к переменным объекта и класса**

Если вы изучали другие ООП-языки, то можете считать, что все поля в питоне public, а все методы virtual.

## Зачем нужна инкапсуляция

Пусть мы пишем класс `Circle` для хранения окружностей в плоскости ХУ.

Что будет, если кто-то установит отрицательный радиус?

Можно дописать функцию проверки корректности радиуса и добавить ее в код.

```python
class Circle:
    # конструктор класса, вызывается когда создаем новый объект класса
    def __init__(self, x=0, y=0, r=1):
         self.x = x                     # все переменные ОБЪЕКТА указываются в конструкторе
         self.y = y
         self.r = r
         
    def set_r(self, r):
        if r < 0:
            raise ValueError('radius is {}'.format(r))
        self.r = r
    
    # другие методы класса
```

Хочется заставить других программистов присваивать радиус только через функцию set_r.

## \_x - джентельменское соглашение (псевдочастные имена)

В питоне придерживаются неофициального соглашения, что переменные, начинающиеся с \_ не надо изменять вне класса. Они для внутреннего использования в классе.

Многие IDE не делают автодополнения вне класса на эти поля.

Но это просто договоренность. Вы можете использовать и изменять такие переменные где угодно.

## \_\_x - искажение

Если имя внутри конструкции `class` начинается с двух подчеркиваний \_\_ за счет имени того класса, в котором они определены. Например, в классе Circle переменная \_\_r не доступна вне класса по этому имени, но доступна по имени \_Circle\_\_r

```python
class Circle:
    # конструктор класса, вызывается когда создаем новый объект класса
    def __init__(self, x=0, y=0, r=1):
         self.x = x                     # полностью открытое имя переменной
         self._y = y                    # частично закрытое
         self.__r = r                   # "закрытое" имя
         
    def set_r(self, r):
        if r < 0:
            raise ValueError('radius is {}'.format(r))
        self.__r = r
    
    # другие методы класса
    
c = Circle(1, 2, 3)    
print(c.x)          # никак не ограничено
print(c._y)         # интерпретатор не ограничивает, коллеги осуждают
print(c.__r)        # нельзя, AttributeError
print(c._Circle__r) # можно, 3
```

В разделе "Подробнее об ООП" мы вернемся к этому примеру и рассмотрим как можно запретить добавление новых атрибутов и запись в уже существующие.

## Права доступа в стране розовых пони

Мы помним, что присваивание создавало переменные.
```python
x = 4   # если х не было, создать его
```

Аналогично присвоением можно экземпляру класса добавить атрибуты.

В питоне синтаксически можно написать так (но не нужно!!!):

```python
class A:    # в классе нет метода __init__ и атрибутов экземпляров класса.
    pass
    
a = A()     # a - ссылка на созданный объект класса А
a.x = 1     # добавили этому объекту поле x и присвоили ему 1

b = A()     # b - ссылка на другой созданный объект класса А
b.y = 2     # добавили этому объекту поле у и присвоили ему 2

print(a.x)  # 1
print(b.y)  # 2
print(a.y)  # AttributeError: 'A' object has no attribute 'y'

print(A.__dict__) # {'__module__': '__main__', '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}
print(a.__dict__) # {'x': 1}
print(b.__dict__) # {'y': 2}
```
Заметьте, атрибуты x и y принадлежат не экземплярам класса (всем), а х - одному экземпляру, y - другому экземпляру. Появление поля х в одном экземпляре класса не означает, что оно появится в другом.

Как такое создание атрибутов объекта может смутить программистов? Рассмотрим измененный пример кода с доступом к полю \_\_r.

```python
class Circle:
    # конструктор класса, вызывается когда создаем новый объект класса
    def __init__(self, x=0, y=0, r=1):
         self.x = x                     # полностью открытое имя переменной
         self._y = y                    # частично закрытое
         self.__r = r                   # "закрытое" имя
         
    def get_r(self):
        return self.__r
    
    # другие методы класса
    
c = Circle(1, 2, 3)  
print(c.__r)        # нельзя, AttributeError  
c.__r = 22          # МОЖНО??? Да, можно. Мы в одном объекте класса добавили атрибут  __r
print(c.__r)        # 22 (раньше получали AttributeError)
print(c._Circle__r) # можно, 3 (c._Circle__r правильное полное "внешнее" имя атрибута self.__r)
print(c.get_r())    # 3
```
Как мы видим, у объекта, на который ссылается переменная `c`, появился новый атрибут `c.\_\_r` равный 22. При этом атрибут `c._Circle\_\_r` остался недоступным и все еще равен 3.

Еще раз: **К атрибутам экземпляра класса, начинающихся с двойного подчеркивания, нельзя обратиться вне класса по этому имени. Полное имя атрибута \_имякласса\_\_имяатрибута**

# Копирование объектов

Зададим прямоугольник как координаты левой верхней точки, его ширину и высоту.
```python
>>> class Point():
>>>     def __init__(self, x=0, y=0):
>>>         self.x = x
>>>         self.y = y
>>> 
>>>     def __str__(self):
>>>         return '({}, {})'.format(self.x, self.y)        
>>> 
>>> class Rect():
>>>     def __init__(self, x=0, y=0, w=0, h=0):
>>>         self.lt = Point(x, y)
>>>         self.width = w
>>>         self.height = h
        
>>> import copy
>>> p1 = Point(1, 2)
>>> p2 = copy.copy(p1)
>>> print(p1)           # (1,2)
>>> print(p2)           # (1,2)
>>> p1 is p2            # это другой объект (копия)
False
>>> p1 == p2            # не переопределена операция __eq__ - по умолчанию == как is
False

>>> r1 = Rect(0, 0, 100, 200)
>>> r2 = copy.copy(r1)
>>> r1 is r2
False
>>> r1.lt is r2.lt
True

>>> r3 = copy.deepcopy(r1)
>>> r1 is r3
False
>>> r1.lt is r3.lt
False
```

TODO: Нарисовать диаграмму для r1 и r2 со ссылкой на общую точку, как в Downey, p 148.

https://docs.python.org/3.6/library/copy.html

* A **shallow copy** constructs a new compound object and then (to the extent possible) inserts references into it to the objects found in the original.
* A **deep copy** constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original.

Two problems often exist with deep copy operations that don’t exist with shallow copy operations:

* Recursive objects (compound objects that, directly or indirectly, contain a reference to themselves) may cause a recursive loop.
* Because deep copy copies everything it may copy too much, such as data which is intended to be shared between copies.
