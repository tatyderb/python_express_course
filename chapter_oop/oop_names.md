# Имена и области видимости

## Дерево атрибутов

* атрибуты экземпляра - создаются `self.атрибут =` в методах;
* атрибуты класса - создаются `атрибут =` внутри инструкции class;
* ссылки на суперклассы - перечисление при наследовании.

Поиск по дереву атрибутов - при любом обращении к атрибуту (даже при `self.атрибут`)

![](/assets/attribute_tree.png)

## Функции при наследовании

Так как поиск атрибутов идет снизу вверх, то в подклассе можно:
* _заместить_ атрибут суперкласса;
* _предоставить_ атрибут суперкласса;
* _расширить_ методы суперкласса за счет их вызова из метода подкласса.

Расширение:
```python
>>> class Super:
... 	def method(self):
... 		print('in Super.method')
...
>>> class Sub(Super):
... 	def method(self):           		# Переопределить метод
... 		print('starting Sub.method')	# Дополнительное действие
... 		Super.method(self)          	# Выполнить действие по умолчанию
... 		print(ending Sub.method')
```

## Взаимодействие классов при наследовании

Файл примера specialize.py

* _Super_ - имеет методы _method_ и _delegate_ (он хочет метод _action_ в наследнике).
* _Inheritor_ - ничего своего, все только наследует от _Super_.
* _Replacer_ - переопределяет _Super.method_ своей собственной версией.
* _Extender_ - переопределяет _Super.method_ так, что вызывает и его, для выполнения действий по умолчанию.
* _Provider_ - реализует метод _action_, который ожидается метдом _Super.delegate_

```python
class Super:
    def method(self):
        print('in Super.method')    # Поведение по умолчанию
    def delegate(self):
        self.action()               # Ожидаемый метод

class Inheritor(Super):             # Наследует методы, как они есть
    pass

class Replacer(Super):              # Полностью замещает method
    def method(self):
        print('in Replacer.method')

class Extender(Super):              # Расширяет поведение метода method
    def method(self):
        print('starting Extender.method')
        Super.method(self)
        print('ending Extender.method')

class Provider(Super):              # Определяет необходимый метод
    def action(self):
        print('in Provider.action')

if __name__ == '__main__':
    for myclass in (Inheritor, Replacer, Extender):
        print('\n' + myclass.__name__ + '...')
        myclass().method()
    print('\nProvider...')
    x = Provider()
    x.delegate()
```
Напечатает:
```python
Inheritor...
in Super.method

Replacer...
in Replacer.method

Extender...
starting Extender.method
in Super.method
ending Extender.method

Provider...
in Provider.action
```

## Абстрактные суперклассы

Когда класс _Provider_ вызывается метод `delegate`, начинаются **две** независимых процедуры поиска.

* первый вариант:
  * при вызове `x.delegate()` интерпретатор ищет метод, начиная от класса _Provider_ вверх по дереву наследования.
  * Экземпляр `x` передается в виде аргумента self.
  
* внутри метода `Super.delegate` выражение `self.action` запускает новый независимый поиск в дереве наследования, начиная от экземпляра self и далее вверх по дереву. Но _self_ ссылается на экземпляр класса _Provider_, метод `action` будет найден в подклассе _Provider_.

**Абстрактный суперкласс** - класс, который ожидает, что часть его функционала будет реализована его детьми.

Хороший тон: сделать "абстрактность" неработоспособной, возбуждая `NotImplementedError` или написав `assert` (проверяет логическое выражение, если истина, идет дальше, если ложь, то останавливает выполнение с сообщением об ошибке):
```python
class Super:
    def delegate(self):
        self.action()
    def action(self):
		assert False, 'action must be defined!' # При вызове этой версии
    
>>> X = Super()
>>> X.delegate()
AssertionError: action must be defined!
```
или через возбуждение исключения

