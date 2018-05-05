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
