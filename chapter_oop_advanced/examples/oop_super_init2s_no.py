""" Проверим, нужно ли вызывать в конструкторе конструктор базового класса или он будет вызван неявно"""

class Base(object):
    def __init__(self):
        print('Base.__init__')
        
class A(Base):
    def __init__(self):
        #super().__init__()
        print('A.__init__')
        
class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A, B):
    def __init__(self):
        super().__init__()
        print('C.__init__')

#k = A()                     # Base.__init__
                            # A.__init__
x = C()                     # Base.__init__
                            # B.__init__ - вызваны конструкторы обоих базовых классов
                            # A.__init__ - порядок вызова 
                            # C.__init__
                            
print(C.__mro__)