```python
class Super:
    def delegate(self):
        self.action()
    def action(self):
        raise NotImplementedError('action must be defined!')
        
>>> X = Super()
>>> X.delegate()
NotImplementedError: action must be defined!
```
Если наследник не реализует метод, то мы получим исключение и у него:
```python
>>> class Sub(Super): pass
...
>>> X = Sub()
>>> X.delegate()
NotImplementedError: action must be defined!
```
до тех пор, пока не реализуем: 
```python
>>> class Sub(Super):
... 	def action(self): print('Реализация тут')
...
>>> X = Sub()
>>> X.delegate()
Реализация тут
```

## Абстрактные суперклассы в питоне 2.6 и 3.0

Абстрактный суперкласс можно определить с помощью специальных синтаксических конструкций. Они разные в питоне 2.6 и 3.0

Эти конструкции **запретят создавать экземпляры, если методы не будут определены в дереве ниже**.

Python 3.0 (подробнее разберем позже):
```python
from abc import ABCMeta, abstractmethod
class Super(metaclass=ABCMeta):
    @abstractmethod
    def method(self, ...):
        pass
```

Python 2.6:
```python
class Super:
    __metaclass__ = ABCMeta
    @abstractmethod
    def method(self, ...):
        pass
```

Чтобы запретить это для методов _delegate_ и _action_, напишем эту конструкцию для питона 3.0:
```python
>>> from abc import ABCMeta, abstractmethod
>>>
>>> class Super(metaclass=ABCMeta):
...     def delegate(self):
...         self.action()
...     @abstractmethod
...     def action(self):
...         pass

>>> X = Super()
TypeError: Can’t instantiate abstract class Super with abstract methods action
>>> class Sub(Super): pass
...
>>> X = Sub()
TypeError: Can’t instantiate abstract class Sub with abstract methods action
>>> class Sub(Super):
... def action(self): print('Реализация тут')
...
>>> X = Sub()
>>> X.delegate()
Реализация тут
```

Плюс: получаем ошибку раньше - при **создании экземпляра класса**, а не при попытке вызвать у экземпляра метод, которого нет.

Минус: увеличение кода.

О декораторах функций (@abstractmethod) и объявлении метаклассов расскажем потом.

# Пространство имен

* **Неквалифицированные имена** (например, Х) располагаются в областях видимости (namespace).
* **Квалифицированные имена атрибутов** (например, object.X) принадлежат простанствам имен объектов.
* Некоторые области видимости инициализируют пространства имен объектов (в модулях и классах)

## Простые имена - глобальные, пока нет =

Правило нахождения имени LEGB.

* **Присваивание** (X = value) - делает имена локальными, создает или изменяет имя X в текущей локальной области видимости, если имя не объявлено глобальным

* **Ссылка** (X) - пытается отыскать имя Х по правилу LEGB.

## Имена атрибутов: пространства имен объектов

Квалифицированные имена атрибутов ссылаются на атрибуты конкретных объектов и к ним применяются правила, предназначенные для модулей и классов. Для объектов классов и экземпляров эти правила дополняются включением процедуры поиска в дереве наследования:

* **Присваивание** (object.X = value)
Создает или изменяет атрибут с именем X в пространстве имен объекта object, и ничего больше. 

Восхождение по дереву наследования происходит только при попытке получить ссылку на атрибут, но не при выполнении операции присваивания.

* **Ссылка** (object.X)
Для объектов, созданных на основе классов, поиск атрибута X производится сначала в объекте object, затем во всех классах, расположенных выше в дереве наследования. В случае объектов, которые создаются не из классов, таких как модули, атрибут X извлекается непосредственно из объекта object.

## Классификация имен происходит при =.

mynames.py:
```python
X = 11 # Глобальное (в модуле) имя/атрибут (X, или manynames.X)

def f():
    print(X) # Обращение к глобальному имени X (11)

def g():
    X = 22 # Локальная (в функции) переменная (X, скрывает имя X в модуле)
    print(X)
    
class C:
    X = 33 # Атрибут класса (C.X)
    def m(self):
        X = 44 # Локальная переменная в методе (X)
        self.X = 55 # Атрибут экземпляра (instance.X)    

if __name__ == '__main__':
    print(X)        # 11: модуль (за пределами файла manynames.X)
    f()             # 11: глобальная
    g()             # 22: локальная
    print(X)        # 11: переменная модуля не изменилась
    obj = C()       # Создать экземпляр
    print(obj.X)    # 33: переменная класса, унаследованная экземпляром
    obj.m()         # Присоединить атрибут X к экземпляру
    print(obj.X)    # 55: экземпляр
    print(C.X)      # 33: класс (она же obj.X, если в экземпляре нет X)
    #print(C.m.X)   # ОШИБКА: видима только в методе
    #print(g.X)     # ОШИБКА: видима только в функции
```

