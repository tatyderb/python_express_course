## Модуль asyncio

Фреймворк, представляемый asyncio основан на event loop (цикле обработки событий), первоклассном объекте, ответственном за обработку событий ввода-вывода, системных событий и изменения контекста приложения. У этого цикла есть несколько реализаций. Обычно по умолчанию берется подходящая реализация, но вы можете выбрать реализацию сами. Это может быть полезно, например, под Windows, где некторые классы могут дать выигрыш в сетевом I/O.

Приложение взаимодействует с event loop _неявно_, регистрируя код, который будет выполнен и позволяя циклу обработки событий делать необходимые вызовы в коде приложения когда появляются события.

Например, сервер открывает сокеты и регистрирует их, чтобы сказали, когда придет input event. Event loop уведомляет сервер, когда возникает новое входящее соединиение или когда есть данные для чтения.

Ожидается, что приложение снова получит контроль после обработки события. То есть если нет больше данных для чтения, сервер должен вернуть управление циклу обработки.

Правильный возврат управления обеспечивают корутины. О них чуть позже.

future - это структура данных, представляющая результат работы, которая еще не совсем закончена. Event loop может следить за тем, что объект Future заверщается, позволяя одной части приложения ожидать другую для завершения некоторой работы. Кроме future модуль asyncio содержит другие concurrency примитивы, такие как lock и semaphore.

Task - это подкласс Future, который знает как обернуть и управлять исполнением корутин. Task может быть scheduled (запланирована) циклом обработки на выполнение, когда будут доступны необходимые ей ресурсы, и передаст произведенные данные (результат) в другие корутины.

### Корутины

Корутины похожи на генераторы за исключением нескольких отличий, основные из которых:
* генераторы возвращают данные
* корутины потребляют данные

Создадим генератор для чисел Фибоначчи:
```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```
Этот генератор можно использовать в цикле for:
```python
for i in fib():
    print(i)
```

Такой подход отличается скоростью и отсутствием повышенной нагрузки на память, поскольку значения генерируются "на лету" и не хранятся в списке. Теперь, если мы используем yield, то получим корутину. 

**Корутины потребляют данные, которые им передают**

Пример реализации grep через корутину:
```python
def grep(pattern):
    print("Searching for", pattern)
    while True:
        line = (yield)
        if pattern in line:
            print(line)
```
Код `line = (yield)` - место, куда передаются данные из внешнего источника.

Сначала данных нет. Потом они передаются метдом **send()**:
```python
search = grep('coroutine')
next(search)                        # нужно, чтобы корутина заработала
# Вывод: Searching for coroutine
search.send("I love you")
search.send("Don't you love me?")
search.send("I love coroutines instead!")
# Вывод: I love coroutines instead!
```

Корутины, как и генераторы, не запускаются сразу. Для запуска нужен метод \_\_next\_\_() и send().

Корутины можно закрыть:
```python
search.close()
```

## Кооперативная многозадачность с корутинами

Стартовать корутину event loop модуля asyncio может разными способами. Самый простой - вызвать **run_until_complete()**, передавая в него саму корутину.

Заметьте, написание корутины стало синтаксически проще:

```python
import asyncio

async def coroutine():
    print('in coroutine')

event_loop = asyncio.get_event_loop()
try:
    print('starting coroutine')
    coro = coroutine()                  # это НЕ приводит к вызову корутины
    print('entering event loop')
    event_loop.run_until_complete(coro)
finally:
    print('closing event loop')
    event_loop.close()
```
получаем:
```python
starting coroutine
entering event loop
in coroutine
closing event loop
```

### Возвращаем результат из корутины

Из корутины возвращается результат. Код ожидает получения этого результата.
```python
import asyncio

async def coroutine():
    print('in coroutine')
    return 'result'

event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(
        coroutine()
    )
    print('it returned: {!r}'.format(return_value))
finally:
    event_loop.close()
```
получаем:
```python
in coroutine
it returned: 'result'
```

### Цепь выполнения корутин

Одна корутина может стартовать другую корутину и ожидать от нее результата. Это позволяет запросто сделать декомпозицию задачи на части, которые можно повторно использовать. 

Пример описывает 2 фазы, которые должны выполняться в нужном порядке, но могут выполняться параллельно с другими операциями.

```python
import asyncio

async def outer():
    print('in outer')
    print('waiting for result1')
    result1 = await phase1()
    print('waiting for result2')
    result2 = await phase2(result1)
    return (result1, result2)

async def phase1():
    print('in phase1')
    return 'result1'

async def phase2(arg):
    print('in phase2')
    return 'result2 derived from {}'.format(arg)

event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(outer())
    print('return value: {!r}'.format(return_value))
finally:
    event_loop.close()
```
получаем:
```python
in outer
waiting for result1
in phase1
waiting for result2
in phase2
return value: ('result1', 'result2 derived from result1')
```

### Генераторы вместо корутин

Корутины - это ключевой компонент дизайна asyncio. Они дают конструкцию языка для того, чтобы остановить выполнение программы, при этом сохраняя состояние, в котором была программа и входя в это состояние через некоторое время. Что является очень важным для поддержания данного фреймворка.

В питоне 3.5 была введена новая возможность определять такие корутины естественно, используя **async def** и **await** для ожидания.

Ранняя версия питона 3.0 использует генераторы, обернутые в декоратор **asyncio.coroutine()** и **yield** для достижения того же эффекта.

```python
# asyncio_generator.py
import asyncio

@asyncio.coroutine
def outer():
    print('in outer')
    print('waiting for result1')
    result1 = yield from phase1()
    print('waiting for result2')
    result2 = yield from phase2(result1)
    return (result1, result2)

@asyncio.coroutine
def phase1():
    print('in phase1')
    return 'result1'

@asyncio.coroutine
def phase2(arg):
    print('in phase2')
    return 'result2 derived from {}'.format(arg)

event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(outer())
    print('return value: {!r}'.format(return_value))
finally:
    event_loop.close()
```
получим то же самое, что и в предыдущем примере.

## Планирование запуска обычных функций

