## Заключение

* Исключение - простой способ разнести в коде место ошибки и ее обработку.
* try-ecxept-else-finally блок
    * **try** - код, который может породить исключение
    * **ecxept** - перехват исключений
        * '''ecxept (ZeroDivisionError, IndexError) as e:'''
        * '''ecxept ZeroDivisionError as e:'''
        * '''ecxept ZeroDivisionError:'''
        * '''ecxept:''' - перехват всех исключений. Так не нужно писать.
    * **else** - если try прошло БЕЗ исключений.
    * **finally** - clean-up фаза, выполнится в любом случае.
* **raise** - генерация исключения  
    * 'raise ValueError("Negative length")' - создание нового исключения
    * 'raise e' - повторный запуск исключения e (что стало со стектрейсом?)
    * 'raise' - повторный запуск последнего исключения.
* создаем свое исключение: 'class MyException(Exception): pass'
* информация об исключении e:
    * 'str(e)' - division by zero
    * 'exc_type, exc_value, exc_traceback = sys.exc_info()' - что хранится в исключении
    * 'traceback.print_exc(file=sys.stdout)' - печать стектрейса  

### Заключительный пример

```python
try:
    print('Я уверен, исключений не будет!')
except Exception:
    print('Исключение')
else:
    # Любой код, который должен быть исполнен, если исключение в блоке
    # try не было вызвано, но для которого не должна проводиться
    # обработка исключений
    print('Я буду исполнен, если в try не будет исключений.'
          'Мои исключения не будут обрабатываться.')
finally:
    print('Я буду исполнен в любом случае!')
​
# Вывод: Я уверен, исключений не будет!
#        Я буду исполнен, если в try не будет исключений. Мои исключения не будут обрабатываться.
#        Я буду исполнен в любом случае!
```