Теперь в другом файле:
```python
# otherfile.py
import manynames
X = 66
print(X)            # 66: здешняя глобальная переменная
print(manynames.X)  # 11: глобальная, ставшая атрибутом в результате импорта
manynames.f()       # 11: X в manynames, не здешняя глобальная!
manynames.g()       # 22: локальная в функции, в другом файле
print(manynames.C.X) # 33: атрибут класса в другом модуле
I = manynames.C()
print(I.X)          # 33: все еще атрибут класса
I.m()
print(I.X)          # 55: а теперь атрибут экземпляра!
```

Добавим global и nonlocal:
```python
X = 11              # Глобальная в модуле
def g1():
    print(X)        # Ссылка на глобальную переменную в модуле
def g2():
    global X
    X = 22          # Изменит глобальную переменную в модуле
def h1():
    X = 33          # Локальная в функции
    def nested():
        print(X)    # Ссылка на локальную переменную в объемлющей функции
def h2():
    X = 33          # Локальная в функции
    def nested():
        nonlocal X  # Инструкция из Python 3.0
        X = 44      # Изменит локальную переменную в объемлющей функции
```

**Старайтесь не писать одинаковые имена в разных областях (контекстах)**

# Словари пространств имен (исследуем какие есть имена)

Пространства имен реализованы как словари и доступны по встроенному атрибуту **\_\_dict\_\_**

Аналогично объекты классов и экземпляров: обращение к квалифицированному имени - это операция доступа к элементу словаря.

```python
>>> class super:
...     def hello(self):
...         self.data1 = 'spam'
...
>>> class sub(super):
...     def hola(self):
...         self.data2 = 'eggs'
...
```

* экземпляры по атрибуту **\_\_class\_\_** получают ссылку на класс;
* класс по атрибуту **\_\_bases\_\_** получает кортеж со ссылками на суперклассы.

```python
>>> X = sub()
>>> X.__dict__              # Словарь пространства имен экземпляра
{}
>>> X.__class__             # Класс экземпляра
<class '__main__.sub'>
>>> sub.__bases__           # Суперклассы данного класса
(<class '__main__.super'>,)
>>> super.__bases__         # В Python 2.6 возвращает пустой кортеж ()
(<class 'object'>,)
```

Исследуем экземпляр подкласса:
```python
>>> Y = sub()
>>> X.hello()
>>> X.__dict__
{'data1': 'spam'}
>>> X.hola()
>>> X.__dict__
{'data1': 'spam', 'data2': 'eggs'}
>>> sub.__dict__.keys()
['__module__', '__doc__', 'hola']
>>> super.__dict__.keys()
['__dict__', '__module__', '__weakref__', 'hello', '__doc__'>]
>>> Y.__dict__              # до сих пор пустой!!!
{}
```

Имена с \_\_ определяются автоматически.

Можно доступиться к атрибуту по квалифицированному имени или индексироваться по ключу:
```python
>>> X.data1, X.__dict__['data1']
('spam', 'spam')
>>> X.data3 = 'toast'
>>> X.__dict__
{'data1': 'spam', 'data3': 'toast', 'data2': 'eggs'}
>>> X.__dict__['data3'] = 'ham'
>>> X.data3
'ham'
```
Заметим, что унаследованный атрибут X.hello недоступен через `X.__dict__['hello']`

Функция **dir(object)** напоминает вызов **object.__dict__.keys()**, но:
* _dir_ - сортирует свой список и включает в него системные атрибуты.
* собирает унаследованные атрибуты (с версии 2.2)
* вместе с атрибутами класса _object_

