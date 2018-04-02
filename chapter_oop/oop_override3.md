# Атрибуты и ограничение доступа через переопределение операторов

## Обращение к атрибутам \_\_getattr\_\_ и \_\_setattr\_\_

**\_\_getattr\_\_** - получить ссылку на атрибут.

НЕ вызывается, если интерпретатор может найти атрибут в дереве наследования.

Вызывается, если пытается получить ссылку на _неопределенный_ (несуществующий) атрибут.
Атрибут вычисляется **динамически**.

Сделаем класс, который ведет себя так, как у его экземпляров есть атрибут age и нет других атрибутов.

```python
>>> class empty:
... def __getattr__(self, attrname):
...     if attrname == 'age':
...         return 40
...     else:
...         raise AttributeError, attrname
...
>>> x = empty()
>>> x.age
40
>>> x.name
...текст сообщения об ошибке опущен...
AttributeError: name
```

**\_\_setattr\_\_** - вызывается **всегда**, когда пишем `self.atr = value`. 

Вызывается `self.__setattr__('atr', value)`

Если внутри этого метода нужно сделать `self.name = x`, то не пишите так (получите бесконечный цикл рекурсивных вызовов), а пишите `self.__dict__['name'] = x`

```python
>>> class accesscontrol:
... def __setattr__(self, attr, value):
...     if attr == 'age':
...         self.__dict__[attr] = value
...     else:
...         raise AttributeError, attr + ' not allowed'
...
>>> x = accesscontrol()
>>> x.age = 40              # Вызовет метод __setattr__
>>> x.age
40
>>> x.name = 'mel'
...текст сообщения об ошибке опущен...
AttributeError: name not allowed
```

Как еще управлять атрибутами (см. позже):
* \_\_getattribute\_\_ - обращение к любым атрибутам (даже уже существующим). Пишем обращение к атрибуту так же, как в \_\_setattr\_\_, чтобы избежать рекурсии: `self.__dict__['name'] = x`
* функция `property`() 
* _дескрипторы_ связывают методы \_\_get\_\_ и \_\_set\_\_ с доступом к нужным атрибутам класса.

Пример: ограничиваем права доступа через \_\_setattr\_\_
```python
class PrivateExc(Exception): pass               # Создали пользовательское исключение
class Privacy:
    def __setattr__(self, attrname, value):     # Вызывается self.attrname = value
        if attrname in self.privates:
            raise PrivateExc(attrname, self)
        else:
            self.__dict__[attrname] = value     # ибо self.attrname = value будет рекурсивно вызывать __setattr__

class Test1(Privacy):
    privates = ['age']
    
class Test2(Privacy):
    privates = ['name', 'pay']
    def __init__(self):
        self.__dict__['name'] = 'Tom'
        
x = Test1()
y = Test2()
x.name = 'Bob'
y.name = 'Sue'          # <== ошибка
y.age = 30
x.age = 40              # <== ошибка
```
Полная реализация будет позже.
