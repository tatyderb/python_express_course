# Перегрузка операторов

Мы можем легко найти минимальное число, сумму чисел или отсортировать последовательность:
```python
>>> a = [3, 7, -1, 10]
>>> min(a)
-1
>>> sorted(a)
[-1, 3, 7, 10]
>>> sum(a)
19
```
Хочется, чтобы эти функции работали и для классов. Для этого нужно, чтобы классы умели сравнивать < (для min и sorted), и складывать через + (для sum).

Мы научились, чтобы `print` могла печатать экземпляры класса. Для этого мы в классе пишем функцию **\_\_str\_\_(self)**.
Если есть класс А, и `x = A()` - экземпляр класса А, то при `print(x)` вызывается `str(x)`, которая вызывает `x.__str__()`
`print([x])` вызовет функцию `repr(x)`, которая вызовет `x.__repr__()`

То есть, если мы определим в классе функцию со специальным именем, он будет вызываться при выполнении операций над экземплярами класса.

Можно переопределить в классе функции, чтобы работали операторы:

| Специальная функция | Оператор | Значение |
|---|---|---|
| \_\_lt\_\_(self, other) | x &lt; y | Возвращает True, если х меньше, чем у |
| \_\_le\_\_(self, other) | x <= y | Возвращает True, если х меньше или равно у |
| \_\_eq\_\_(self, other) | x == y | Возвращает True, если х равно у |
| \_\_ne\_\_(self, other) | x != y | Возвращает True, если х НЕ равно у |
| \_\_gt\_\_(self, other) | x > y | Возвращает True, если х больше, чем у |
| \_\_ge\_\_(self, other) | x >= y | Возвращает True, если х больше или равно у |

| Специальная функция | Оператор | Коментарий |
|---|---|---|
| \_\_add\_\_(self, other) | x + y | |
| \_\_sub\_\_(self, other) | x - y | |
| \_\_mul\_\_(self, other) | x * y | |
| \_\_truediv\_\_(self, other) | x / y | |
| \_\_floordiv\_\_(self, other) | x // y |  |
| \_\_mod\_\_(self, other) | x % y |  |
| \_\_pow\_\_(self, other) | x \*\* y |  |

Вспомним умножение строки на число 'hi'\*3. Можно написать 3\*'hi', получим такой же результат.

Для того, чтобы написать функцию число \* строку, нужно переопределить для строки метод \_\_rmul\_\_ .

```python
some_object + other
```
Вызывает \_\_add\_\_()

```python
other + some_object
```
Вызывает \_\_radd\_\_(). У нее первый операнд other, а второй self.

Ее можно реализовать как:
```python
def __radd__(self, other):
    return __add__(other, self)
```

## Пример с точкой на плоскости XY

В классе Point (точка на плоскости ХУ) переопределим функции для == и для <
```python
class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return '({} {})'.format(self.x, self.y)
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __lt__(self, other):
        """ Меньше та точка, у которой меньше х. При одинаковых x, та, у которой меньше y."""
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
    
    # другие функции класса: move, dir, dist...
    
# Тестируем функции класса:
def test():
    p0 = Point(3, 5)
    p1 = Point(3, 5)
    p2 = Point(-1, 7)
    p3 = Point(3, 1.17)
    
    print('p0=', p0)       # 3 5
    print('p1=', p1)       # 3 5
    print('p2=', p2)       # -1 7
    print('p3=', p3)       # 3 1.17
    
    print('p0 == p1', p0 == p1) # True
    assert(p0 == p1)
    print('p1 == p2', p1 == p2) # False
    assert(not p1 == p2)
    
    print('p0 != p1', p0 != p1) # False
    assert(not(p0 != p1))
    print('p1 != p2', p1 != p2) # True
    assert(p1 != p2)
    
    print('p2 < p1', p2 < p1)   # True
    assert(p2 < p1)
    print('p1 < p2', p1 < p2)   # False
    assert(not(p1 < p2))

    print('p3 < p1', p3 < p1)   # True
    assert(p3 < p1)
    print('p1 < p3', p1 < p3)   # False
    assert(not (p1 < p3))
    
    a = [p0, p1, p2, p3]
    pmin = min(a)
    print('pmin =', pmin)
    assert(p2 == pmin)
    
    b = sorted(a)
    print(b)
    assert(b == [p2, p3, p0, p1])
    
test()
```
