# Декораторы

Декораторы - это функции, которые изменяют работу других функций. Это делает код короче.

Рассмотрим где их можно использовать и как написать свой декоратор.

## Источники

* [Intermediate python](https://lancelote.gitbooks.io/intermediate-python/content/book/decorators.html)
* [Python Decorator Library](https://wiki.python.org/moin/PythonDecoratorLibrary)

* Лутц, Изучаем Python. глава 38. Декораторы
* [Python3 Patterns, Recipes and Idioms](http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html)

Пакеты с декорататорами, используемые в заданиях:
* [attrs](https://github.com/python-attrs/attrs) - attrs is the Python package that will bring back the joy of writing classes by relieving you from the drudgery of implementing object protocols
* [Contracts](https://github.com/AndreaCensi/contracts) - проверка аргументов функций и возвращаемых значений; [документация](http://andreacensi.github.io/contracts/)
* [numba](http://numba.pydata.org/numba-doc/dev/index.html) и [User manual](http://numba.pydata.org/numba-doc/dev/user/index.html) - Numba is a compiler for Python array and numerical functions that gives you the power to speed up your applications with high performance functions written directly in Python.


## Для чего нужны декораторы

* декораторы функций - управляют не только вызовами функций, но и объектами функций (могут, например, зарегистрировать функции в каком-то прикладном интерфейсе).
* декораторы классов - не только управляет вызовами классов для создания экземпляров класса, но и может изменять объект класса (например, добавить методы), в этом декораторы аналогичны метаклассам.

Плюсы декораторов:
* очевидный синтаксис; они более заметны, чем вызов вспомогательных функций, которые могут быть далеко по тексту кода от функций и классов, к которым они применяются.
* применяются к функции или классу только один раз, когда они определяются, не надо писать дополнительный программный код при каждом их вызове.

Недостатки (любой обертывающей логики):
* изменяют типы декорируемых объектов;
* порождают дополнительные вызовы функций;


## Вспоминаем работу с функциями

Чтобы понять как работают декораторы, напишем свой декоратор.

Для этого вспомним некоторые идеи питона.

### Функции являются объектами

Функция - это тоже объект. Ее можно присваивать переменной. Вызывать функции можно по имени этой переменной.

```python
def hi(name="yasoob"):
    return "Привет " + name

print(hi())
# Вывод: 'Привет yasoob'

# Мы можем присвоить функцию переменной:
greet = hi
# Мы не используем здесь скобки, поскольку наша задача не вызвать функцию,
# а передать её объект переменной. Теперь попробуем запустить

print(greet())
# Вывод: 'Привет yasoob'

# Посмотрим что произойдет, если мы удалим ссылку на оригинальную функцию
del hi
print(hi())
# Вывод: NameError

print(greet())
# Вывод: 'Привет yasoob'
```

### Функции внутри функции

В питоне можно определить функцию внутри функции. Ее можно будет вызвать внутри объемлющей функции. Но нельзя напрямую вызвать вне объемлющей функции.

```python
def hi(name="yasoob"):
    print("Вы внутри функции hi()")

    def greet():
        return "Вы внутри функции greet()"

    def welcome():
        return "Вы внутри функции welcome()"

    print(greet())
    print(welcome())
    print("Вы внутри функции hi()")

hi()
# Вывод: 
# Вы внутри функции hi()
# Вы внутри функции greet()
# Вы внутри функции welcome()
# Вы внутри функции hi()

# Пример демонстрирует, что при вызове hi() вызываются также функции
# greet() и welcome(). Кроме того, две последние функции недоступны
# извне hi():

greet()
# Вывод: NameError: name 'greet' is not defined
```

Видим, что нельзя снаружи объемлющей функции напрямую вызывать вложенную функцию. Но вложенную функцию можно вернуть и потом вызывать из любого места:

### Возвращаем функцию из функции

Заметьте, внутри функции hi вложенные функции greet и welcome НЕ вызываются. Они только возвращаются. Вызываются они в других местах (куда функции вернули).

```python
def hi(name="yasoob"):
    def greet():
        return "Вы внутри функции greet()"

    def welcome():
        return "Вы внутри функции welcome()"

    if name == "yasoob":
        return greet
    else:
        return welcome

a = hi()
print(a)
# Вывод: <function greet at 0x7f2143c01500>

# Это наглядно демонстрирует, что переменная 'a' теперь указывает на
# функцию greet() в функции hi(). Теперь попробуйте вот это

print(a())
# Вывод: Вы внутри функции greet()
```
Обратите внимание: greet - ссылка на фукнцию, greet() - вызов функции. Скобки имеют значение.

Из функции возвращаются объекты функций greet и welcome. 

`hi()` - это вызов функции. Она исполняется и возвращается ссылка на greet. 

При вызове `hi(name=ali)` вызовется функции hi и возвратит ссылку на функцию welcome.

Чтобы вызвать ту функцию, которую вернули, можно вызвать `hi()()` - напечатает "Мы внутри greet".

Функцию можно передать аргументом другой функции:
```python
def hi():
    return "Привет yasoob!"

def doSomethingBeforeHi(func):
    print("BEFORE hi()")
    print(func())

doSomethingBeforeHi(hi)

# Вывод: 
# BEFORE hi()
# Привет yasoob!
```

Декораторы позволяют исполнять код до и после вызова функции

## Пишем декоратор

Мы уже по сути написали декоратор. Добавим в него еще действия после вызова функции.

```python
def a_new_decorator(a_func):

    def wrapTheFunction():
        print("BEFORE a_func()")

        a_func()

        print("AFTER a_func()")

    return wrapTheFunction

def a_function_requiring_decoration():
    print("Я функция, которая требует декорации")

a_function_requiring_decoration()
# Вывод: "Я функция, которая требует декорации"

a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
# Теперь функция a_function_requiring_decoration обернута в wrapTheFunction()

a_function_requiring_decoration()

# Вывод: 
# BEFORE a_func()
# Я функция, которая требует декорации
# AFTER a_func()
```

Мы обернули вызов нашей функции.

По сути, есть только переменные (глобальные и разных сортов локальные) и вызов функций (в т.ч. compile). Есть замыкания (если функция объявляется внутри другой, то из внутренней функции доступны не только свои локальные переменные, но и локальные переменные внешней)

wrapTheFunction - не функция, а локальная переменная для a_new_decorator
При каждом вызове a_new_decorator внутри первой строкой вызывается compile, результат которого записывается в локальную переменную wrapTheFunction. 
Этот compile, среди прочего, запоминает значение a_func.
Вот этот compile и возвращается.

Декоратор можно написать через синтаксис с @.

Выражение @a_new_decorator это сокращенная версия следующего кода:
```python
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
```
Пример через @.
```python
@a_new_decorator
def a_function_requiring_decoration():
    """Эй ты! Задекорируй меня полностью!"""
    print("Я функция, которая требует декорации")

a_function_requiring_decoration()
# Вывод: 
# BEFORE a_func()
# Я функция, которая требует декорации
# AFTER a_func()

# Выражение @a_new_decorator это сокращенная версия следующего кода:
# a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
```

Но у нас перестало работать \_\_name\_\_ так, как мы хотим (печатать имя вот этой самой функции):
```python
print(a_function_requiring_decoration.__name__)     # wrapTheFunction, хотим a_function_requiring_decoration
```

Наша функция a_function_requiring_decoration была заменена на wrapTheFunction. Она перезаписала имя и строку документации оригинальной функции. Это можно исправить, используя **functools.wrap**:

```python
from functools import wraps

def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("BEFORE a_func()")
        a_func()
        print("AFTER a_func()")
    return wrapTheFunction

@a_new_decorator
def a_function_requiring_decoration():
    """Эй ты! Задекорируй меня полностью!"""
    print("Я функция, которая требует декорации")

print(a_function_requiring_decoration.__name__)
# Вывод: a_function_requiring_decoration
``` 
### Как сделать декоратор

Примечание: @wraps принимает на вход функцию для декорирования и добавляет функциональность копирования имени, строки документации, списка аргументов и т.д. Это открывает доступ к свойствам декорируемой функции из декоратора.

```python
from functools import wraps
def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Функция не будет исполнена"
        return f(*args, **kwargs)
    return decorated

@decorator_name
def func():
    return("Функция исполняется")

can_run = True
print(func())
# Вывод: Функция исполняется

can_run = False
print(func())
# Вывод: Функция не будет исполнена
```

## Использования декораторов

### Авторизация

Декораторы могут использоваться в веб-приложениях для проверки авторизации пользователя, перед тем как открывать ему доступ к функционалу. Они активно используются в веб-фреймворках Flask и Django. Вот пример проверки авторизации на декораторах:

```python
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
    return decorated
```

### Логирование

```python
from functools import wraps

def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " была исполнена")
        return func(*args, **kwargs)
    return with_logging

@logit
def addition_func(x):
    """Считаем что-нибудь"""
    return x + x


result = addition_func(4)
# Вывод: addition_func была исполнена
```

## Декораторы с аргументами

Является ли @wraps декоратором или она обычная функция, которая может принимать аргументы? 

Когда используется синтаксис @my_decorator, мы применяем декорирующую функцию с аргументом в виде декорируемой функции. В Python все является объектом, в том числе и функци. Можно написать функции, возвращающие декорирующие функции.


### Вложенные декораторы внутри функций

Добавим к примеру с логером аргумент в виде файла, куда мы будем логировать:

```python
from functools import wraps

def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " была исполнена"
            print(log_string)
            # Открываем логфайл и записваем данные
            with open(logfile, 'a') as opened_file:
                # Мы записываем логи в конкретный файл
                opened_file.write(log_string + '\n')
        return wrapped_function
    return logging_decorator

@logit()
def myfunc1():
    pass

myfunc1()
# Вывод: myfunc1 была исполнена
# Файл out.log создан и содержит строку выше

@logit(logfile='func2.log')
def myfunc2():
    pass

myfunc2()
# Вывод: myfunc2 была исполнена
# Файл func2.log создан и содержит строку выше
```

## Декораторы классов

Пусть наш лог-декоратор находится на продакшене и теперь мы хотим, кроме регулярной записи в лог-файл, иметь возможность экстренного уведомления по емейл в случае ошибок.

Звучит как повод написать класс-наследник, но мы до этого работали с декораторами функций. Они связывали имена функций с другим вызываемым объектом на этапе определения фукнции. 

Посмортрим на декораторы классов, которые будут связывать имя класса с другим вызываемым объектом на этапе его пределения.

```python
class logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        log_string = func.__name__ + " была исполнена"
        print(log_string)
        # Открываем логфайл и записваем данные
        with open(self.logfile, 'a') as opened_file:
            # Мы записываем логи в конкретный файл
            opened_file.write(log_string + '\n')
        # Отправляем сообщение
        self.notify()

    def notify(self):
        # Только записываем логи
        pass
```
Такое решение имеет дополнительно преимущество в краткости, в сравнении с вложенными функциями, при этом синтаксис декорирования функции остается прежним:
```python
@logit()
def myfunc1():
    pass
```
Расширим класс logit, чтобы notify мог посылать емейл:
```python
class email_logit(logit):
    """
    Реализация logit для отправки писем администраторам при вызове
    функции
    """
    def __init__(self, email='admin@myproject.com', *args, **kwargs):
        self.email = email
        super(email_logit, self).__init__(*args, **kwargs)

    def notify(self):
        # Отправляем письмо в self.email
        # Реализация не будет здесь приведена
        pass
```

@email_logit будет работать также как и @logit, при этом отправляя сообщения на почту администратору помимо журналирования.

# Еще о декораторах 

**Управление функцией сразу после ее создания**:
```python
def decorator(F):
    # Обработка функции F
    return F

@decorator
def func(): ...         # func = decorator(func)
```
Так как функции func присваивается та же оригинальная функция funс, то такой декоратор просто что-то делает после определения функций.

Можно использовать для регистрации функции в прикладном интерфейсе, присоединения атрибутов функции и тп.

Мы изучали больше перехват **вызова** функции:
```python
def decorator(F):
    # Сохраняет или использует функцию F
    # Возвращает другой вызываемый объект:
    # вложенная инструкция def, class с методом __call__ и так далее.
@decorator
def func(): ...         # func = decorator(func)
```
Декоратор вызывается на этапе декорирования. Возвращаемый объект будет вызываться при вызове функции. Возвращаемый объект может принимать любые аргументы, которые передаются в декорируемую функцию.

Аналогично, при декорировании класса объект экземпляра является всего лишь первым аргументом возвращаемого вызываемого объекта.

Т.е. при декорировании фукнции:
```python
def decorator(F):       # На этапе декорирования @
    def wrapper(*args): # Обертывающая функция
        # Использование F и аргументов
        # F(*args) – вызов оригинальной функции
    return wrapper
    
@decorator              # func = decorator(func)
def func(x, y):         # func передается декоратору в аргументе F
    ...
func(6, 7)              # 6, 7 передаются функции wrapper в виде *args
```
* когда в программе будет вызвана функция func, в действительности будет вызвана функция wrapper, возвращаемая декоратором; 
* функция wrapper может вызвать оригинальную функцию func, которая остается доступной ей в области видимости объемлющей функции. 

**Для каждой декорированной функции создается новая область видимости, в которой сохраняется информация о состоянии.**

При декорировании с помощью класса:
```python
class decorator:
    def __init__(self, func):   # На этапе декорирования @
        self.func = func
    def __call__(self, *args):  # Обертка вызова функции
        # Использование self.func и аргументов
        # self.func(*args) – вызов оригинальной функции
        
@decorator
def func(x, y):                 # func = decorator(func)
    ...                         # func будет передана методу __init__

func(6, 7)                      # 6, 7 передаются методу __call__ в виде *args
```
* Когда в программе будет вызывана функция func, в действительности будет вызван метод `__call__` перегрузки операторов экземпляра, созданного декоратором; 
* метод `__call__` вызовет оригинальную функцию func, которая доступна ему в виде атрибута экземпляра. 

**Для каждой декорированной функции создается новый экземпляр, хранящий информацию о состоянии в своих атрибутах.**

В методах класса первым аргуметом идет self, поэтому такой класс-декоратор **не работает для декорирования методов**.

## Декорирование методов

```python
class decorator:
    def __init__(self, func):   # func – это метод, не связанный
        self.func = func        # с экземпляром класса decorator
        
    def __call__(self, *args):  # self – это экземпляр декоратора
        # вызов self.func(*args) потерпит неудачу!
        # Экземпляр C отсутствует в args!

class C:
    @decorator
    def method(self, x, y):     # method = decorator(method)
        ...                     # то есть имени method присваивается экземпляр
                                # класса decorator
```

Для **одновременной поддержки** возможности декорирования функций и методов лучше всего применять вложенные функции:

```python
def decorator(F):               # F – функция или метод, не связанный с экземпляром
    def wrapper(*args):         # для методов - экземпляр класса в args[0]
        # F(*args) – вызов функции или метода
    return wrapper
    
@decorator
def func(x, y):                 # func = decorator(func)
    ...
func(6, 7) # В действительности вызовет wrapper(6, 7)

class C:
    @decorator
    def method(self, x, y):     # method = decorator(method)
        ...                     # Присвоит простую функцию

X = C()
X.method(6, 7)                  # В действительности вызовет wrapper(X, 6, 7)
```

Вложенные функции - самый простой способ создания декораторов.

# Декораторы классов

Можно декорировать класс. Конструкция 
```python
@decorator          # Декорирование класса
    class C:
        ...

x = C(99)           # Создает экземпляр
```
эквивалентна конструкции
```python
class C:
    ...
C = decorator(C)    # Присваивает имени класса результат,
                    # возвращаемый декоратором
x = C(99)           # Фактически вызовет decorator(C)(99)
```

Результат работы декоратора вызывается, когда позднее в программе нужно создать экземпляр класса. Например, чтобы выполнить некоторые операции сразу после создания класса, нужно вернуть сам оригинальный класс:

```python
def decorator(C):
    # Обработать класс C
    return C
    
@decorator
class C: ...        # C = decorator(C)
```
Если нужно добавить обертывающую логику, которая будет перехватывать создание экземпляра класса С, то нужно возвращать вызываемый объект:
```python
def decorator(C):
    # Сохранить или использовать класс C
    # Возвращает другой вызываемый объект:
    # вложенная инструкция def, class с методом __call__ и так далее.
    
@decorator
class C: ...        # C = decorator(C)
```

Пример такого обертывания класса, когда к классу добавляется интерфейс (тут - обработка обращений к неопределенным атрибутам):
```python
def decorator(cls):                 # На этапе декорирования @
    class Wrapper:
        def __init__(self, *args):  # На этапе создании экземпляра
            self.wrapped = cls(*args)
        def __getattr__(self, name): # Вызывается при обращении к атрибуту
            return getattr(self.wrapped, name)
    return Wrapper

@decorator
class C:                            # C = decorator(C)
    def __init__(self, x, y):       # Вызывается методом Wrapper.__init__
        self.attr = 'spam'

x = C(6, 7)                         # В действительности вызовет Wrapper(6, 7)
print(x.attr)                       # Вызовет Wrapper.__getattr__, выведет 'spam'
```
Цитата (Лутц, с 1096)
В этом примере декоратор присвоит оригинальному имени класса другой класс, который сохраняет оригинальный класс в области видимости объемлющей функции, создает и встраивает экземпляр оригинального класса при вызове. Когда позднее будет выполнена попытка прочитать значение атрибута экземпляра, она будет перехвачена методом \_\_getattr\_\_ обертки и делегирована встроенному экземпляру оригинального класса. Кроме того, для каждого декорированного класса создается новая область видимости объемлющей функции, в которой сохраняется оригинальный класс.

### Поддержка множества экземпляров

**Тут будет ОДИН экземпляр класса С**

```python
class Decorator:
    def __init__(self, C):      # На этапе декорирования @
        self.C = C
    def __call__(self, *args):  # На этапе создания экземпляра
        self.wrapped = self.C(*args)
        return self
    def __getattr__(self, attrname): # Вызывается при обращении к атрибуту
        return getattr(self.wrapped, attrname)
        
@Decorator
class C: ...                    # C = Decorator(C)

x = C()
y = C()                         # Затрет x!
```
пример подробнее с печатью:
```python
class Decorator:
    def __init__(self, C):      # На этапе декорирования @
        print('Decorator.__init__, C=', C)
        self.C = C
    def __call__(self, *args):  # На этапе создания экземпляра
        print('Decorator.__call__, *args', *args, 'self=', id(self))
        self.wrapped = self.C(*args)
        return self
    def __getattr__(self, attrname): # Вызывается при обращении к атрибуту
        return getattr(self.wrapped, attrname)
        
@Decorator
class C:                        # C = Decorator(C)
    def __init__(self, n):
        print("create C, id=", id(self))
        self.n = n

x = C(1)
y = C(2)                         # Затрет x!

print(id(x))
print(id(y))

print(x.n)
print(y.n)
```
выведет:
```python
Decorator.__init__, C= <class '__main__.C'>
Decorator.__call__, *args 1 self= 4293020976
create C, id= 4293020944
Decorator.__call__, *args 2 self= 4293020976
create C, id= 4292307344
4293020976
4293020976
2
2
```
Можно исправить, вернув из `Decorator.__call__` не self, а self.wrapped.

Альтернативный подход будет описан ниже.

## Вложение декораторов

Конструкция
```python
@A
@B
@C
def f(...):
    ...
```
равноценна следующей:
```python
def f(...):
    ...
f = A(B(C(f)))
```
пример:
```python
def d1(F): return lambda: 'X' + F()
def d2(F): return lambda: 'Y' + F()
def d3(F): return lambda: 'Z' + F()

@d1
@d2
@d3
def func():         # func = d1(d2(d3(func)))
    return 'spam'
    
print(func())       # XYZsmap
```

## Пример декоратора - измерение производительности

Напишем декоратор, который измеряет сколько времени занимает вызов функции и будет суммировать это время для разных вызовов.

До Python 3.3 для этого можно использовать функцию time.clock(). Начиная с Python 3.3 лучше использовать time.perf_counter() или time.process_time().

Измерение времени генерации списков против времени создания с использованием функции map имеет смысл до Python 2.6, потому что далее map возвращает генератор (т.е. отрабатывает мгновенно) и нужно сравнивать уже итерацию по генератору и по списку.

```python
import time

class timer:
    def __init__(self, func):
        self.func = func
        self.alltime = 0
        
    def __call__(self, *args, **kargs):
        start = time.clock()
        result = self.func(*args, **kargs)
        elapsed = time.clock() - start
        self.alltime += elapsed
        print('%s: %.5f, %.5f' % (self.func.__name__, elapsed, self.alltime))
        return result
        
@timer
def listcomp(N):
    return [x * 2 for x in range(N)]

@timer
def mapcall(N):
    return map((lambda x: x * 2), range(N))
    
result = listcomp(5)    # Хронометраж данного вызова, всех вызовов,
listcomp(50000)         # возвращаемое значение
listcomp(500000)
listcomp(1000000)
print(result)
print('allTime = %s' % listcomp.alltime) # Общее время всех вызовов listcomp
print('')

result = mapcall(5)
mapcall(50000)
mapcall(500000)
mapcall(1000000)
print(result)
print('allTime = %s' % mapcall.alltime)         # Общее время всех вызовов mapcall

print('map/comp = %s' % round(mapcall.alltime / listcomp.alltime, 3))
```
получим (Python 2.6):
```python
listcomp: 0.00002, 0.00002
listcomp: 0.00910, 0.00912
listcomp: 0.09105, 0.10017
listcomp: 0.17605, 0.27622
[0, 2, 4, 6, 8]
allTime = 0.276223304917

mapcall: 0.00003, 0.00003
mapcall: 0.01363, 0.01366
mapcall: 0.13579, 0.14945
mapcall: 0.27648, 0.42593
[0, 2, 4, 6, 8]
allTime = 0.425933533452
map/comp = 1.542
```

### Добавим аргументы в декоратор timer

Хочется, чтобы каждый таймер имел метку для вывода (например, печатать `==>`), а так же отключать и включать сообщения.

Для передачи аргумента в декоратор можно написать функцию-декоратор:
```python
def timer(label=''):
    def decorator(func):
        def onCall(*args):      # Аргументы args передаются функции
            ...                 # func сохраняется в объемлющей области
            print(label, ...    # label сохраняется в объемлющей области
        return onCall
    return decorator            # Возвращает фактический декоратор

@timer('==>')                   # То же, что и listcomp = timer('==>')(listcomp)
def listcomp(N): ...            # Имени listcomp присваивается декоратор

listcomp(...)                   # В действительности вызывается функция decorator
```

# Задачи

## Использовать декоратор

Напишите пример использования декоратора [Easy Dump of Function Arguments](https://wiki.python.org/moin/PythonDecoratorLibrary#Easy_Dump_of_Function_Arguments)

Посмотрите, как он работает для переданных в виде аргументов списков и словарей.



## Написать декоратор, который ...

### Дописать в декоратор logit логирование аргументов, с которым была вызвана функция