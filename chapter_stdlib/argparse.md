# Разбор аргументов командной строки

* [getopt](https://docs.python.org/3/library/getopt.html#module-getopt) - как getopt в С.
* [optparse](https://docs.python.org/3/library/optparse.html#module-optparse) - deprecated
* [argparse](https://docs.python.org/3/library/argparse.html) - будем изучать

Есть еще другие модули.

## Источники

* [argparse tutorial](https://docs.python.org/3/howto/argparse.html)
* [argparse документация](https://docs.python.org/3/library/argparse.html)

## Какие бывают аргументы командной строки

Запустим команду **ls** и посмотрим, какие у нее есть аргументы:
```python
$ ls
cpython  devguide  prog.py  pypy  rm-unused-function.patch
$ ls pypy
ctypes_configure  demo  dotviewer  include  lib_pypy  lib-python ...
$ ls -l
total 20
drwxr-xr-x 19 wena wena 4096 Feb 18 18:51 cpython
drwxr-xr-x  4 wena wena 4096 Feb  8 12:04 devguide
-rwxr-xr-x  1 wena wena  535 Feb 19 00:05 prog.py
drwxr-xr-x 14 wena wena 4096 Feb  7 00:59 pypy
-rw-r--r--  1 wena wena  741 Feb 18 01:01 rm-unused-function.patch
$ ls --help
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
...
```

* Можно запускать команду без параметров, она покажет содержимое текущей директории.
* Позиционный аргумент - имя директории, которую мы просматриваем. Программа решает что делать с аргументом на основе того, _где_ он появился в командной строке. Так в команде `cp src dst` первый аргумент - что копируем, второй аргумент - куда копируем.
* `-l` может появиться, а может и нет. Опциональный аргумент. 
  * Возможна склейка аргументов, т.е. либо вызов `ls -l -a`, либо `ls -la`.
  * опциональные аргументы возможно записать в короткой `-s` или полной `--size` форме.
* есть хелп

## Простой разбор аргументов

Почти ничего не сделали.
```python
import argparse
parser = argparse.ArgumentParser()
parser.parse_args()
```
что получили?
```python
$ python3 prog.py
$ python3 prog.py --help
usage: prog.py [-h]

optional arguments:
  -h, --help  show this help message and exit
$ python3 prog.py --verbose
usage: prog.py [-h]
prog.py: error: unrecognized arguments: --verbose
$ python3 prog.py foo
usage: prog.py [-h]
prog.py: error: unrecognized arguments: foo
```
* Без аргументов ничего не делает.
* Есть хелп, который запускается по ключам -h или --help
* Если задаем аргументы, которых нет, получаем сообщение об ошибке + usage.

## Позиционные аргументы

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()
print(args.echo)
```
запускаем:
```python
$ python3 prog.py
usage: prog.py [-h] echo
prog.py: error: the following arguments are required: echo
$ python3 prog.py --help
usage: prog.py [-h] echo

positional arguments:
  echo

optional arguments:
  -h, --help  show this help message and exit
$ python3 prog.py foo
foo
```
* функция `add_argument("echo")` добавила позиционный аргумент в список допустимых аргументов.  
* `parse_args()` возвращает данные, в атрибуте _echo_ этих данных находится позиционный аргумент.
* В хелп попадет без описания
* если он не задан, получаем сообщение об ошибке, какого именно аргумента нет.

Добавим хелп:
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)
```
получим:
```python
$ python3 prog.py -h
usage: prog.py [-h] echo

positional arguments:
  echo        echo the string you use here

optional arguments:
  -h, --help  show this help message and exit
```

Пусть программа считает квадрат аргумента:
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number")
args = parser.parse_args()
print(args.square**2)
```
получаем:
```python
$ python3 prog.py 4
Traceback (most recent call last):
  File "prog.py", line 5, in <module>
    print(args.square**2)
TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'int'
```

Очевидно, что аргументы разбираются как строки. А нужно число.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number",
                    type=int)
args = parser.parse_args()
print(args.square**2)
```
получим:
```python
$ python3 prog.py 4
16
$ python3 prog.py four
usage: prog.py [-h] square
prog.py: error: argument square: invalid int value: 'four
```
Заметьте, что диагностика изменилась. Аргумент есть, но не того типа - тоже проведет к сообщению об ошибке.

TODO: описать все возможные типы из документации.

## Опциональные аргументы

Добавляются той же функцией **add_argument**, начинаются с --.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")
```
получим:
```python
$ python3 prog.py --verbosity 1
verbosity turned on
$ python3 prog.py
$ python3 prog.py --help
usage: prog.py [-h] [--verbosity VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  --verbosity VERBOSITY
                        increase output verbosity
$ python3 prog.py --verbosity
usage: prog.py [-h] [--verbosity VERBOSITY]
prog.py: error: argument --verbosity: expected one argument
```

* Программа написана так, чтобы что-то печатать, когда задано --verbosity и ничего не печатать, когда не задано.
* аргумент не обязательный, можно запускать без него.
* если запустили без него, то значение переменной args.verbosity выставляется в None и проверка if args.verbosity дает False.
* добавлено его описание в секцию optional arguments
* требует параметра после --verbosity (любого типа), иначе не работает.

Но такое поведение удобно, например, для опционального задания конфиг-файла, `-c myconfig.ini`, но не для переменной, которая либо включена (повышенный уровень логирования), либо выключена.

Сделаем ее булевской переменной:
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
```
получим:
```python
$ python3 prog.py --verbose
verbosity turned on
$ python3 prog.py --verbose 1
usage: prog.py [-h] [--verbose]
prog.py: error: unrecognized arguments: 1
$ python3 prog.py --help
usage: prog.py [-h] [--verbose]

optional arguments:
  -h, --help  show this help message and exit
  --verbose   increase output verbosity
```
Теперь опциональный аргумент должен запускаться без параметров и его значение либо True (если указан), либо False (если не указан).

Хелп изменился.

### Короткие имена -v и --verbosity

Просто перечислите варианты задания аргумента в add_argument:
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
```
получим:
```python
$ python3 prog.py -v
verbosity turned on
$ python3 prog.py --help
usage: prog.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
```

## Позиционные и опциональные аргументы вместе

В программу вычисления квадрата числа добавим опцию --verbosity.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print("the square of {} equals {}".format(args.square, answer))
else:
    print(answer)
```
Запустим программу:
```python
$ python3 prog.py
usage: prog.py [-h] [-v] square
prog.py: error: the following arguments are required: square
$ python3 prog.py 4
16
$ python3 prog.py 4 --verbose
the square of 4 equals 16
$ python3 prog.py --verbose 4
the square of 4 equals 16
```
* Вернули позиционный аргумент, значит получили ошибку, что его нет.
* порядок позиционного и опционального аргумента не имеет значения.

### Опциональный аргумент с параметром + позиционный аргумент

Сделаем шаг назад. Пусть наш опциональный аргумент имеет параметр - какой уровень логирования будет использован (целое число, как и позиционный аргумент).

Как в этом случае задать и разобрать аргументы?

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```
запускаем:
```python
$ python3 prog.py 4
16
$ python3 prog.py 4 -v
usage: prog.py [-h] [-v VERBOSITY] square
prog.py: error: argument -v/--verbosity: expected one argument
$ python3 prog.py 4 -v 1
4^2 == 16
$ python3 prog.py 4 -v 2
the square of 4 equals 16
$ python3 prog.py 4 -v 3
16
```
### выбор значения из заранее определенного списка

Не нравится, что при задании `--verbosity 3` мы получили 0 уровень. И никто не скажет, какие уровни доступны. Зададим допустимый набор аргументов:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```
запустим:
```python
$ python3 prog.py 4 -v 3
usage: prog.py [-h] [-v {0,1,2}] square
prog.py: error: argument -v/--verbosity: invalid choice: 3 (choose from 0, 1, 2)
$ python3 prog.py 4 -h
usage: prog.py [-h] [-v {0,1,2}] square

positional arguments:
  square                display a square of a given number

optional arguments:
  -h, --help            show this help message and exit
  -v {0,1,2}, --verbosity {0,1,2}
                        increase output verbosity
```

Заметьте, изменились и хелп, и сообщение ошибке.

## Подсчет количества заданных аргументов -v action='count'

Хотим определять уровень логирования по тому, сколько раз задали опцию -v в командной строке: ничего, -v, -vv.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display the square of a given number")
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```
запускаем:
```python
$ python3 prog.py 4
16
$ python3 prog.py 4 -v
4^2 == 16
$ python3 prog.py 4 -vv
the square of 4 equals 16
$ python3 prog.py 4 --verbosity --verbosity
the square of 4 equals 16
$ python3 prog.py 4 -v 1
usage: prog.py [-h] [-v] square
prog.py: error: unrecognized arguments: 1
$ python3 prog.py 4 -h
usage: prog.py [-h] [-v] square

positional arguments:
  square           display a square of a given number

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity  increase output verbosity
$ python3 prog.py 4 -vvv
16
```

* Если не определен ни один флаг -v, то args.verbosity = None
* Без разницы - указыват короткую или полную форму флага -v или --verbosity.
* Слишком большое количество аргументов -vvv дает опять лаконичную форму логирования. 

Поправим это, заменив
`if args.verbosity == 2` на `if args.verbosity >= 2`.

Увы, если не задано -v, то переменная None и для нее не определено >=.

Добавим опцию **default**=0, чтобы когда аргумент не задан, значение переменной было не None, а 0.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
```
запустим:
```python
$ python3 prog.py 4 -vvv
the square of 4 equals 16
$ python3 prog.py 4
16
```

## Опциональный аргумент МОЖЕТ содержать параметр

```python
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('--foo', nargs='?', help='foo help')
>>> parser.add_argument('bar', nargs='+', help='bar help')
>>> parser.print_help()
usage: PROG [-h] [--foo [FOO]] bar [bar ...]

positional arguments:
 bar          bar help

optional arguments:
 -h, --help   show this help message and exit
 --foo [FOO]  foo help
```

## Сложный пример

Напишем программу, которая возводит не в квадрат, а в указанную степень:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()
answer = args.x**args.y
if args.verbosity >= 2:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
elif args.verbosity >= 1:
    print("{}^{} == {}".format(args.x, args.y, answer))
else:
    print(answer)
```
запустим:
```python
$ python3 prog.py
usage: prog.py [-h] [-v] x y
prog.py: error: the following arguments are required: x, y
$ python3 prog.py -h
usage: prog.py [-h] [-v] x y

positional arguments:
  x                the base
  y                the exponent

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity
$ python3 prog.py 4 2 -v
4^2 == 16
```

## Взаимоисключающие аргументы

Зададим два аргумента: -v - повысить уровень логирования, -q - отключить логирование.

Добавим их в **add_mutually_exclusive_group()**

```python
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
```
запустим:
```python
$ python3 prog.py 4 2
4^2 == 16
$ python3 prog.py 4 2 -q
16
$ python3 prog.py 4 2 -v
4 to the power 2 equals 16
$ python3 prog.py 4 2 -vq
usage: prog.py [-h] [-v | -q] x y
prog.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
$ python3 prog.py 4 2 -v --quiet
usage: prog.py [-h] [-v | -q] x y
prog.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
```

## Добавим описание, для чего нужна программа

**argparse.ArgumentParser(description=**"calculate X to the power of Y"**)**

```python
import argparse

parser = argparse.ArgumentParser(description="calculate X to the power of Y")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
```
запустим:
```python
$ python3 prog.py --help
usage: prog.py [-h] [-v | -q] x y

calculate X to the power of Y

positional arguments:
  x              the base
  y              the exponent

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
  -q, --quiet
```

## Переменное число позиционных аргументов

Напишем программу, которая складывает числа, которые заданы в виде аргументов. 


## TODO
TODO: документация по add_argument (action)