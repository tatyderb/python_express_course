# Вызов методов базового класса

Надо вызвать метод базового класса из метода, который переопределен в производном классе.

Из конструктора дочернего класса нужно _явно_ вызывать конструктор родительского класса.

Обращение к базовому классу происходит с помощью [**super()**](https://docs.python.org/3/library/functions.html#super)

## Нужно явно вызывать конструктор базового класса

```python
class A(object):
    def __init__(self, x=5):
        print('A.__init__')
        self.x = x
        
class B(A):
    def __init__(self, y=2):
        print('B.__init__')
        self.y = y

k = B(7)                    # B.__init__

print('k.y =', k.y)         # k.y = 7   
#print('k.x =', k.x)        # AttributeError: 'B' object has no attribute 'x'
```

Видно, что без явного вызова конструктора класса А не вызывается `A.__init__` и не создается поле x класса А.

Вызовем конструктор явно.

**Конструктор базового класса стоит вызывать раньше, чем иницилизировать поля класса-наследника**, потому что поля наследника могут зависеть (быть сделаны из) полей экземпляра базового класса.

```python
class A(object):
    def __init__(self, x=5):
        print('A.__init__')
        self.x = x
        
class B(A):
    def __init__(self, y=2):
        print('B.__init__')
        super().__init__(y/2)
        self.y = y

k = B(7)                    # B.__init__
                            # A.__init__
print('k.y =', k.y)         # k.y = 7   
print('k.x =', k.x)         # k.x = 3.5
```

## super() или прямое обращение к классу?

Метод класса можно вызвать, используя синтаксис вызова через имя класса:
```python
class Base(object):
    def __init__(self):
        print('Base.__init__')
        
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')

k = A()                     # Base.__init__
                            # A.__init__
```

Все работает. Но при дальнейшем развитии классов могут начаться проблемы:

```python
class Base(object):
    def __init__(self):
        print('Base.__init__')
        
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
        
class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')

class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')

x = C()                     # Base.__init__
                            # A.__init__
                            # Base.__init__ - второй вызов
                            # B.__init__
                            # C.__init__
```
Видно, что конструктор `Base.__init__` вызывается дважды. Иногда это недопустимо (считаем количество созданных экземпляров класса, увеличивая в конструкторе счетчик на 1; выдаем очередное auto id какому-то нашему объекту, например, номер пропуска или паспорта или номер заказа).

То же самое через super():
* вызов конструктора Base.\_\_init\_\_ происходит только 1 раз.
* вызваны конструкторы всех базовых классов.
* порядок вызова конструкторов для классов А и В не определен.

```python
class Base(object):
    def __init__(self):
        print('Base.__init__')
        
class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')
        
class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A, B):
    def __init__(self):
        super().__init__()
        print('C.__init__')

x = C()                     # Base.__init__
                            # B.__init__ - вызваны конструкторы обоих базовых классов
                            # A.__init__ - порядок вызова 
                            # C.__init__
```

Как это работает?

Рассмотрим method resolution order, который определен для каждого класса: `print(C.__mro__)`
Получим `(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>)`

Для реализации наследования питон ищет вызванный атрибут начиная с первого класса до последнего. Этот список создается слиянием (merge sort) списков базовых классов:
* дети проверяются раньше родителей.
* если родителей несколько, то проверяем в том порядке, в котором они перечислены.
* если подходят несколько классов, то выбираем первого родителя.

При вызове super() продолжается поиск, начиная со следующего имени в MRO. Пока каждый переопределенный метод вызывает super() и вызывает его только один раз, будет перебран весь список MRO и каждый метод будет вызван только один раз.

### Не забываем вызывать метод суперкласса

А если где-то не вызван метод суперкласса?
```python
class Base(object):
    def __init__(self):
        print('Base.__init__')
        
class A(Base):
    def __init__(self):
        #super().__init__()     - НЕ вызываем super()
        print('A.__init__')
        
class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A, B):
    def __init__(self):
        super().__init__()
        print('C.__init__')

x = C()                     # A.__init__
                            # C.__init__
                            
print(C.__mro__)
# (<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>)
```
Заметим, что хотя в `B.__init__` есть вызов super(), то до вызова `B.__init__` не доходит.

* Вызываем у объекта класса С метод \_\_init\_\_. 
* Ищем его в mro и находим С.\_\_init\_\_. Выполняем его.
* В этом методе вызов super() - ищем метод \_\_init\_\_ далее по списку от найденного. 
* Находим A.\_\_init\_\_. Выполняем его. В нем нет никаких super() - дальнейший поиск по mro прекращается.

### Нет метода в своем базовом классе, есть у родителя моего сиблинга

Определим класс, который пытается вызвать метод, которого нет в базовом классе:
```python
class A(object):
    def spam(self):
        print('A.spam')
        super().spam()

x = A()
x.spam()
```
получим, как и ожидалось:
```python
A.spam
Traceback (most recent call last):
  File "examples/oop_super_3.py", line 7, in <module>
    x.spam()
  File "examples/oop_super_3.py", line 4, in spam
    super().spam()
AttributeError: 'super' object has no attribute 'spam'
```

Определим метод spam в классе В. Класс С, наследник А и В, вызывает метод A.spam(), который вызывает B.spam - класс В не связан с классом А.

```python
class A(object):
    def spam(self):
        print('A.spam')
        super().spam()

class B(object):
    def spam(self):
        print('B.spam')
        
class C(A, B):
    pass

y = C()
y.spam()
print(C.__mro__)
```
получим:
```python
A.spam
B.spam
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>)
```
Для объекта класса С вызвали метод spam(). Ищем его в MRO. Находим A.spam() и вызываем. Далее для super() из A.spam() идем дальше от найденного по списку mro и находим B.spam().

Отметим, что при другом порядке описания родителей `class C(B, A)`, вызывается метод B.spam() у которого нет super():
```python
B.spam
(<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
```
Вызываем метод spam для объекта класса С. В С его нет, ищем дальше в В. Находим. Вызваем. Далее super() нет и дальнейший поиск не производится.

Чтобы не было таких сюрпризов при переопределении методов придерживайтесь правил:
* все методы в иерархии с одинаковым именем имеют одинаковую сигнатуру вызова (количество аргументов и их имена для именованных аргументов).
* реализуйте метод в самом базовом классе, чтобы цепочка вызовов закончилась хоть каким 

## Обращение к дедушке

### Игнорируем родителя

Если у нас есть 3 одинаковых метода foo(self) в наследуемых классах А, В(А), C(B), и нужно из C.foo() вызвать сразу A.foo() минуя B.foo(), то наши классы неправильно сконструированы (почему нужно игнорировать В? может, нужно было наследовать С от А, а не от В?). Нужен рефакторинг.

Но можно всегда вызвать метод по имени класса:
```python
class A(object):
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        
class C(B):
    def spam(self):
        A.spam(self)
        print('C.spam')

y = C()
y.spam()
print(C.__mro__)
```
получим 
```python
A.spam
C.spam
(<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
```

### Метод определен только у дедушки

Если в В такого метода нет, и из C.foo() нужно вызвать A.foo() (или в базовом классе выше по иерархии), вызываем super().foo() и больше не думаем, у какого пра-пра-пра-дедушки реализован этот метод.

Просто воспользуйтесь super() для поиска по mro.
```python
class A(object):
    def spam(self):
        print('A.spam')

class B(A):
    pass

class C(B):
    def spam(self):
        super().spam()
        print('C.spam')

y = C()
y.spam()
print(C.__mro__)
```
получим:
```python
A.spam
C.spam
(<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
```

### super().super() не работает

Или мы ищем какого-то родителя в mro, или точно указываем из какого класса нужно вызвать метод.

## Литература

* [Документация по python](https://docs.python.org/3/library/functions.html#super)
* [Python's super\(\) considered super!](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/)
* Python Cookbook, chapter 8.7 Calling a Method on a Parent Class