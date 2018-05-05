## CTypes

Самый простой способ - [ctypes](https://docs.python.org/3.6/library/ctypes.html)

* Плюс: не нужно изменять С-код. 

Проверьте, что библиотека и ваш интерпретатор питона собраны для одной и той же архитектуры, у них совпадает размер машинного слова и тп.

С-совместимые типы данных и функции для загрузки DLL.

### Таблица типов

| ctypes type | C type | Python type |
|---|---|---|
| c\_bool | \_Bool | bool |
| c\_char | char | 1-character bytes object |
| c\_wchar | wchar\_t | 1-character string |
| c\_byte | char | int |
| c\_ubyte | unsigned char | int |
| c\_short | short | int |
| c\_ushort | unsigned short | int |
| c\_int | int | int |
| c\_uint | unsigned int | int |
| c\_long | long | int |
| c\_ulong | unsigned long | int |
| c\_longlong | \_\_int64 or long long | int |
| c\_ulonglong | unsigned \_\_int64 or unsigned long long | int |
| c\_size\_t | size\_t | int |
| c\_ssize\_t | ssize\_t or Py\_ssize\_t | int |
| c\_float | float | float |
| c\_double | double | float |
| c\_longdouble | long double | float |
| c\_char\_p | char * (NUL terminated) | bytes object or None |
| c\_wchar\_p | wchar\_t * (NUL terminated) | string or None |
| c\_void\_p | void * | int or None |

### Пример: сумма 2 чисел на языке С:
```c
// Простой C-файл - суммируем целые и действительные числа

int add_int(int, int);
float add_float(float, float);

int add_int(int num1, int num2){
    return num1 + num2;
}

float add_float(float num1, float num2){
    return num1 + num2;
}
```
Скомпилируем файл в библиотеку .so (.dll под Windows). Получим adder.so.
```python
# Для Linux
$  gcc -shared -Wl,-soname,adder -o adder.so -fPIC add.c

# Для Mac
$ gcc -shared -Wl,-install_name,adder.so -o adder.so -fPIC add.c
```
Код на питоне:
```python
from ctypes import *

# Загружаем библиотеку
adder = CDLL('./adder.so')

# Находим сумму целых чисел
# Самый простой случай - аргументы по умолчанию int и возвращается по умолчанию int
res_int = adder.add_int(4,5)
print("Сумма 4 и 5 = " + str(res_int))

# Находим сумму действительных чисел
# нужно описать типы аргументов и возвращаемого значения
a = c_float(5.5)
b = c_float(4.1)

add_float = adder.add_float
add_float.restype = c_float
print("Сумма 5.5 и 4.1 = " + str(add_float(a, b)))
```
запускаем и получаем:
```python
Сумма 4 и 5 = 9
Сумма 5.5 и 4.1 = 9.600000381469727
```

### Пример sample.c

Пусть shared library собрана и помещена в той же директории, что и питоновский файл.

Напишем питоновский модуль-обертку для этой библиотеки:
```python
# sample.py
import ctypes
import os

# Try to locate the .so file in the same directory as this file
_file = 'libsample.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
_mod = ctypes.cdll.LoadLibrary(_path)

# int gcd(int, int)
gcd = _mod.gcd
gcd.argtypes = (ctypes.c_int, ctypes.c_int)
gcd.restype = ctypes.c_int

# int in_mandel(double, double, int)
in_mandel = _mod.in_mandel
in_mandel.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_int)
in_mandel.restype = ctypes.c_int

# int divide(int, int, int *)
# напишем функцию-обертку, которая возвращает два значения
_divide = _mod.divide
_divide.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
_divide.restype = ctypes.c_int
def divide(x, y):
    rem = ctypes.c_int()
    quot = _divide(x, y, rem)
    return quot,rem.value

# void avg(double *, int n)
# Define a special type for the 'double *' argument
class DoubleArrayType:
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, ctypes.Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from array.array objects
    def from_array(self, param):
        if param.typecode != 'd':
            raise TypeError('must be an array of doubles')
        ptr, _ = param.buffer_info()
        return ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double))

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((ctypes.c_double)*len(param))(*param)
        return val
        
    from_tuple = from_list

    # Cast from a numpy array
    def from_ndarray(self, param):
        return param.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    
DoubleArray = DoubleArrayType()

_avg = _mod.avg
_avg.argtypes = (DoubleArray, ctypes.c_int)
_avg.restype = ctypes.c_double
def avg(values):
    return _avg(values, len(values))
    
# struct Point { }
class Point(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_double),
        ('y', ctypes.c_double)
    ]
# double distance(Point *, Point *)
distance = _mod.distance
distance.argtypes = (ctypes.POINTER(Point), ctypes.POINTER(Point))
distance.restype = ctypes.c_double
```
Теперь можно использовать эти питоновские функции, импортируя модуль-обертку:
```python
>>> import sample
>>> sample.gcd(35,42)
7
>>> sample.in_mandel(0,0,500)
1
>>> sample.in_mandel(2.0,1.0,500)
0
>>> sample.divide(42,8)
(5, 2)
>>> sample.avg([1,2,3])
2.0
>>> p1 = sample.Point(1,2)
>>> p2 = sample.Point(4,5)
>>> sample.distance(p1,p2)
4.242640687119285
```

#### Где расположена библиотека?
Библиотека должна лежать в том месте, где питоновский код может ее найти. Как вариант, можем положить ее в той же директории. В примере эта директория добывается из переменной `__file__`.

Если в другом месте - настраивайте пути поиска.

Если вы хотите взять стандартную библиотеку, то можно использовать функцию **ctypes.util.find_library()**

```python
>>> from ctypes.util import find_library
>>> find_library('m')
'/usr/lib/libm.dylib'
>>> find_library('pthread')
'/usr/lib/libpthread.dylib'
>>> find_library('sample')
'/usr/local/lib/libsample.so'
```

Библиотека загружается функцией **ctypes.cdll.LoadLibrary**(_path_), которой передают путь к библиотеке.

#### Спецификация типов аргументов и возвращаемого значения

Некоторые функции можно определить один-в-один:
```python
# int in_mandel(double, double, int)
in_mandel = _mod.in_mandel
in_mandel.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_int)
in_mandel.restype = ctypes.c_int
```

#### Передача целочисленных переменных по указателю (изменение нескольких значений)

Некоторые содержат приемы, которые не работают в питоновском коде и "питонично" писать по-другому. 

В функции divide() частное возвращается, а остаток записывается в переменную, адрес которой передан последним аргументом. Если мы переведем слово-в-слово, то код не будет работать:
```python
>>> divide = _mod.divide
>>> divide.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
>>> x = 0
>>> divide(10, 3, x)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
ctypes.ArgumentError: argument 3: <class 'TypeError'>: expected LP_c_int instance instead of int
```
int - это неизменяемые объекты в питоне, поэтому по адресу не удается поменять значение.

Чтобы код заработал, нужно сделать x нужного типа. 
```python
>>> x = ctypes.c_int()
>>> divide(10, 3, x)
3
>>> x.value
1
```
В функцию передается ссылка на объект типа c_int, который содержит мутабельные целые числа. Полученное число лежит в поле value.

Но лучше написать "питоническую" функцию-обертку, которая в питоновском стиле вернет кортеж из частного и остатка. И далее использовать эту функцию divide.

```python
# int divide(int, int, int *)
_divide = _mod.divide
_divide.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
_divide.restype = ctypes.c_int

def divide(x, y):
    rem = ctypes.c_int()
    quot = _divide(x,y,rem)
    return quot, rem.value
```

#### Массивы

Функция avr хочет получить массив дробных чисел. Но что есть "массив" в питоне? Список? Кортеж? Массив numpy? Массив из модуля array? 

Для обработки всех этих возможностей сделан класс DoubleArrayType. Метод **from_param**() превращает питоновский тип в подходящий объект ctypes (например, в указатель на ctypes.c_double). Вы пишите его так, как вам хочется.

Цитата из документации по ctypes:

If you have defined your own classes which you pass to function calls, you have to implement a from\_param() class method for them to be able to use them in the argtypes sequence. The from\_param() class method receives the Python object passed to the function call, it should do a typecheck or whatever is needed to make sure this object is acceptable, and then return the object itself, its \_as\_parameter\_ attribute, or whatever you want to pass as the C function argument in this case. Again, the result should be an integer, string, bytes, a ctypes instance, or an object with an \_as\_parameter\_ attribute.

Для этого определяется тип передаваемого параметра и вызывается метод, который обрабатывает именно этот тип. Так для **списков и кортежей** питона вызывается метод from\_list (обратите внимание, как реализуется, что для кортежей вызывается тот же метод). from\_list() преобразует param в массив ctypes.

Пример преобразования списка в массив ctypes:
```python
>>> nums = [1, 2, 3]
>>> a = (ctypes.c_double * len(nums))(*nums)
>>> a
<__main__.c_double_Array_3 object at 0x10069cd40>
>>> a[0]
1.0
>>> a[1]
2.0
>>> a[2]
3.0
>>>
```

Для массивов из пакета **array** метод извлекает хранящийся внутри объекта адрес массива чисел. Смотрим, как можно его извлечь:

```python
>>> import array
>>> a = array.array('d',[1,2,3])
>>> a
array('d', [1.0, 2.0, 3.0])
>>> ptr, _ = a.buffer_info()
>>> ptr
4298687200
>>> ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double))
<__main__.LP_c_double object at 0x10069cd40>
```

Из **numpy.array** - как показано в from_ndarray().

Протестируем работу функции avr на разных типах массивов:
```python
>>> import sample
>>> sample.avg([1,2,3])
2.0
>>> sample.avg((1,2,3))
2.0
>>> import array
>>> sample.avg(array.array('d',[1,2,3]))
2.0
>>> import numpy
>>> sample.avg(numpy.array([1.0,2.0,3.0]))
2.0
```

#### Структуры

Для передачи структуры языка С сделаем класс, наследующий классу **ctypes.Structure** и определим соответствующие поля нужных типов:

```python
class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double),
                ('y', ctypes.c_double)]
```
Далее используем этот класс везде, где нужен экземпляр этой структуры:
```python
>>> p1 = sample.Point(1,2)
>>> p2 = sample.Point(4,5)
>>> p1.x
1.0
>>> p1.y
2.0
>>> sample.distance(p1,p2)
4.242640687119285
```

### Подключение стандартных библиотека
Стандартная MS С библиотека:
```python
>>> from ctypes import *
>>> print(windll.kernel32)  
<WinDLL 'kernel32', handle ... at ...>
>>> print(cdll.msvcrt)      
<CDLL 'msvcrt', handle ... at ...>
>>> libc = cdll.msvcrt      
>>>
```

**Note**:  Accessing the standard C library through cdll.msvcrt will use an outdated version of the library that may be incompatible with the one being used by Python. Where possible, use native Python functionality, or else import and use the msvcrt module.

На Linux:
```python
>>> cdll.LoadLibrary("libc.so.6")  
<CDLL 'libc.so.6', handle ... at ...>
>>> libc = CDLL("libc.so.6")       
>>> libc                           
<CDLL 'libc.so.6', handle ... at ...>
>>>
```

### Возвращаемое значение

Вызовем стандартную функцию strchr.

```python
>>> strchr = libc.strchr
>>> strchr(b"abcdef", ord("d"))  
8059983
>>> strchr.restype = c_char_p    # c_char_p is a pointer to a string
>>> strchr(b"abcdef", ord("d"))
b'def'
>>> print(strchr(b"abcdef", ord("x")))
None
>>>
```
Заметьте, когда нужно вернуть NULL, возвращается None.

Можно определить типы аргументов функции:
```python
>>> strchr.restype = c_char_p
>>> strchr.argtypes = [c_char_p, c_char]
>>> strchr(b"abcdef", b"d")
'def'
>>> strchr(b"abcdef", b"def")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ArgumentError: argument 2: exceptions.TypeError: one character string expected
>>> print(strchr(b"abcdef", b"x"))
None
>>> strchr(b"abcdef", b"d")
'def'
>>>
```

### Объект питона в виде аргумента

Определите в классе поле **\_as\_parameter\_**. В нем должен быть один из приемлемых типов: число, строка или байты.

If you don’t want to store the instance’s data in the `_as_parameter_` instance variable, you could define a property which makes the attribute available on request.

```python
>>> class Bottles:
...     def __init__(self, number):
...         self._as_parameter_ = number
...
>>> bottles = Bottles(42)
>>> printf(b"%d bottles of beer\n", bottles)
42 bottles of beer
19
>>>
```

### Итого о ctypes

Удобен для маленьких вставок. Для больших библиотек придется много времени тратить на написание как вызывать фукции (функции-обертки, классы).

Придется вникать в содержимое кода на С. Легко ошибиться с указателями и выйти за границы памяти.
