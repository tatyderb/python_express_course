# Множественное наследование

При создании класса можно указать более одного базового класса.

При поиске атрибутов интерпретатор обходит указанные в заголовке классы слева направо, пока не найдет совпадение.

Так как сами базовые классы могут быть наследниками других классов, получаем дерево (не в терминах графов) наследования.

Разница в поиске атрибутов:

* старые классы - поиск атрибутов сначала продолжается по направлению снизу вверх всеми возможными путями, вплоть до вершины дерева наследования, а затем слева направо.
* новые классы (в Python 3 все классы новые) - поиск в ширину (см. раздел про super() и mro()).

## Пример множественного наследования для реализации \_\_repr\_\_

Идея: написать 1 класс, который будет реализовывать удобный \_\_repr\_\_ для произвольного класса и использовать его.

Класс ListInstance в файле lister.py: получим список атрибутов экземпляра.

```python
class ListInstance(object):
    def __str__(self):
        return '<Instance of {}, id = {}>:\n{}'.format(
                    self.__class__.__name__,    # имя класса реального объекта
                    id(self),
                    self.__attrnames()          # список пар атрибут - значение
                )
                
    def __attrnames(self):
        """Список пар атрибут - значение объекта в виде строки с отступом"""
        return '\n'.join(('\tname {} = {}'.format(attr, self.__dict__[attr]) for 
                            attr in sorted(self.__dict__)))
```
Использование:
```python
class A(object):
    def __init__(self, x):
        self.x = x
    def foo(self):
        pass
class B(A, ListInstance):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y
    def bzz(self):
        pass
x = ListInstance()
print(x)

b = B(1, 2)
print(b)
```
напечатает:
```python
<Instance of ListInstance, id = 4292312080>:

<Instance of B, id = 4292312240>:
        name bzz = <bound method B.bzz of <__main__.B object at 0xffd77e10>>
        name foo = <bound method A.foo of <__main__.B object at 0xffd77e10>>
        name x = 1
        name y = 2
```

Метод \_\_attrnames() сделан с \_\_, чтобы ни в каком классе не был определен метод с таким же методом (ибо он разворачивается в \_имякласса\_\_имяметода как и прочие атрибуты, начинающиеся с \_\_ (но не оканчивающиеся на \_\_).

Дополонительные атрибуты тоже будут напечатаны:
```python
>>> import lister
>>> class C(lister.ListInstance): pass
...
>>> x = C()
>>> x.a = 1; x.b = 2; x.c = 3
>>> print(x)
<Instance of C, address 40961776>:
    name a=1
    name b=2
    name c=3
```

Преимущества такой реализации \_\_str\_\_:
* реализация вывода сделана в одном месте, ее можно централизованно поменять;
* можно использовать в различных классах.

### Изменим класс ListInstance (все атрибуты, вместе с наследуемыми)

Хотим, чтобы print(x) печатало все наследуемые атрибуты (кроме специальных, начинающихся и оканчивающихся \_\_).

Для этого заменим вызов \_\_dir\_\_ на dir() - получим атрибуты всех классов и чтобы находили значение этого атрибута, заменим self.\_\_dir\_\_\[attr\] на getattr(self, attr), которая будет искать в дереве наследования:

```python
class ListInstance(object):
    def __str__(self):
        return '<Instance of {}, id = {}>:\n{}'.format(
                    self.__class__.__name__,    # имя класса реального объекта
                    id(self),
                    self.__attrnames()          # список пар атрибут - значение
                )
                
    def __attrnames(self):
        """Список пар атрибут - значение объекта в виде строки с отступом"""
        return '\n'.join(('\tname {} = {}'.format(
                            attr, 
                            '<>' if attr.startswith('__') and attr.endswith('__') else getattr(self, attr)
                            ) 
                            for attr in sorted(dir(self)) 
                        ))
```
получим:
```python
<Instance of B, id = 4292312336>:
        name _ListInstance__attrnames = <bound method ListInstance.__attrnamesf <__main__.B object at 0xffd77d10>>
        name __class__ = <>
        .... еще много-много методов вида __метод__ .....
        name __str__ = <>
        name bzz = <bound method B.bzz of <__main__.B object at 0xffd77e10>>
        name foo = <bound method A.foo of <__main__.B object at 0xffd77e10>>
        name x = 1
        name y = 2
```

### Задача

* Выводить атрибуты, разбив их по классам;

# Универсальные фабрики объектов

Иногда до этапа выполнения неизвестно, какие объекты нужно создавать.

Для создания объектов "по требованию", используют шаблон проектирования фабрика.

Сделаем функцию factory, которая создает объект нужного класса с указанными параметрами:

```python
def factory(aClass, *args): # Кортеж с переменным числом аргументов
    return aClass(*args)    # Вызов aClass 
    
class Spam:
    def doit(self, message):
        print(message)
class Person:
    def __init__(self, name, job):
        self.name = name
        self.job = job
        
object1 = factory(Spam)                     # Создать объект Spam
object2 = factory(Person, 'Guido', 'guru')  # Создать объект Person
```
Можно сделать factory гибче:
```python
def factory(aClass, *args, **kwargs):       # +kwargs
    return aClass(*args, **kwargs)          # Вызвать aClass
```

