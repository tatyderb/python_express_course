# Источники

* [python3 tutorial](https://docs.python.org/3/tutorial/modules.html#)
* [pep-328 Absolute and Relative Imports](https://docs.python.org/2.5/whatsnew/pep-328.html)
* []()
* []()
  
# Запуск 

Для каждого файла определена переменная \_\_name\_\_, в которой определяется как этот файл выполняется - как подгружаемый модуль или как отдельная программа.

Пусть у нас есть файл fibo.py с функцией fib, который печатает свою переменную \_\_name\_\_

Импортируем его в интерактивном интерпретаторе:
```python
>>> import fibo
>>> fibo.__name__
'fibo'
```
Запустим его как отдельную программу:
```python
$python fibo.py
__main__
```
То есть если хочется выполнять код только в режиме программы, то пишем:
```python
if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))
```

