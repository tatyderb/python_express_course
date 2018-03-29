# Дополнительные возможности модулей

## Сокрытие данных в модулях

Конструкция `from .. import *` импортирует иногда лишнее (что является внутренними переменными и методами модуля и не являются его API).

Как с этим бороться? (Никак, увы.)

* переменные (и функции) вида \_x не доступны при таком импорте;
* можно в \_\_init\_\_.py файле определить список **\_\_all\_\_** и тогда будут импортироваться при \* только указанные имена.

```python
__all__ = ['Error', 'encode', 'decode'] # Экспортируются только эти имена
```

Ничто не мешает нужный метод или переменную импортировать, явно указав имя.

## Изменение пути поиска модулей

Т.е. нужно изменить sys.path.

Например:
```python
>>> import sys
>>> sys.path
['', 'C:\\users', 'C:\\Windows\\system32\\python30.zip', ...далее опущено...]
>>> sys.path.append('C:\\sourcedir')        # Дополнение пути поиска модулей
>>> import string                           # Новый каталог будет участвовать в поиске
```
Так можно полностью переписать пути поиска:
```python
>>> sys.path = [r'd:\temp'] # Изменяет путь поиска модулей
>>> sys.path.append('c:\\lp4e\\examples') # Только для этой программы
>>> sys.path
['d:\\temp', 'c:\\lp4e\\examples']
>>> import string
Traceback (most recent call last):
File "<stdin>", line 1, in ?
ImportError: No module named string
```

Добавить текущую директорию в sys.path (далее расскажут об используемых модулях и методах).
```python
from os.path import dirname
sys.path.append(dirname(__file__))
```

## Модули - это объекты

Пусть есть модуль М. В нем есть атрибут name.

Доступ к атрибуту:
```python
M.name                  # Полное имя объекта
M.__dict__['name']      # Доступ с использованием словаря пространства имен
sys.modules['M'].name   # Доступ через таблицу загруженных модулей
getattr(M, 'name')      # Доступ с помощью встроенной функции
```

## Документация модулей

В начале модуля можно задать строку документации в тройных кавычках. 
Файл mydir.py:
```python
"""
mydir.py: описание для чего служит файл
"""

def listing(module, verbose=True):
    # далее код модуля
```

Написанную документацию для модуля mydir можно вывести как:
```python
>>> import mydir
>>> help(mydir)
Help on module mydir:
NAME
    mydir - mydir.py: описание для чего служит файл
FILE
    c:\users\veramark\mark\mydir.py
FUNCTIONS
    listing(module, verbose=True)
```

## Импортирование модуля в виде строки

Нельзя написать:
```python
>>> import "string"
File "<stdin>", line 1
import "string"
^
SyntaxError: invalid syntax
```
или 
```python
x = "string"
import x        # тут пытаемся импортировать не модуль string, а ищем файл x.py
```
Выполним код с помощью **exec()**
```python
>>> modname = 'string'
>>> exec('import ' + modname)   # Выполняется как строка программного кода
>>> string                      # Модуль был импортирован в пространство имен
<module 'string' from 'c:\Python30\lib\string.py'>
```
или вызовем функцию **\_\_import\_\_()**
```python
>>> modname = 'string'
>>> string = __import__(modname)
>>> string
<module 'string' from 'c:\Python30\lib\string.py'>
```

## Перегрузка модулей (еще раз)

При перегрузке модуля через reload иногда возникает проблема, что нужно перегрузить все модули, которые были в него импортированы.

Придется писать код, который "вручную" перегружает все необходимые модули. Можно для этого анализировать \_\_dict\_\_ 
Лутц, стр 679 - пример такого кода.
