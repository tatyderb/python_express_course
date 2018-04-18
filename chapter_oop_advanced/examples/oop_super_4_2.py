class A(object):
    def spam(self):
        print('A.spam')

class B(A):
    pass

class C(B):
    def spam(self):
        super().spam()
        print('C.spam')

y = C()
y.spam()
print(C.__mro__)
