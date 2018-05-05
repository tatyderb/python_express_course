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

## Диагностика segmentation faults

Что-то пошло не так и программа упала. Хочется получить информативный trace падения. Воспользуемся модулем **faulthandler**

Из кода питона:
```python
import faulthandler
faulthandler.enable()
```
или запустим питон с опцией `-Xfaulthandler`:
```python
bash % python3 -Xfaulthandler program.py
```
или определите переменную окружения **PYTHONFAULTHANDLER**.

Если ваша программа с использованием С-кода упала, вы получите сообщение вида:
```python
Fatal Python error: Segmentation fault
Current thread 0x00007fff71106cc0:
File "example.py", line 6 in foo
File "example.py", line 10 in bar
File "example.py", line 14 in spam
File "example.py", line 19 in <module>
Segmentation fault
```
Далее воспользуйтесь питон дебагером **pdb** и С-дебагером (например, gdb) для исследования С-части.

It should be noted that certain kinds of errors in C may not be easily recoverable. For
example, if a C extension trashes the stack or program heap, it may render faulthan
dler inoperable and you’ll simply get no output at all (other than a crash). Obviously,
your mileage may vary.