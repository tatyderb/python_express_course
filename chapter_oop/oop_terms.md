# Объектно-ориентированное программирование

## Процедурный и объектно-ориентированный подход

Процедурный подход хорош для небольших (до 500 строк) проектов. Объектно-ориентированно программировать можно и на ассемблере. Но трудно. Удобнее программировать на языке, где есть для этого возможности.

Посмотрим, что есть в питоне для объектно-ориентированного подхода.

Рассмотрим окружности на плоскости ХУ.

Для задания окружности нужно задать координаты центра окружности x, y и ее радиус r. Для этого можно использовать обычный кортеж.
```python
circle = (1, 2, 15)
```
Проблемы:
* не очевидно, где тут радиус. Может быть (x, y, r), а может мы задавали (r, x, y)
* если есть функции `distance_from_origin(x, y)` (расстояние от начала координат до центра окружности) и `edge_distance_from_origin(x, y, radius)` (расстояние от начала координат до окружности), при обращении к ним нам нужно распаковывать кортеж (лишние операции):
```python
distance = distance_from_origin(*circle[:2])
distance = edge_distance_from_origin(*circle)
```
Решение: именованный кортеж (named tuple):

```python
import collections
Circle = collections.namedtuple("Circle", "x y radius")
circle = Circle(13, 84, 9)
distance = distance_from_origin(circle.x, circle.y)
```
Проблемы:

* можно создать кортеж с отрицательным радиусом (нет проверки значений) (при процедурном подходе эти проверки либо не делаются, либо требуют написания слишком много кода);
* tuple неизменяем, named tuple изменяем через метод collections.namedtuple_replace() (но код ужасает) `circle = circle._replace(radius=12)`

Решение:  взять коллекцию с изменяемыми значениями, например, list или dict.

```python
circle = [1, 2, 15]                  # list 
circle = dict(x=36, y=77, radius=8)  # dict
```
* list
  * нет доступа к circle\['x'\],
  * можно сделать circle.sort()
* dict - решает проблемы из list, но
  * еще нет защиты от отрицательного радиуса,
  * еще можно передать в функцию, которая не работает с окружностями (а, например, ждет прямоугольник).

Решение: сделать свой новый тип данных, который будет представлять окружность на ХУ плоскости.

## Новые типы данных

Новый тип данных в питоне называется **класс (class)**. Данные этого типа называются (как и раньше) **объектами** или **экземплярами класса (instance)**.

* **Класс** - это набор правил (способ создания и работы с однотипными объектами):
  * из каких переменных и данных состоит объект - **атрибуты** или **поля** - характеризуют состояние объекта;
  * что можно делать с экземпляром класса (поведение объекта) - **метод** или **функция** класса - могут менять состояние объекта.
  * **конструктор** - специальный метод, где описывается как создавать объект.
  
5 - это объект класса int. Для него определены арфиметические операции, его можно преобразовать в строку, его можно сделать из других объектов (строки, float).
"Hello" - это объект класса str. Строки можно складывать, брать из них срезы, находить в ней подстроку, и так далее.

As a noun, "AT-trib-ute" is pronounced with emphasis on the first syllable, as opposed to
"a-TRIB-ute", which is a verb.  (Downey, p 144).

## Создаем новый класс  

* Для создания класса используют ключевое слово **class**
* поля и методы пишут с **отступом**
* имя класса принято писать **с большой буквы**

Класс записывается так (будем использовать сегодня): 

```python
class ИмяКласса:
    'Описание для чего нужен класс - строка документации (можно не писать)'
    поля и методы класса
```

или так (будем использовать, когда начнем говорить о наследовании):

```python
class ИмяКласса(базовые классы через запятую):
    'Описание для чего нужен класс - строка документации (можно не писать)'
    поля и методы класса
```

_На самом деле, когда базовый класс не указывается явно, это класс **object**_

Самый простой класс (мы использовали для создания своего исключения):
```python
class MyOwnException(Exception):   # мой класс исключений наследуется от базового класса Exception
    pass                           # ничего дополнительного или особого он не делает, просто существует
```

Пример класса, описывающего окружности:

