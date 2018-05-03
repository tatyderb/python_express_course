# Связанные и несвязанные методы

**Несвязанные методы _класса_** - это методы без аргумента _self_.

При обращении к функциональному атрибуту класса через имя класса получаем объект несвязанного метода. Для вызова метода нужно передать экземпляр класса в первый аргумент (_self_).

**Связанные методы _экземпляра_** - пара _self_ + функция.

Попытка обращения к функциональному атрибуту класса через имя экземпляра возвращает объект связанного метода. Интерпретатор автоматически упаковывает экземпляр с функцией в объект связанного метода, поэтому вам не требуется передавать экземпляр в вызов такого метода.

И несвязанные методы класса, и связанные методы экземпляра - объекты (так же, как числа и строки) и могут передаваться в виде аргументов (так же как числа или строки). При запуске оба требуют экземпляр в первом аргументе (self). 

При вызове связанного метода интерпретатор автоматически подставляет первым аргументом экземпляр, который использовался для создания объекта связанного метода.

```python
class Spam:
    def doit(self, message):
        print(message)
        
object1 = Spam()
object1.doit('hello world')
```
На самом деле создается **объект связанного метода** `object1.doit`, в который упакованы вместе экземпляр `object1` и метод `Spam.doit`.

Можно присвоить этот объект переменной и использовать переменную для вызова, как простую функцию:
```python
x = object1.doit    # Объект связанного метода: экземпляр+функция
x('hello world')    # То же, что и object1.doit('...')
```

Вызовем метод через имя класса:
```python
object1 = Spam()
t = Spam.doit       # Объект несвязанного метода
t(object1, 'howdy') # Передать экземпляр в первый аргумент
```

**self.method** - это объект связанного метода экземпляра, так как _self_ - объект экземпляра.

```python
class Eggs:
    def m1(self, n):
        print(n)
    def m2(self):
        x = self.m1     # Еще один объект связанного метода
        x(42)           # Выглядит как обычная функция

Eggs().m2()             # Выведет 42
```

## В Python 3 несвязанные методы - это функции

В Python 3 можно в классе создавать методы без аргумента self и не писать декоратор @staticmethod.

```python
class A(object):
    def __init__(self, x):
        self.x = x
        
    def __str__(self):
        return str(self.x)
        
    @staticmethod
    def new_A(s):
        t = A(int(s))
        return t
        
    @staticmethod
    def common_foo(x, k):
        return x * k
        
    def a_foo(self, k):
        self.x = __class__.common_foo(self.x, k)
        
    def func_foo(x, k):
        return x * k

    def a_func_foo(self, k):
        self.x = __class__.func_foo(self.x, k)
        
a1 = A(1)
print('a1 =', a1)

a2 = A.new_A("2")
print('a2 =', a2)

z = A.common_foo(3, 4)
print('z =', z)

a1.a_foo(5)
print('a1 =', a1)

z = A.func_foo(3, 4)
print('z =', z)

a1.a_func_foo(5)
print('a1 =', a1)
```
 
Использование декоратора @staticmethod повышает читаемость кода.

## Связанные методы и другие вызываемые объекты

Связанные методы экземпляра класса - это объекты, которые хранят и экземпляр, и метод. Их можно использовать как обычные функции:

```python
>>> class Number:
... def __init__(self, base):
...     self.base = base
... def double(self):
...     return self.base * 2
... def triple(self):
...     return self.base * 3
...
>>> x = Number(2)   # Объекты экземпляров класса
>>> y = Number(3)   # Атрибуты + методы
>>> z = Number(4)
>>> x.double()      # Обычный непосредственный вызов
4
>>> acts = [x.double, y.double, y.triple, z.double] # Список связанных методов
>>> for act in acts:                                # Вызовы откладываются
...     print(act())                                # Вызов как функции
...
4
6
9
8
```

Можно посмотреть на атрибуты, которые дают доступ к объекту экземпляра и к методу:
```python
>>> bound = x.double
>>> bound.__self__, bound.__func__
(<__main__.Number object at 0x0278F610>, <function double at 0x027A4ED0>)
>>> bound.__self__.base
2
>>> bound() # Вызовет bound.__func__(bound.__self__, ...)
4
```
Можно обрабатывать одинаково:
* функции, определенные через def или lambda;
* экземпляры, наследующие метод \_\_call\_\_;
* связанные методы экземпляров.

```python
>>> def square(arg):
...     return arg ** 2 # Простые функции (def или lambda)
...
>>> class Sum:
...     def __init__(self, val): # Вызываемые экземпляры
...         self.val = val
...     def __call__(self, arg):
...         return self.val + arg
...
>>> class Product:
...     def __init__(self, val): # Связанные методы
...         self.val = val
...     def method(self, arg):
...         return self.val * arg
...
>>> sobject = Sum(2)
>>> pobject = Product(3)
>>> actions = [square, sobject, pobject.method] # Функция, экземпляр, метод
>>> for act in actions:                         # Все 3 вызываются одинаково
...     print(act(5))                           # Вызов любого вызываемого
...                                             # объекта с 1 аргументом
25
7
15
>>> actions[-1](5)                              # Индексы, генераторы, отображения
15
>>> [act(5) for act in actions]
[25, 7, 15]
>>> list(map(lambda act: act(5), actions))
[25, 7, 15]
```

Класс - тоже вызываемый объект. Но он вызывается для создания экземпляра:
```python
>>> class Negate:
...     def __init__(self, val):    # Классы - тоже вызываемые объекты
...         self.val = -val         # Но вызываются для создания объектов
...     def __repr__(self):         # Реализует вывод экземпляра
...         return str(self.val)
...
>>> actions = [square, sobject, pobject.method, Negate] # Вызвать класс тоже можно
>>> for act in actions:
...     print(act(5))
...
25
7
15
-5
>>> [act(5) for act in actions]     # Вызовет __repr__, а не __str__!
[25, 7, 15, -5]
```
Посмотрим, какие это объекты:
```python
>>> table = {act(5): act for act in actions}    # генератор словарей
>>> for (key, value) in table.items():
...     print('{0:2} => {1}'.format(key, value))
...
-5 => <class '__main__.Negate'>
25 => <function square at 0x025D4978>
15 => <bound method Product.method of <__main__.Product object at 0x025D0F90>>
7 => <__main__.Sum object at 0x025D0F70>
```

## Связанные методы и callback

Пример использования связанных методов - GUI на tkinter.

Везде, где можно использовать функцию, можно использовать связанный метод.

Можно написать через функцию (или лямбда-выражение):
```python
def handler():
...     сохраняет информацию о состоянии в глобальных переменных...
...
widget = Button(text='spam', command=handler)
```

Можно использовать связанный метод:
```python
class MyWidget:
    def handler(self):
...     сохраняет информацию о состоянии в self.attr...
    def makewidgets(self):
        b = Button(text='spam', command=self.handler)
```
self.handler - объект связанного метода. В нем хранятся self и MyWidget.handler. Так как self ссылается на оригинальный экземпляр, то потом, когда метод handler будет вызван для обработки событий, у него будет доступ к экземпляру и его атрибутам (где можно хранить информацию о состоянии объекта между событиями).

Еще один вариант хранения информации между событиями - переопределение метода \_\_call\_\_ (см. перегрузку операторов).