```python
>>> X.__dict__, Y.__dict__
{ ({'data1': 'spam', 'data3': 'ham', 'data2': 'eggs'}, {})
>>> list(X.__dict__.keys())         # Необходимо в Python 3.0
['data1', 'data3', 'data2']
                                    # В Python 2.6
>>> dir(X)
['__doc__', '__module__', 'data1', 'data2', 'data3', 'hello', 'hola']
>>> dir(sub)
['__doc__', '__module__', 'hello', 'hola']
>>> dir(super)
['__doc__', '__module__', 'hello']
                                    # В Python 3.0:
>>> dir(X)
['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__',
...часть строк опущена...
'data1', 'data2', 'data3', 'hello', 'hola']
>>> dir(sub)
['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__',
...часть строк опущена...
'hello', 'hola']
>>> dir(super)
['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__',
...часть строк опущена...
'hello'
]
```

## Строки документации (docstring)

Написаны в тройных кавычках.

Автоматически сохраняются интерпретатором в их объектах.

Сделаем блоки документации:
```python
"""I am: docstr.__doc__"""
def func(args):
    """I am: docstr.func.__doc__"""
    pass
class spam:
    """I am: spam.__doc__ or docstr.spam.__doc__"""
    def method(self, arg):
        """I am: spam.method.__doc__ or self.method.__doc__"""
        pass
```

Доступ к объектам docstr:
```python
>>> import docstr
>>> docstr.__doc__
'I am: docstr.__doc__'
>>> docstr.func.__doc__
'I am: docstr.func.__doc__'
>>> docstr.spam.__doc__
'I am: spam.__doc__ or docstr.spam.__doc__'
>>> docstr.spam.method.__doc__
'I am: spam.method.__doc__ or self.method.__doc__'
```

Сделаем из строк документации help:
```python
>>> help(docstr)
Help on module docstr:
NAME
    docstr - I am: docstr.__doc__
FILE
    c:\misc\docstr.py
CLASSES
    spam
    class spam
    | I am: spam.__doc__ or docstr.spam.__doc__
    |
    | Methods defined here:
    |
    | method(self, arg)
    |   I am: spam.method.__doc__ or self.method.__doc__
FUNCTIONS
    func(args)
        I am: docstr.func.__doc__
```

## Классы и модули

* Модули
  * Это пакеты данных и исполняемого кода.
  * Создаются как файлы с программным кодом на языке Python или как расширения на языке C.
  * Задействуются операцией import.
* Классы
  * Реализуют новые объекты.
  * Создаются с помощью инструкции class.
  * Задействуются операцией вызова.
  *  Всегда располагаются внутри модуля.
Кроме того, классы поддерживают дополнительные возможности, недоступные в модулях, такие как перегрузка операторов, создание множества экземпляров и наследование. Несмотря на то что и классы, и модули являются пространствами имен, между ними есть различия.


# Встроенные атрибуты класса

https://www.tutorialspoint.com/python/python_classes_objects.htm

* \_\_dict\_\_ - Dictionary containing the class's namespace.
* \_\_doc\_\_ - Class documentation string or none, if undefined.
* \_\_name\_\_ - Class name.
* \_\_module\_\_ - Module name in which the class is defined. This attribute is "\_\_main\_\_" in interactive mode.
* \_\_bases\_\_ - A possibly empty tuple containing the base classes, in the order of their occurrence in the base class list.

```python
#!/usr/bin/python

class Employee:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self):
     print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary

print "Employee.__doc__:", Employee.__doc__
print "Employee.__name__:", Employee.__name__
print "Employee.__module__:", Employee.__module__
print "Employee.__bases__:", Employee.__bases__
print "Employee.__dict__:", Employee.__dict__
```
Получаем:
```
Employee.__doc__: Common base class for all employees
Employee.__name__: Employee
Employee.__module__: __main__
Employee.__bases__: ()
Employee.__dict__: {'__module__': '__main__', 'displayCount':
<function displayCount at 0xb7c84994>, 'empCount': 2, 
'displayEmployee': <function displayEmployee at 0xb7c8441c>, 
'__doc__': 'Common base class for all employees', 
'__init__': <function __init__ at 0xb7c846bc>}
```