```python
from math import PI
class Circle:
    'Окружности на плоскости ХУ'
    # конструктор класса, вызывается когда создаем новый объект класса
    def __init__(self, x=0, y=0, r=1):
         self.x = x                     # все переменные ОБЪЕКТА указываются в конструкторе
         self.y = y
         self.r = r
   
    # методы объекта:
    def area(self):                     # первый аргумент всегда self
         return PI * self.r * self.r    # доступ к аргументам - только через self.

    def perimetr(self):                 # первый аргумент всегда self
         return 2*PI * self.r           # доступ к аргументам - только через self.

    def zoom(self, k):                  # увеличим окружность в k раз
         self.r *= k

    def is_crossed(self, c):            # пересекается или нет эта окружность с окружностью с?
        d2 = (self.x - c.x)**2 + (self.y - c.y)**2
        r2 = (self.r + c.r)**2
        return d2 <= r2
        
    def __str__(self):
        return 'Circle x={} у={} r={}, area={}'.format(self.x, self.y. self.r, self.area())
        # обратите внимание на вызов self.area() - вызываем другой метод этого объекта тоже через self

# тут можно уже создавать объекты класса и их использовать
```

* **\_\_init\_\_(self, другие аргументы через запятую)** - конструктор класса (не совсем так, там еще есть \_\_new\_\_, но об этом подробнее в наследовании и переопределении методов).
* **self** - ссылка на себя, через нее доступаемся к атрибутам (полям и методам)

**self.метод - вызов другого метода класса**

**self** - первый аргумент методов экземпляра класса.

## Создание объекта (экземпляра класса)

```python
с = Circle(1, 2, 3)
```
* Создается экземпляр класса Circle - окружность с центром в точке (1, 2) и радиусом 3
* ссылка на нее записывается в переменную `c`

## Доступ к полям и методам

**ссылка_на_объект.поле**

**ссылка_на_объект.метод**

```python
c = Circle()
c.x = 1
c.y = 2
c.r = 3
a = c.area()    # у объекта, на который ссылается с, вызвали метод area
```

## Объекты и ссылки (повторение - мать учения)

```python
c = Circle()            # создали единичную окружность с центром в (0,0), на нее ссылается с
c.x = 1                 # эта окружность стала радиусом 3 с центром в (1, 2)
c.y = 2
c.r = 3
a = c.area()            # у объекта, на который ссылается с, вызвали метод area

d = Circle(5, 6, 2.5)   # создали окружность радиуса 2.5 с центром в (5, 6), на нее ссылается d
a = c.area() + d.area() # площадь окружности, на которую ссылается с и площадь окружности, на которую ссылается d

c = d                   # теперь c ТОЖЕ ссылается на вторую окружность, ссылок на первую окружность нет
```

**c = d** - это присвоение ссылок на объекты.

Что будет напечатано?

```python
c = Circle()
d = Circle()
c.x = 1
d.x = 6
print('c.x = ', c.x)
print('d.x = ', d.x)

c = d
print('c.x = ', c.x)
print('d.x = ', d.x)
```

## Функция возвращает объект



## Method overloading

Можно ли создать в питоне методы класса с одинаковыми именами?

Нет. В python так не пишут.

Вы можете использовать значения по умолчанию, \*args и \*\*kargs - в питоне есть другие механизмы для того же результата.

Можно использовать декоратор `@overload`, но о декораторах расскажем позже.

## Термины (заключение)

* **Модель** - упрощенное описание

* **Объект**:
  * Переменные (характеризуют состояние объекта)
  * Методы (могут состояния менять)

* **Класс** – способ задания однотипных объектов
  * прототип объекта (его переменные)
  * метод создания из прототипа конкретного объекта

Еще раз "на пальцах":
* Класс - **шаблон** объекта,
* Объект - **экземпляр** класса.

## Термины на английском языке

Понадобятся при поиске в интернете.

https://www.tutorialspoint.com/python/python_classes_objects.htm

**Class** - A user-defined prototype for an object that defines a set of attributes that characterize any object of the class. The attributes are data members (class variables and instance variables) and methods, accessed via dot notation.

**Class variable** - A variable that is shared by all instances of a class. Class variables are defined within a class but outside any of the class's methods. Class variables are not used as frequently as instance variables are.

**Data member** - A class variable or instance variable that holds data associated with a class and its objects.

**Function overloading** - The assignment of more than one behavior to a particular function. The operation performed varies by the types of objects or arguments involved.

**Instance variable** - A variable that is defined inside a method and belongs only to the current instance of a class.

**Inheritance** - The transfer of the characteristics of a class to other classes that are derived from it.

**Instance** - An individual object of a certain class. An object obj that belongs to a class Circle, for example, is an instance of the class Circle.

**Instantiation** - The creation of an instance of a class.

**Method** - A special kind of function that is defined in a class definition.

**Object** - A unique instance of a data structure that's defined by its class. An object comprises both data members (class variables and instance variables) and methods.

**Operator overloading** - The assignment of more than one function to a particular operator.

# Задачи



## Uno card game (на дом)

Добавить карты +2, skip, wild, wild+4