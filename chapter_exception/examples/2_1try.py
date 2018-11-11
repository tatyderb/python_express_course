import traceback
import sys

def foo(a):
    b = [1, 2, 3]
    x = 5 / a
    y = b[a]
    print(x, a, y)

try:    
    foo(2)      # ok
    foo(0)      # на 0 делить нельзя
    foo(7)      # выход за границы списка
except ZeroDivisionError:
    pass
except IndexError  as e:
    print('Поймали исключение!')
    print(e)
    print('-'*60)
    traceback.print_exc(file=sys.stdout)
    print('-'*60)
    
print('После блока обработки исключений')