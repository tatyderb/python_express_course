""" Проверим, нужно ли вызывать в конструкторе конструктор базового класса или он будет вызван неявно"""

class A(object):
    def __init__(self, x=5):
        print('A.__init__')
        self.x = x
        
class B(A):
    def __init__(self, y=2):
        print('B.__init__')
        self.y = y

k = B(7)                    # B.__init__

print('k.y =', k.y)         # k.y = 7   
#print('k.x =', k.x)        # AttributeError: 'B' object has no attribute 'x'
    