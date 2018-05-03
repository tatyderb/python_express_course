# Инкапсуляция

**В python НЕТ возможности полностью ограничить доступ к переменным объекта и класса**

Если вы изучали другие ООП-языки, то можете считать, что все поля в питоне public, а все методы virtual.

## Еще раз об \_\_name

**mangling** - изменение имен, чтобы имена имели принадлежность к *классу*. Это делается не столько для ограничения доступа к именам, а чтобы не было конфликта имен переменных в разных классах.

**Имена внутри инструкции class, которые начинаются с \_\_, но не заканчиваются на \_\_ автоматически расширяются именем класса**.

Зачем нужно? Делаем класс С3, который наследует классы С1 и С2. В обоих классах есть атрибут х:
```python
class C1:
    def meth1(self): self.X = 88    # Предполагается, что X - это мой атрибут
    def meth2(self): print(self.X)
class C2:
    def meth1(self): self.X = 99    # и мой тоже
    def meth2(self): print(self.X)
class C3(C1, C2): 
    pass

I = C3() # У меня только один атрибут X!
```
Значение self.X зависит от того, кто последний присвоил значение в этот атрибут, ибо _он один_.

Используем псевдочастотные имена для предотвращения конфликтов:
```python
class C1:
    def meth1(self): self.__X = 88      # Теперь X - мой атрибут
    def meth2(self): print(self.__X)    # Превратится в _C1__X
class C2:
    def metha(self): self.__X = 99      # И мой тоже
    def methb(self): print(self.__X)    # Превратится в _C2__X
class C3(C1, C2): pass

I = C3()                                # В I два имени __X (с именами классов)
I.meth1(); I.metha()
print(I.__dict__)
I.meth2(); I.methb()
```

Внимание: псевдочастотные имена мы создаем еще **при разработке классов С1 и С2**. При создании класса С3 мы пользуемся результатом правильного создания. Позволяет избежать _случайных_ конфликтов.

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