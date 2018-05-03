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

## CTypes

Самый простой способ - [ctypes](https://docs.python.org/3.6/library/ctypes.html)

* Плюс: не нужно изменять С-код. 
* Минус: не работает с объектами (переменными типа структура).

С-совместимые типы данных и функции для загрузки DLL.

Пример: сумма 2 чисел на языке С:
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
res_int = adder.add_int(4,5)
print("Сумма 4 и 5 = " + str(res_int))

# Находим сумму действительных чисел
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
PyArg_ParseTuple(args, "siO", &n, &s, &list);
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