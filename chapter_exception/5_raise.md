## Генерация исключений в Python

Для принудительной генерации исключения используется инструкция **raise**.

Самый простой пример работы с raise может выглядеть так.
```python
try:
   raise Exception("Some exception")
except Exception as e:
   print("Exception exception " + str(e))
```
Таким образом, можно "вручную" вызывать исключения при необходимости.

Или перевызвать последнее исключение, вызвав **raise** без параметров.

## Информация в исключении

Обычно достаточно перехватить исключение и реагировать на сам факт его появления.

**args** - это кортеж составных частей исключения. В него можно добавить свою информацию.

Код
```python
(a,b,c) = d
```
может породить исключение
```python
ValueError: unpack list of wrong size
```

Сразу возникает вопрос - а что в переменной d, что не удалось его распаковать. Добавим значение переменной d в исключение и raise обновленное исключение.

```python
try:
  a, b, c = d
except Exception as e:
  e.args += (d,)
  raise
```


Иногда нужно логировать исключение или обрабатывать дополнительную информацию.
```python
import traceback
import sys

def foo(a):
    x = 5 / a
    print(x, a)

try:    
    foo(5)
    foo(0)      # на 0 делить нельзя
    foo(7)
except ZeroDivisionError as e:                  # если e не нужно, то as e не пишем
    print('Поймали исключение!')
    print(e)                                    # печать 'division by zero'
    print('-'*60)
    traceback.print_exc(file=sys.stdout)        # печать stacktrace
    print('-'*60)
    
print('После блока обработки исключений')
```
Получили:
```python
1.0 5
Поймали исключение!
division by zero
------------------------------------------------------------
Traceback (most recent call last):
  File "1try.py", line 10, in <module>
    foo(0)      # на 0 делить нельзя
  File "1try.py", line 5, in foo
    x = 5 / a
ZeroDivisionError: division by zero
------------------------------------------------------------
После блока обработки исключений
```

### Напечатать только сообщение исключения

**str(e)** - просто преобразуйте исключение к строке.

### Напечатать stacktrace исключения

[Документация](https://docs.python.org/3/library/traceback.html)

Используйте функцию **traceback.print_exc()**

### Тип, значение и traceback

Используйте функцию **sys.exc_info()**
 
```python
exc_type, exc_value, exc_traceback = sys.exc_info()
```

### Пример, как все это используется

Сохраните программу в файл tb.py и запустите ее.
```python
import sys, traceback

def lumberjack():
    bright_side_of_death()

def bright_side_of_death():
    return tuple()[0]

try:
    lumberjack()
except IndexError:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    
    print("*** print_tb:")
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    
    print("*** print_exception:")
    # exc_type below is ignored on 3.5 and later
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
                              
    print("*** print_exc:")
    traceback.print_exc(limit=2, file=sys.stdout)
    
    print("*** format_exc, first and last line:")
    formatted_lines = traceback.format_exc().splitlines()
    print(formatted_lines[0])
    print(formatted_lines[-1])
    
    print("*** format_exception:")
    # exc_type below is ignored on 3.5 and later
    print(repr(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback)))
                                          
    print("*** extract_tb:")
    print(repr(traceback.extract_tb(exc_traceback)))
    print("*** format_tb:")
    print(repr(traceback.format_tb(exc_traceback)))
    print("*** tb_lineno:", exc_traceback.tb_lineno)
```
Получилось:
```python
*** print_tb:
  File "tb.py", line 10, in <module>
    lumberjack()
*** print_exception:
Traceback (most recent call last):
  File "tb.py", line 10, in <module>
    lumberjack()
  File "tb.py", line 4, in lumberjack
    bright_side_of_death()
IndexError: tuple index out of range
*** print_exc:
Traceback (most recent call last):
  File "tb.py", line 10, in <module>
    lumberjack()
  File "tb.py", line 4, in lumberjack
    bright_side_of_death()
IndexError: tuple index out of range
*** format_exc, first and last line:
Traceback (most recent call last):
IndexError: tuple index out of range
*** format_exception:
['Traceback (most recent call last):\n', '  File "tb.py", line 10, in <module>\n    lumberjack()\n', '  File "tb.py", line 4, in lumberjack\n    bright_side_of_death()\n', '  File "tb.py", line 7, in bright_side_of_death\n    return tuple()[0]\n', 'IndexError: tuple index out of range\n']
*** extract_tb:
[<FrameSummary file tb.py, line 10 in <module>>, <FrameSummary file tb.py, line 4 in lumberjack>, <FrameSummary file tb.py, line 7 in bright_side_of_death>]
*** format_tb:
['  File "tb.py", line 10, in <module>\n    lumberjack()\n', '  File "tb.py", line 4, in lumberjack\n    bright_side_of_death()\n', '  File "tb.py", line 7, in bright_side_of_death\n    return tuple()[0]\n']
*** tb_lineno: 10
```
