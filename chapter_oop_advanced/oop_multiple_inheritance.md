# ������������� ������������

��� �������� ������ ����� ������� ����� ������ �������� ������.

��� ������ ��������� ������������� ������� ��������� � ��������� ������ ����� �������, ���� �� ������ ����������.

��� ��� ���� ������� ������ ����� ���� ������������ ������ �������, �������� ������ (�� � �������� ������) ������������.

������� � ������ ���������:

* ������ ������ - ����� ��������� ������� ������������ �� ����������� ����� ����� ����� ���������� ������, ������ �� ������� ������ ������������, � ����� ����� �������.
* ����� ������ (� Python 3 ��� ������ �����) - ����� � ������ (��. ������ ��� super() � mro()).

## ������ �������������� ������������ ��� ���������� \_\_repr\_\_

����: �������� 1 �����, ������� ����� ������������� ������� \_\_repr\_\_ ��� ������������� ������ � ������������ ���.

����� ListInstance � ����� lister.py: ������� ������ ��������� ����������.

```python
class ListInstance(object):
    def __str__(self):
        return '<Instance of {}, id = {}>:\n{}'.format(
                    self.__class__.__name__,    # ��� ������ ��������� �������
                    id(self),
                    self.__attrnames()          # ������ ��� ������� - ��������
                )
                
    def __attrnames(self):
        """������ ��� ������� - �������� ������� � ���� ������ � ��������"""
        return '\n'.join(('\tname {} = {}'.format(attr, self.__dict__[attr]) for 
                            attr in sorted(self.__dict__)))
```
�������������:
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
����������:
```python
<Instance of ListInstance, id = 4292312080>:

<Instance of B, id = 4292312240>:
        name bzz = <bound method B.bzz of <__main__.B object at 0xffd77e10>>
        name foo = <bound method A.foo of <__main__.B object at 0xffd77e10>>
        name x = 1
        name y = 2
```

����� \_\_attrnames() ������ � \_\_, ����� �� � ����� ������ �� ��� ��������� ����� � ����� �� ������� (��� �� ��������������� � \_���������\_\_��������� ��� � ������ ��������, ������������ � \_\_ (�� �� �������������� �� \_\_).

��������������� �������� ���� ����� ����������:
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

������������ ����� ���������� \_\_str\_\_:
* ���������� ������ ������� � ����� �����, �� ����� ��������������� ��������;
* ����� ������������ � ��������� �������.

### ������� ����� ListInstance (��� ��������, ������ � ������������)

�����, ����� print(x) �������� ��� ����������� �������� (����� �����������, ������������ � �������������� \_\_).

��� ����� ������� ����� \_\_dir\_\_ �� dir() - ������� �������� ���� ������� � ����� �������� �������� ����� ��������, ������� self.\_\_dir\_\_\[attr\] �� getattr(self, attr), ������� ����� ������ � ������ ������������:

```python
class ListInstance(object):
    def __str__(self):
        return '<Instance of {}, id = {}>:\n{}'.format(
                    self.__class__.__name__,    # ��� ������ ��������� �������
                    id(self),
                    self.__attrnames()          # ������ ��� ������� - ��������
                )
                
    def __attrnames(self):
        """������ ��� ������� - �������� ������� � ���� ������ � ��������"""
        return '\n'.join(('\tname {} = {}'.format(
                            attr, 
                            '<>' if attr.startswith('__') and attr.endswith('__') else getattr(self, attr)
                            ) 
                            for attr in sorted(dir(self)) 
                        ))
```
�������:
```python
<Instance of B, id = 4292312336>:
        name _ListInstance__attrnames = <bound method ListInstance.__attrnamesf <__main__.B object at 0xffd77d10>>
        name __class__ = <>
        .... ��� �����-����� ������� ���� __�����__ .....
        name __str__ = <>
        name bzz = <bound method B.bzz of <__main__.B object at 0xffd77e10>>
        name foo = <bound method A.foo of <__main__.B object at 0xffd77e10>>
        name x = 1
        name y = 2
```

### ������

* �������� ��������, ������ �� �� �������;

# ������������� ������� ��������

������ �� ����� ���������� ����������, ����� ������� ����� ���������.

��� �������� �������� "�� ����������", ���������� ������ �������������� �������.

������� ������� factory, ������� ������� ������ ������� ������ � ���������� �����������:

```python
def factory(aClass, *args): # ������ � ���������� ������ ����������
    return aClass(*args)    # ����� aClass 
    
class Spam:
    def doit(self, message):
        print(message)
class Person:
    def __init__(self, name, job):
        self.name = name
        self.job = job
        
object1 = factory(Spam)                     # ������� ������ Spam
object2 = factory(Person, 'Guido', 'guru')  # ������� ������ Person
```
����� ������� factory �����:
```python
def factory(aClass, *args, **kwargs):       # +kwargs
    return aClass(*args, **kwargs)          # ������� aClass
```

