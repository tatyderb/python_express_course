class A(object):
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        
class C(B):
    def spam(self):
        super().super().spam()

y = C()
y.spam()
print(C.__mro__)
