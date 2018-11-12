## Не пойманное исключение

```python
def foo(a):
    x = 5 / a
    print(x, a)
    
foo(5)
foo(0)      # на 0 делить нельзя
foo(7)
```
* foo(5) был вызван и выполнился. 
* foo(0) был вызван, но выполнение всей программы прекратилось на строке x = 5 / a
* foo(7) не вызвался.

Получили:
```
1.0 5
Traceback (most recent call last):
  File "nocatch.py", line 6, in <module>
    foo(0)      # на 0 делить нельзя
  File "nocatch.py", line 2, in foo
    x = 5 / a
ZeroDivisionError: division by zero
```

Это называется **stacktrace**.

Рассмотрим подробнее сообщение об ошибке. Напечатан стек вызова функций с указанием в каком файле на какой строке возникло исключение и код, который его породил.

```python
ZeroDivisionError: division by zero
```

**ZeroDivisionError** - тип исключения. Исключение - это такой же объект, как и другие данные в программе. 

**division by zero** - текст этого исключения. Зависит от типа.

## Блок try - except

Попробуем поймать исключение:

```python
def foo(a):
    x = 5 / a
    print(x, a)

try:    
    foo(5)
    foo(0)      # на 0 делить нельзя
    foo(7)
except ZeroDivisionError as e:
    print('Поймали исключение!')
    
print('После блока обработки исключений')
```
Получили:
```python
1.0 5
Поймали исключение!
После блока обработки исключений
```

Видим, что при поимке исключения, программа может выполняться дальше.

foo(7) - не выполняется, так как это блок try - то что нужно выполнить до первого исключения.

print('После блока обработки исключений') - программа работает дальше, после окончания try-ecxept блока.

## Как работает перехват исключений

* Вначале выполняется код, находящийся между операторами try и except.
* Если в ходе его выполнения исключения не произошло, то код в блоке except пропускается, а код в блоке try выполняется весь до конца.
* Если исключение происходит, то выполнение в рамках блока try прерывается и выполняется код в блоке except. При этом для оператора except можно указать, какие исключения можно обрабатывать в нем. При возникновении исключения, ищется именно тот блок except, который может обработать данное исключение.
* Если среди except блоков нет подходящего для обработки исключения, то оно передается наружу из блока try. В случае, если обработчик исключения так и не будет найден, то исключение будет необработанным (unhandled exception) и программа аварийно остановится.


## Много разных исключений

Иногда код может породить исключения разных типов.

Если они обрабатываются одинаково, то перечислите их типы через запятую:
```python
except (RuntimeError, TypeError, NameError):
    pass
```

Если нужна разная обработка, то пишем много except блоков:
```python
ecxept RuntimeError:
    print('один случай')
ecxept TypeError:
    print('второй случай')
ecxept NameError:
    print('третий случай')
```

Примеры. Перечисление:
```python
import traceback
import sys

def foo(a):
    b = [1, 2, 3]
    x = 5 / a
    y = b[a]
    print(x, a, y)

try:    
    foo(2)
    # foo(0)      # на 0 делить нельзя
    foo(7)
except (ZeroDivisionError, IndexError)  as e:
    print('Поймали исключение!')
    print(e)
    print('-'*60)
    traceback.print_exc(file=sys.stdout)
    print('-'*60)
    
print('После блока обработки исключений')
```

Отдельные блоки:
```python
import traceback
import sys

def foo(a):
    b = [1, 2, 3]
    x = 5 / a
    y = b[a]
    print(x, a, y)

try:    
    foo(2)      # ok
    foo(0)      # на 0 делить нельзя
    foo(7)      # выход за границы списка
except ZeroDivisionError:
    pass
except IndexError  as e:
    print('Поймали исключение!')
    print(e)
    print('-'*60)
    traceback.print_exc(file=sys.stdout)
    print('-'*60)
    
print('После блока обработки исключений')
```

## Разные исключения ловим в разных местах

Вызываются функции bzz -> qqq -> foo.

В foo возникают исключения ZeroDivisionError и IndexError.

Поймаем исключение ZeroDivisionError в функции qqq, а IndexError в функции bzz.

```python
import traceback
import sys

def foo(a):
    b = [1, 2, 3]
    x = 5 / a
    y = b[a]
    print(x, a, y)
    
def qqq(a):
    try:
        foo(a)
    except ZeroDivisionError:
        print('qqq: ZeroDivisionError')
        traceback.print_exc(file=sys.stdout)
    print('qqq: After try-ecxept block')
        
def bzz(a):
    try:
        qqq(a)
    except IndexError:
        print('bzz: IndexError')
        traceback.print_exc(file=sys.stdout)
    print('bzz: After try-ecxept block\n')

bzz(2)
        # 2.5 2 3
        # qqq: After try-ecxept block
        # bzz: After try-ecxept block
bzz(0)
        # qqq: ZeroDivisionError
        # qqq: After try-ecxept block
        # bzz: After try-ecxept block
bzz(7)
        # bzz: IndexError
        # bzz: After try-ecxept block
```

Обратите внимание на различие в stacktrace.

```python
2.5 2 3
qqq: After try-ecxept block
bzz: After try-ecxept block

qqq: ZeroDivisionError
Traceback (most recent call last):
  File "2_2try_tb.py", line 12, in qqq
    foo(a)
  File "2_2try_tb.py", line 6, in foo
    x = 5 / a
ZeroDivisionError: division by zero
qqq: After try-ecxept block
bzz: After try-ecxept block

bzz: IndexError
Traceback (most recent call last):
  File "2_2try_tb.py", line 20, in bzz
    qqq(a)
  File "2_2try_tb.py", line 12, in qqq
    foo(a)
  File "2_2try_tb.py", line 7, in foo
    y = b[a]
IndexError: list index out of range
bzz: After try-ecxept block
```
