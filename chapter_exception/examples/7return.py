def foo(a):
    b = [1, 2, 3]
    x = 5 / a
    y = b[a]
    print(x, a, y)
    
def bzz(a):
    try:
        foo(a)
        print('try')
        return 1
    except:
        print('ecxept')
        return 2
    else:
        print('else')
        return 3
    finally:
        print('finally')
        return 4
    return 5
    
print('bzz({})={}'.format(2, bzz(2)))
print('bzz({})={}'.format(0, bzz(0)))
print('bzz({})={}'.format(7, bzz(7)))
