class A(object):
    def spam(self):
        print('A.spam')
        super().spam()

class B(object):
    def spam(self):
        print('B.spam')
        
class C(A, B):
    pass

x = A()
#x.spam()

y = C()
y.spam()
print(C.__mro__)
