import traceback
import sys

def foo(a):
    b = [1, 2, 3]
    x = 5 / a
    y = b[a]
    print(x, a, y)
    
def qqq(a):
    try:
        foo(a)
    except ZeroDivisionError:
        print('qqq: ZeroDivisionError')
        traceback.print_exc(file=sys.stdout)
    print('qqq: After try-ecxept block')
        
def bzz(a):
    try:
        qqq(a)
    except IndexError:
        print('bzz: IndexError')
        traceback.print_exc(file=sys.stdout)
    print('bzz: After try-ecxept block\n')

bzz(2)
        # 2.5 2 3
        # qqq: After try-ecxept block
        # bzz: After try-ecxept block
bzz(0)
        # qqq: ZeroDivisionError
        # qqq: After try-ecxept block
        # bzz: After try-ecxept block
bzz(7)
        # bzz: IndexError
        # bzz: After try-ecxept block
