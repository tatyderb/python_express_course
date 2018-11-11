import traceback
import sys

def foo(a):
    x = 5 / a
    print(x, a)

try:    
    foo(5)
    foo(0)      # на 0 делить нельзя
    foo(7)
except ZeroDivisionError as e:
    print('Поймали исключение!')
    print(e)
    print('-'*60)
    traceback.print_exc(file=sys.stdout)
    print('-'*60)
    
print('После блока обработки исключений')