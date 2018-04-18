""" Проверим, нужно ли вызывать в конструкторе конструктор базового класса или он будет вызван неявно"""

class Base(object):
    def __init__(self):
        print('Base.__init__')
        
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
        
class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')

class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')

k = A()                     # Base.__init__
                            # A.__init__
x = C()                     # Base.__init__
                            # A.__init__
                            # Base.__init__ - второй вызов
                            # B.__init__
                            # C.__init__