class A(object):
    def __init__(self, x):
        self.x = x
        
    def __str__(self):
        return str(self.x)
        
    @staticmethod
    def new_A(s):
        t = A(int(s))
        return t
        
    @staticmethod
    def common_foo(x, k):
        return x * k
        
    def a_foo(self, k):
        self.x = __class__.common_foo(self.x, k)
        
    def func_foo(x, k):
        return x * k

    def a_func_foo(self, k):
        self.x = __class__.func_foo(self.x, k)
        
a1 = A(1)
print('a1 =', a1)

a2 = A.new_A("2")
print('a2 =', a2)

z = A.common_foo(3, 4)
print('z =', z)

a1.a_foo(5)
print('a1 =', a1)

z = A.func_foo(3, 4)
print('z =', z)

a1.a_func_foo(5)
print('a1 =', a1)
