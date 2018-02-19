# Инкапсуляция

**В python НЕТ возможности полностью ограничить доступ к переменным объекта и класса**

Если вы изучали другие ООП-языки, то можете считать, что все поля в питоне public, а все методы virtual.

## @property - определяем get, set, del функции

Хочется read-only атрибуты.

Хочется, чтобы set методы для атрибута обязательно вызывались, запретить прямое присваивание obj.x = 7.

```property([fget[, fset[, fdel[, doc]]]]) -> property ```

* *fget* : Функция, реализующая возврат значения свойства.
* *fset* : Функция, реализующая установку значения свойства.
* *fdel* : Функция, реализующая удаление значения свойства.
* *doc* : Строка документации для создаваемого свойства. Если не задано , будет использовано описание от fget (если оно существует).

Позволяет использовать методы в качестве свойств объектов — порождает дескриптор, позволяющий создавать «вычисляемые» свойства (тип property).

Пример использования в классическом виде:
```python
class Mine(object):

    def __init__(self):
        self._x = None

    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value

    def del_x(self):
        self._x = 'No more'

    x = property(get_x, set_x, del_x, 'Это свойство x.')

type(Mine.x)  # property
mine = Mine()
mine.x        # None
mine.x = 3
mine.x        # 3
del mine.x  
mine.x        # No more
```

Используя функцию в качестве декоратора можно легко создавать вычисляемые свойства только для чтения:

```python
class Mine(object):

    def __init__(self):
        self._x = 'some value'

    @property
    def prop(self):
        return self._x

mine = Mine()
mine.prop                  # some value
mine.prop = 'other value'  # AttributeError

del mine.prop              # AttributeError
```
Объект свойства также предоставляет методы getter, setter, deleter, которые можно использовать в качестве декораторов для указания функций реализующих получение, установку и удаление свойства соответственно. Следующий код эквивалентен коду из первого примера:

```python
class Mine(object):

    def __init__(self):
        self._x = None

    x = property()

    @x.getter
    def x(self):
        """Это свойство x."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        self._x = 'No more'
```


## \_\_slots\_\_

Можно запретить создание атрибута объекта используя \_\_slots\_\_

```python
class Robot():
  __slots__ = ['a', '_b', '__c']
  def __init__(self):
    self.a = 123
    self._b = 123
    self.__c = 123
 
obj = Robot()
print(obj._Robot__c)    # 123 - все еще можем доступиться до атрибута по полному имени
obj.__c = 77            # УРА! AttributeError: 'Robot' object has no attribute '__c'
print(obj.a)
print(obj._b)
print(obj.__c)          
```

Нельзя создать атрибут объекта, не перечисленный в \_\_slots\_\_

## Переопределение \_\_setattr\_\_

```python
class Robot(object):
   def __init__(self):
      self.a = 123
      self._b = 123
      
   def __setattr__(self, name, val):
      if name not in ('a', '_b'):
            raise AttributeError(name)
      super().__setattr__(name, val)
 
obj = Robot()
obj.a = 5
print(obj.a)
obj.__c = 77       # AttributeError
print(obj.__c)     # AttributeError
```

Аналогично можно переопределить другие функции доступа к атрибутам.