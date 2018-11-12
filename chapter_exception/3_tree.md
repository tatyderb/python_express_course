## Иерархия исключений

Какой тип в блоке except является подходящим, чтобы перехватить исключение?

Точно такой же или его предок в иерархии классов исключений.

Ищем походящий блок сверху вниз:
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
    #foo(0)      # на 0 делить нельзя
    foo(7)      # выход за границы списка
except Exception:           # ловим еще исключения, которые наследуют от класса Exception
    pass
except IndexError  as e:    # никогда не выполнится, исключение поймали раньше
    print('Поймали исключение!')
    print(e)
    print('-'*60)
    traceback.print_exc(file=sys.stdout)
    print('-'*60)
    
print('После блока обработки исключений')
```

При выходе за границы массива исключение будет перехвачено в блоке except Exception, потому что в предках класса IndexError есть Exception.

Пишем исключения от самых специфических (сначала) к более общим (ниже).

** Никогда не пишите ecxept Exception**. Так вы поймаете (чужие) исключения, которые не позволят диагностировать логическую ошибку в программе.

**except без указания типа ловит все исключения. Не надо так писать!**

Информация о дереве наследования:
```python
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
```

### Обзор исключений

* **BaseException** - базовое исключение, от которого берут начало все остальные.
    * **SystemExit** - исключение, порождаемое функцией sys.exit при выходе из программы.
    * **KeyboardInterrupt** - порождается при прерывании программы пользователем (обычно сочетанием клавиш Ctrl+C).
    * **GeneratorExit** - порождается при вызове метода close объекта generator.
    * **Exception** - а вот тут уже заканчиваются полностью системные исключения (которые лучше не трогать) и начинаются обыкновенные, с которыми можно работать.
        * **StopIteration** - порождается встроенной функцией next, если в итераторе больше нет элементов.
        * **ArithmeticError** - арифметическая ошибка.
            * **FloatingPointError** - порождается при неудачном выполнении операции с плавающей запятой. На практике встречается нечасто.
            * **OverflowError** - возникает, когда результат арифметической операции слишком велик для представления. Не появляется при обычной работе с целыми числами (так как python поддерживает длинные числа), но может возникать в некоторых других случаях.
            * **ZeroDivisionError** - деление на ноль.
        * **AssertionError** - выражение в функции assert ложно.
        * **AttributeError** - объект не имеет данного атрибута (значения или метода).
        * **BufferError** - операция, связанная с буфером, не может быть выполнена.
        * **EOFError** - функция наткнулась на конец файла и не смогла прочитать то, что хотела.
        * **ImportError** - не удалось импортирование модуля или его атрибута.
        * **LookupError** - некорректный индекс или ключ.
            * **IndexError** - индекс не входит в диапазон элементов.
            * **KeyError** - несуществующий ключ (в словаре, множестве или другом объекте).
        * **MemoryError** - недостаточно памяти.
        * **NameError** - не найдено переменной с таким именем.
            * **UnboundLocalError** - сделана ссылка на локальную переменную в функции, но переменная не определена ранее.
        * **OSError** - ошибка, связанная с системой.
            * **BlockingIOError**
            * **ChildProcessError** - неудача при операции с дочерним процессом.
            * **ConnectionError** - базовый класс для исключений, связанных с подключениями.
                * **BrokenPipeError**
                * **ConnectionAbortedError**
                * **ConnectionRefusedError**
                * **ConnectionResetError**
            * **FileExistsError** - попытка создания файла или директории, которая уже существует.
            * **FileNotFoundError** - файл или директория не существует.
            * **InterruptedError** - системный вызов прерван входящим сигналом.
            * **IsADirectoryError** - ожидался файл, но это директория.
            * **NotADirectoryError** - ожидалась директория, но это файл.
            * **PermissionError** - не хватает прав доступа.
            * **ProcessLookupError** - указанного процесса не существует.
            * **TimeoutError** - закончилось время ожидания.
        * **ReferenceError** - попытка доступа к атрибуту со слабой ссылкой.
        * **RuntimeError** - возникает, когда исключение не попадает ни под одну из других категорий.
        * **NotImplementedError** - возникает, когда абстрактные методы класса требуют переопределения в дочерних классах.
        * **SyntaxError** - синтаксическая ошибка.
            * **IndentationError** - неправильные отступы.
                * **TabError** - смешивание в отступах табуляции и пробелов.
        * **SystemError** - внутренняя ошибка.
        * **TypeError** - операция применена к объекту несоответствующего типа.
        * **ValueError** - функция получает аргумент правильного типа, но некорректного значения.
        * **UnicodeError** - ошибка, связанная с кодированием / раскодированием unicode в строках.
            * **UnicodeEncodeError** - исключение, связанное с кодированием unicode.
            * **UnicodeDecodeError** - исключение, связанное с декодированием unicode.
            * **UnicodeTranslateError** - исключение, связанное с переводом unicode.
        * **Warning** - предупреждение.

### Как узнать какие исключения может выпускать функция?

**Все пропускаемые исключения обязаны быть описаны в документации.**

Цитата из документации по встроенной функции open:

open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

Open file and return a corresponding file object. If the file cannot be opened, an OSError is raised.
