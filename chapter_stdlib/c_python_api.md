# С - расширения

## Источники

* [документация](https://docs.python.org/3/extending/building.html)
* [tutorialspoint](https://www.tutorialspoint.com/python/python_further_extensions.htm)
* [ctypes документация](https://docs.python.org/3.6/library/ctypes.html)
* [SWIG tutorial](http://www.swig.org/tutorial.html)
  * [SWIG on Windows](http://www.swig.org/Doc3.0/Windows.html)
* [C/Python API](https://docs.python.org/3/c-api/)

* [Intermediate python](https://lancelote.gitbooks.io/intermediate-python/content/book/python_c_extension.html)
* [SciPy cookbook](http://scipy-cookbook.readthedocs.io/items/idx_interfacing_with_other_languages.html)
* [Using C and Fortran code with Python](http://nbviewer.jupyter.org/github/jrjohansson/scientific-python-lectures/blob/master/Lecture-6A-Fortran-and-C.ipynb)
* [Numba vs. Cython: Take 2](http://nbviewer.jupyter.org/url/jakevdp.github.io/downloads/notebooks/NumbaCython.ipynb)
* Python cookbook, chapter 15, C extensions
* (Python Cookbook by David Ascher, Alex Martelli)[https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch16.html] Chapter 16. Extending and Embedding

## Зачем использовать вставки другого кода

* С работает быстрее;
* нужна конкретная библиотека на С и не хочется переписывать ее на питон;
* нужен низкоуровневый интерфейс управления ресурсами для работы с памятью и файлами.

## Что использовать для вызова С-функции

Один из механизмов:
* ctypes
* SWIG
* Python/C API

## Как сделать файл-библиотеку на языке С или С++

SWIG [FAQ](https://github.com/swig/swig/wiki/FAQ#shared-libraries)

## С-код, который мы будем дальше использовать

```python
/* sample.c */
#include <math.h>
/* Compute the greatest common divisor */
int gcd(int x, int y) {
    int g = y;
    while (x > 0) {
        g = x;
        x = y % x;
        y = g;
    }
    return g;
}
/* Test if (x0,y0) is in the Mandelbrot set or not */
int in_mandel(double x0, double y0, int n) {
    double x=0,y=0,xtemp;
    while (n > 0) {
        xtemp = x*x - y*y + x0;
        y = 2*x*y + y0;
        x = xtemp;
        n -= 1;
        if (x*x + y*y > 4) return 0;
    }
    return 1;
}
/* Divide two numbers */
int divide(int a, int b, int *remainder) {
    int quot = a / b;
    *remainder = a % b;
    return quot;
}
/* Average values in an array */
double avg(double *a, int n) {
    int i;
    double total = 0.0;
    for (i = 0; i < n; i++) {
        total += a[i];
    }
    return total / n;
}
/*A C data structure */
typedef struct Point {
    double x,y;
} Point;
/* Function involving a C data structure */
double distance(Point *p1, Point *p2) {
    return hypot(p1->x - p2->x, p1->y - p2->y);
}
```

* _gdc_ и _is\_mandel_ - простые функции от int и double, которые возвращают значения;
* _divide_ - возвращает, по сути, 2 числа - частное и записывает остаток от деления по указанному адресу;
* _avg_ - перебирает массив, переданный как указатель;
* _Point_ и _distance_ - работают со структурами.

Пусть прототипы функций файла `sample.c` заданы в `sample.h` и сам файл собран в библиотеку `libsample.so`.

## CTypes

Самый простой способ - [ctypes](https://docs.python.org/3.6/library/ctypes.html)

* Плюс: не нужно изменять С-код. 

Проверьте, что библиотека и ваш интерпретатор питона собраны для одной и той же архитектуры, у них совпадает размер машинного слова и тп.

С-совместимые типы данных и функции для загрузки DLL.

### Таблица типов

| ctypes type | C type | Python type |
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

Для массивов из пакета **array** метод извлекает собствено адрес массива чисел. Смотрим, как можно извлечь его из массива:

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



## SWIG

[SWIG on Windows](http://www.swig.org/Doc3.0/Windows.html)

В Simplified Wrapper and Interface Generator (SWIG) нужно написать отдельный файл, который описывает интерфейс. Этот файл будет передаваться в утилиту командной строки SWIG.

Обычно его не используют, ибо сложно. Но если у вас много языков, откуда нужно доступаться к С-коду, то используйте SWIG.

Пример из (SWIG tutorial)[http://www.swig.org/tutorial.html]

C-файл `example.c` содержит разные функции и переменные:
```python
#include <time.h>
double My_variable = 3.0;

int fact(int n) {
    if (n <= 1) return 1;
    else return n*fact(n-1);
}

int my_mod(int x, int y) {
    return (x%y);
}

char *get_time()
{
    time_t ltime;
    time(&ltime);
    return ctime(&ltime);
}
```

Файл, описывающий интерфейс `example.i`. Он не будет изменяться в зависимости от языка, на который вы хотите портировать свой C-код:

```python
/* example.i */
%module example
%{
/* Помещаем сюда заголовочные файлы или объявления функций */
extern double My_variable;
extern int fact(int n);
extern int my_mod(int x, int y);
extern char *get_time();
%}

extern double My_variable;
extern int fact(int n);
extern int my_mod(int x, int y);
extern char *get_time();
```
Компиляция (заметьте, питон 2.1, указывайте правильную директорию к вашему актуальному питону):
```python
unix % swig -python example.i
unix % gcc -c example.c example_wrap.c -I/usr/local/include/python2.1
unix % ld -shared example.o example_wrap.o -o _example.so
```

Python:
```python
>>> import example
>>> example.fact(5)
120
>>> example.my_mod(7,3)
1
>>> example.get_time()
'Sun Feb 11 23:01:07 1996'
>>>
```

## C/Python API

[C/Python API](https://docs.python.org/3/c-api/)

**Работает с объектами**

Пишем специальный C-код для работы с питоном.

Все объекты Python представляются как структуры PyObject и заголовочный файл `Python.h` предоставляет различные функции для работы с объектами. Например, если PyObject одновременно PyListType (список), то мы можем использовать функцию PyList_Size(), чтобы получить длину списка. Это эквивалентно коду len(some_list) в Python. Большинство основных функций/операторов для стандартных Python объектов доступны в C через Python.h.

### Пример

Давайте напишем С-библиотеку для суммирования всех элементов списка Python (все элементы являются числами).
Начнем с интерфейса, который мы хотим иметь в итоге. Вот Python-файл, использующий пока отсутствующую C-библиотеку:

```python
# Это не простой Python import addList это C-библиотека
import addList

l = [1,2,3,4,5]
print("Сумма элементов списка - " + str(l) + " = " +  str(addList.add(l)))
```

С-код `adder.c`:

```c
// Python.h содержит все необходимые функции, для работы с объектами Python
#include <Python.h>

// Эту функцию мы вызываем из Python кода
static PyObject* addList_add(PyObject* self, PyObject* args){

  PyObject * listObj;

  // Входящие аргументы находятся в кортеже
  // В нашем случае есть только один аргумент - список, на который мы будем
  // ссылаться как listObj
  if (! PyArg_ParseTuple( args, "O", &listObj))
    return NULL;

  // Длина списка
  long length = PyList_Size(listObj);

  // Проходимся по всем элементам
  int i, sum =0;
  for(i = 0; i < length; i++){
    // Получаем элемент из списка - он также Python-объект
    PyObject* temp = PyList_GetItem(listObj, i);
    // Мы знаем, что элемент это целое число - приводим его к типу C long
    long elem = PyInt_AsLong(temp);
    sum += elem;
  }

  // Возвращаемое в Python-код значение также Python-объект
  // Приводим C long к Python integer
  return Py_BuildValue("i", sum);
}

// Немного документации для 'add'
static char addList_docs[] =
    "add( ): add all elements of the list\n";

/*
Эта таблица содержит необходимую информацию о функциях модуля
<имя функции в модуле Python>, <фактическая функция>,
<ожидаемые типы аргументов функции>, <документация функции>
*/
static PyMethodDef addList_funcs[] = {
    {"add", (PyCFunction)addList_add, METH_VARARGS, addList_docs},
    {NULL, NULL, 0, NULL}
};

/*
addList имя модуля и это блок его инициализации.
<желаемое имя модуля>, <таблица информации>, <документация модуля>
*/
PyMODINIT_FUNC initaddList(void){
    Py_InitModule3("addList", addList_funcs,
                   "Add all the lists");
}
```

* Заголовочный файл `Python.h` содержит все требуемые типы (для представления типов объектов в Python) и определения функций (для работы с Python-объектами).
* Дальше мы пишем функцию, которую собираемся вызывать из Python. По соглашению, имя функции принимается {module-name}\_{function-name}, которое в нашем случае - addList\_add. Подробнее об этой функции будет дальше.
* Затем заполняем таблицу, которая содержит всю необходимую информацию о функциях, которые мы хотим иметь в модуле. Каждая строка относится к функции, последняя - контрольное значение (строка из null элементов).
Затем идёт блок инициализации модуля - PyMODINIT\_FUNC init{module-name}.

Функция addList_add принимает аргументы типа PyObject (args также является кортежем, но поскольку в Python всё является объектами, мы используем унифицированный тип PyObject). Мы парсим входные аргументы (фактически, разбиваем кортеж на отдельные элементы) при помощи PyArg\_ParseTuple(). Первый параметр является аргументом для парсинга. Второй аргумент - строка, регламентирующая процесс парсинга элементов кортежа args. Знак на N-ой позиции строки сообщает нам тип N-ого элемента кортежа args, например - 'i' значит integer, 's' - строка и 'O' - Python-объект. Затем следует несколько аргументов, где мы хотели бы хранить выходные элементы PyArg_ParseTuple(). Число этих аргументов равно числу аргументов, которые планируется передавать в функцию модуля и их позиционность должна соблюдаться. Например, если мы ожидаем строку, целое число и список в таком порядке, сигнатура функции будет следующего вида:
```python
int n;
char *s;
PyObject* list;
PyArg_ParseTuple(args, "isO", &n, &s, &list);
```
В данном случае, нам нужно извлечь только объект списка и сохранить его в переменной listObj. Затем мы используем функцию PyList\_Size() чтобы получить длину списка. Логика совпадает с len(some\_list) в Python.

Теперь мы итерируем по списку, получая элементы при помощи функции PyLint\_GetItem(list, index). Так мы получаем PyObject\*. Однако, поскольку мы знаем, что Python-объекты еще и PyIntType, то используем функцию PyInt\_AsLong(PyObj \*) для получения значения. Выполняем процедуру для каждого элемента и получаем сумму.
Сумма преобразуется в Python-объект и возвращается в Python-код при помощи Py\_BuildValue(). Аргумент "i" означает, что возвращаемое значение имеет тип integer.

В заключение мы собираем C-модуль. Сохраните следующий код как файл setup.py:
```python
# Собираем модули

from distutils.core import setup, Extension

setup(name='addList', version='1.0',\
      ext_modules=[Extension('addList', ['adder.c'])])
```
Запускаем:
```python
python setup.py install
```

Это соберёт и установит C-файл в Python-модуль, который нам требуется.

Теперь осталось только протестировать работоспособность:

```python
# Модуль, вызывающий C-код
import addList

l = [1,2,3,4,5]
print("Сумма элементов списка - " + str(l) + " = " +  str(addList.add(l)))
```

запускаем:
```python
Сумма элементов списка - [1, 2, 3, 4, 5] = 15
```

В итоге, как вы можете видеть, мы получили наше первое C-расширение, использующее Python.h API. Этот метод может показаться сложным, однако с практикой вы поймёте его удобство.

## Cython

* [cython.org](http://cython.org/)