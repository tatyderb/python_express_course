# Имена и области видимости

Лутц p.783

mynames.py:
```python
X = 11 # Глобальное (в модуле) имя/атрибут (X, или manynames.X)

def f():
    print(X) # Обращение к глобальному имени X (11)

def g():
    X = 22 # Локальная (в функции) переменная (X, скрывает имя X в модуле)
    print(X)
    
class C:
    X = 33 # Атрибут класса (C.X)
    def m(self):
        X = 44 # Локальная переменная в методе (X)
        self.X = 55 # Атрибут экземпляра (instance.X)    
```

# Встроенные атрибуты класса

https://www.tutorialspoint.com/python/python_classes_objects.htm

* \_\_dict\_\_ - Dictionary containing the class's namespace.
* \_\_doc\_\_ - Class documentation string or none, if undefined.
* \_\_name\_\_ - Class name.
* \_\_module\_\_ - Module name in which the class is defined. This attribute is "\_\_main\_\_" in interactive mode.
* \_\_bases\_\_ - A possibly empty tuple containing the base classes, in the order of their occurrence in the base class list.

```python
#!/usr/bin/python

class Employee:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self):
     print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary

print "Employee.__doc__:", Employee.__doc__
print "Employee.__name__:", Employee.__name__
print "Employee.__module__:", Employee.__module__
print "Employee.__bases__:", Employee.__bases__
print "Employee.__dict__:", Employee.__dict__
```
Получаем:
```
Employee.__doc__: Common base class for all employees
Employee.__name__: Employee
Employee.__module__: __main__
Employee.__bases__: ()
Employee.__dict__: {'__module__': '__main__', 'displayCount':
<function displayCount at 0xb7c84994>, 'empCount': 2, 
'displayEmployee': <function displayEmployee at 0xb7c8441c>, 
'__doc__': 'Common base class for all employees', 
'__init__': <function __init__ at 0xb7c846bc>}
```