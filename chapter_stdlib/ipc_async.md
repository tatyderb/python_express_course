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

TODO - написать потом, запуск функций по таймеру (задержка, планирование на определенное время)
https://pymotw.com/3/asyncio/scheduling.html

### Scheduling a Callback "Soon"

Если время вызова callback не имеет значения, то можно использовать **call_soon()** для планирования вызова следующей итерации цикла. Любые дополнительные позиционные аргумента после функции передаются в callback во время его вызова. Для передачи в callback аргументов по ключу, используйте **partial()** из модуля functools.

Callback-и запускаются в том порядке, в котором были переданы.

```python
# asyncio_call_soon.py
import asyncio
import functools


def callback(arg, *, kwarg='default'):
    print('callback invoked with {} and {}'.format(arg, kwarg))


async def main(loop):
    print('registering callbacks')
    loop.call_soon(callback, 1)
    wrapped = functools.partial(callback, kwarg='not default')
    loop.call_soon(wrapped, 2)

    await asyncio.sleep(0.1)


event_loop = asyncio.get_event_loop()
try:
    print('entering event loop')
    event_loop.run_until_complete(main(event_loop))
finally:
    print('closing event loop')
    event_loop.close()
```
получим
```python
entering event loop
registering callbacks
callback invoked with 1 and default
callback invoked with 2 and not default
closing event loop
```

## Асинхронное получение результатов

future - это структура данных, представляющая результат работы, которая еще не совсем закончена. Event loop может следить за тем, что объект Future заверщается, позволяя одной части приложения ожидать другую для завершения некоторой работы. 

### Ожидание Future

Future работает как корутина, то есть приемы ожидания корутины так же можно использовать для ожидания, когда future будет помечена как завершенная. В примере future передается в метод **run_until_complete()** цикла обработки.

Состояние Future изменяется в "завершено", когда вызывается **set_result()** и экземпляр Future сохраняет результат, переданный в метод, для дальнейшего поиска.

```python
import asyncio

def mark_done(future, result):
    print('setting future result to {!r}'.format(result))
    future.set_result(result)

event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()

    print('scheduling mark_done')
    event_loop.call_soon(mark_done, all_done, 'the result')

    print('entering event loop')
    result = event_loop.run_until_complete(all_done)
    print('returned result: {!r}'.format(result))
finally:
    print('closing event loop')
    event_loop.close()

print('future result: {!r}'.format(all_done.result()))
```
получаем:
```python
scheduling mark_done
entering event loop
setting future result to 'the result'
returned result: 'the result'
closing event loop
future result: 'the result'
```

Future так же может использовать ключевое слово **await**. Вместо
```python
    result = event_loop.run_until_complete(all_done)
```
можно писать:
```python
    result = await all_done
```
Результат Future возращается, используя await, таким образом зачастую у нас одинаковый код для обычной корутины и экземпляра Future:
```python
# asyncio_future_await.py
import asyncio

def mark_done(future, result):
    print('setting future result to {!r}'.format(result))
    future.set_result(result)

async def main(loop):
    all_done = asyncio.Future()

    print('scheduling mark_done')
    loop.call_soon(mark_done, all_done, 'the result')

    result = await all_done
    print('returned result: {!r}'.format(result))

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
```
получим:
```python
scheduling mark_done
setting future result to 'the result'
returned result: 'the result'
```

### Future Callbacks

В добавок к тому, что Future работает подобно корутине, она может вызывать callbacks во время своего завершения. Callbacks включаются в том же порядке, в каком были зарегистрированы.

callback должен ожидать один аргумент, экземпляр Future. Для передачи дополнительных аргументов в колбеки, так же используйте функцию functools.partial() для написания функции-обертки.

The callback should expect one argument, the Future instance. To pass additional arguments to the callbacks, use functools.partial() to create a wrapper.

```python
# asyncio_future_callback.py
import asyncio
import functools

def callback(future, n):
    print('{}: future done: {}'.format(n, future.result()))

async def register_callbacks(all_done):
    print('registering callbacks on future')
    all_done.add_done_callback(functools.partial(callback, n=1))
    all_done.add_done_callback(functools.partial(callback, n=2))


async def main(all_done):
    await register_callbacks(all_done)
    print('setting result of future')
    all_done.set_result('the result')


event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    event_loop.run_until_complete(main(all_done))
finally:
    event_loop.close()
```
получим:
```python
registering callbacks on future
setting result of future
1: future done: the result
2: future done: the result
```

## Одновременное выполнение задач. Класс Task

Задачи - один из основных путей взаимодействия с циклом обработки. Tasks wrap coroutines and track when they are complete. Задачи - это подклассы Future, таким образом другие корутины могут ожидать их и каждая имеет результат, который можно взять у задачи после ее завершения.


### Запуск задачи

Чтобы запустить задачу, нужно сначала сделать экземпляр задачи функцией **create_task()**. Эта задача будет выполняться как часть параллельных операций, управляемых event loop, до тех пор, пока цикл работет и корутина не закончилась.

В примере ожидаем с помощью **await**, пока задача не закончится и из нее можно будет взять результат.

```python
asyncio_create_task.py
import asyncio

async def task_func():
    print('in task_func')
    return 'the result'

async def main(loop):
    print('creating task')
    task = loop.create_task(task_func())
    print('waiting for {!r}'.format(task))
    return_value = await task
    print('task completed {!r}'.format(task))
    print('return value: {!r}'.format(return_value))

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
```
получим:
```python
creating task
waiting for <Task pending coro=<task_func() running at
asyncio_create_task.py:12>>
in task_func
task completed <Task finished coro=<task_func() done, defined at
asyncio_create_task.py:12> result='the result'>
return value: 'the result'
```

## Cancelling Task

По ссылке на экземпляр Task, которую вернул create_task(), можно отменить задачу до ее завершения метдом **calcel()**.

В примере создается и потом отменяется задача до старта event loop. В результате в функции run_until_complete() возникает исключение CancelledError.

```python
asyncio_cancel_task.py
import asyncio


async def task_func():
    print('in task_func')
    return 'the result'


async def main(loop):
    print('creating task')
    task = loop.create_task(task_func())

    print('canceling task')
    task.cancel()

    print('canceled task {!r}'.format(task))
    try:
        await task
    except asyncio.CancelledError:
        print('caught error from canceled task')
    else:
        print('task result: {!r}'.format(task.result()))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
```
получаем:
```python
creating task
canceling task
canceled task <Task cancelling coro=<task_func() running at
asyncio_cancel_task.py:12>>
caught error from canceled task
```

Если задача была отменена, когда она ожидала другую concurrent операцию, эту задачу уведомляют об отмене возникновением исключения CancelledError в том месте, где происходило ожидание.

Обработка исключения позволяет, если необходимо, зачистить уже выполненную работу.

Catching the exception provides an opportunity to clean up work already done, if necessary.

```python
asyncio_cancel_task2.py
import asyncio


async def task_func():
    print('in task_func, sleeping')
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        print('task_func was canceled')
        raise
    return 'the result'


def task_canceller(t):
    print('in task_canceller')
    t.cancel()
    print('canceled the task')


async def main(loop):
    print('creating task')
    task = loop.create_task(task_func())
    loop.call_soon(task_canceller, task)
    try:
        await task
    except asyncio.CancelledError:
        print('main() also sees task as canceled')


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
```
получили:
```python
creating task
in task_func, sleeping
in task_canceller
canceled the task
task_func was canceled
main() also sees task as canceled
```

### Создание Task из корутины

Функция **ensure_future()** возвращает объект Task, связанную с выполнением корутины. Его можно передать в другой код, который может ожидать его, ничего не зная о том, как была сделана или вызвана оригинальная корутина.

Заметьте, что корутина, переданная в ensure_future() не стартует до тех пор, пока что-то не использует await, чтобы разрешить ее выполнение.

```python
# asyncio_ensure_future.py
import asyncio


async def wrapped():
    print('wrapped')
    return 'result'


async def inner(task):
    print('inner: starting')
    print('inner: waiting for {!r}'.format(task))
    result = await task
    print('inner: task returned {!r}'.format(result))


async def starter():
    print('starter: creating task')
    task = asyncio.ensure_future(wrapped())
    print('starter: waiting for inner')
    await inner(task)
    print('starter: inner returned')


event_loop = asyncio.get_event_loop()
try:
    print('entering event loop')
    result = event_loop.run_until_complete(starter())
finally:
    event_loop.close()
```
получим:
```python
entering event loop
starter: creating task
starter: waiting for inner
inner: starting
inner: waiting for <Task pending coro=<wrapped() running at asyncio_ensure_future.py:12>>
wrapped
inner: task returned 'result'
starter: inner returned
```

## Управление выполнением корутин

Линейный поток выполнения (control flow) ряда корутин легко организуется с помощью встроенного ключевого слова **await**. Для более сложной стуктуры выполнения корутин, позволяющей одной корутине ожидать завершения нескольких других параллельных задач, можно использовать инструменты asyncio.

### Ожидание нескольких корутин

Часто полезно разбить одну операцию на много частей и выполнять их независимо. Например, даунлоад нескольких удаленных ресурсов или querying remote APIs. Если порядок выполнения этих задач не важен, и количество операций может быть любым, можно использовать **wait()** для приостановки одной корутины до завершения других фоновых (background) операций.

Внутри **wait()** использует set для хранения созданных экземпляров Task, что приводит к их запуску и завершению в произвольном порядке. Из wait() возвращается кортеж из двух множеств - завершенные и подвешенные (pending) задачи.

```python
# asyncio_wait.py
import asyncio

async def phase(i):
    print('in phase {}'.format(i))
    await asyncio.sleep(0.1 * i)
    print('done with phase {}'.format(i))
    return 'phase {} result'.format(i)

async def main(num_phases):
    print('starting main')
    phases = [
        phase(i)
        for i in range(num_phases)
    ]
    print('waiting for phases to complete')
    completed, pending = await asyncio.wait(phases)
    results = [t.result() for t in completed]
    print('results: {!r}'.format(results))

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
```
получим:
```python
starting main
waiting for phases to complete
in phase 0
in phase 1
in phase 2
done with phase 0
done with phase 1
done with phase 2
results: ['phase 1 result', 'phase 0 result', 'phase 2 result']
```

Подвешенные (pending) операции будут возвращены, только если wait используют, задавая таймаут.

Эти оставшиеся фоновые задачи должны быть или отменены  или закончены by waiting for them. 

Оставляя эти задачи в подвешенном состоянии пока event loop продолжает работать, мы позволяем этим задачам выполниться в будущем, что нежелательно, если мы посчитали общую операцию прерванной. Если в конце процесса будут подвешенные операции, то получим warnings.

```python
asyncio_wait_timeout.py
import asyncio


async def phase(i):
    print('in phase {}'.format(i))
    try:
        await asyncio.sleep(0.1 * i)
    except asyncio.CancelledError:
        print('phase {} canceled'.format(i))
        raise
    else:
        print('done with phase {}'.format(i))
        return 'phase {} result'.format(i)


async def main(num_phases):
    print('starting main')
    phases = [
        phase(i)
        for i in range(num_phases)
    ]
    print('waiting 0.1 for phases to complete')
    completed, pending = await asyncio.wait(phases, timeout=0.1)
    print('{} completed and {} pending'.format(
        len(completed), len(pending),
    ))
    # Cancel remaining tasks so they do not generate errors
    # as we exit without finishing them.
    if pending:
        print('canceling tasks')
        for t in pending:
            t.cancel()
    print('exiting main')


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
```
получим:
```python
starting main
waiting 0.1 for phases to complete
in phase 1
in phase 0
in phase 2
done with phase 0
1 completed and 2 pending
cancelling tasks
exiting main
phase 1 cancelled
phase 2 cancelled
```

### Сбор результатов с корутин

Если фоновые фазы хорошо определены, и только результаты этих фаз имеют значение, то для ожидания множественных операций можно использовать функцию **gather()** 

Задачи, созданные функцией gather() не видны, то есть их нельзя отменить. Возвращется список результатов в том же порядке, в котором аргументы были переданы в gather(), вне зависимости от того, в каком порядке задачи на самом деле выполнялись и завершились.

```python
# asyncio_gather.py
import asyncio

async def phase1():
    print('in phase1')
    await asyncio.sleep(2)
    print('done with phase1')
    return 'phase1 result'

async def phase2():
    print('in phase2')
    await asyncio.sleep(1)
    print('done with phase2')
    return 'phase2 result'

async def main():
    print('starting main')
    print('waiting for phases to complete')
    results = await asyncio.gather(
        phase1(),
        phase2(),
    )
    print('results: {!r}'.format(results))

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main())
finally:
    event_loop.close()
```
получим:
```python
starting main
waiting for phases to complete
in phase2
in phase1
done with phase2
done with phase1
results: ['phase1 result', 'phase2 result']
```

### Handling Background Operations as They Finish

**as_completed()** - это генератор, который управляет выполнением предоставленных ему корутин и выдает их результаты по одному, не дожидаясь завершения работы других корутин. Так же как и в wait(), порядок не гарантирован, то не надо ждать завершения всех задач, чтобы начать обработку результатов.

В примере стартует несколько фоновых фаз, которые завершаются в обратном порядке. По мере использования генератора, цикл ожидает результата корутины, используя await.

```python
# asyncio_as_completed.py
import asyncio


async def phase(i):
    print('in phase {}'.format(i))
    await asyncio.sleep(0.5 - (0.1 * i))
    print('done with phase {}'.format(i))
    return 'phase {} result'.format(i)


async def main(num_phases):
    print('starting main')
    phases = [
        phase(i)
        for i in range(num_phases)
    ]
    print('waiting for phases to complete')
    results = []
    for next_to_complete in asyncio.as_completed(phases):
        answer = await next_to_complete
        print('received answer {!r}'.format(answer))
        results.append(answer)
    print('results: {!r}'.format(results))
    return results


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
```
получим:
```python
starting main
waiting for phases to complete
in phase 0
in phase 2
in phase 1
done with phase 2
received answer 'phase 2 result'
done with phase 1
received answer 'phase 1 result'
done with phase 0
received answer 'phase 0 result'
results: ['phase 2 result', 'phase 1 result', 'phase 0 result']
```

## Примитивы синхронизации

Хотя приложения asyncio обычно запускаются как single-threaded process, они по-прежнему сделаны как параллельные приложения. Каждая корутина или задача может быть исполнена в произольном порядке, основываясь на прерываниях от I/O и других внешних событиях. Для поддержки безопасной concurrency, asyncio включает реалзицию таких же низкоуровневых примитивов, что и в модулях threading и multiprocessing.

* asyncio.Lock
* asyncio.Event
* asyncio.Condition
* asyncio.Queue

Приведем примеры для Lock и Queue.

### Lock

A Lock can be used to guard access to a shared resource. Only the holder of the lock can use the resource. Multiple attempts to acquire the lock will block so that there is only one holder at a time.

A lock can be invoked directly, using await to acquire it and calling the release() method when done as in coro2() in this example. They also can be used as asynchronous context managers with the with await keywords, as in coro1().

```python
# asyncio_lock.py
import asyncio
import functools


def unlock(lock):
    print('callback releasing lock')
    lock.release()


async def coro1(lock):
    print('coro1 waiting for the lock')
    with await lock:
        print('coro1 acquired lock')
    print('coro1 released lock')


async def coro2(lock):
    print('coro2 waiting for the lock')
    await lock
    try:
        print('coro2 acquired lock')
    finally:
        print('coro2 released lock')
        lock.release()


async def main(loop):
    # Create and acquire a shared lock.
    lock = asyncio.Lock()
    print('acquiring the lock before starting coroutines')
    await lock.acquire()
    print('lock acquired: {}'.format(lock.locked()))

    # Schedule a callback to unlock the lock.
    loop.call_later(0.1, functools.partial(unlock, lock))

    # Run the coroutines that want to use the lock.
    print('waiting for coroutines')
    await asyncio.wait([coro1(lock), coro2(lock)]),


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
```
получим:
```python
acquiring the lock before starting coroutines
lock acquired: True
waiting for coroutines
coro1 waiting for the lock
coro2 waiting for the lock
callback releasing lock
coro1 acquired lock
coro1 released lock
coro2 acquired lock
coro2 released lock
```

### Queue

An asyncio.Queue provides a first-in, first-out data structure for coroutines like a queue.Queue does for threads or a multiprocessing.Queue does for processes.

Adding items with put() or removing items with get() are both asynchronous operations, since the queue size might be fixed (blocking an addition) or the queue might be empty (blocking a call to fetch an item).

```python
asyncio_queue.py
import asyncio


async def consumer(n, q):
    print('consumer {}: starting'.format(n))
    while True:
        print('consumer {}: waiting for item'.format(n))
        item = await q.get()
        print('consumer {}: has item {}'.format(n, item))
        if item is None:
            # None is the signal to stop.
            q.task_done()
            break
        else:
            await asyncio.sleep(0.01 * item)
            q.task_done()
    print('consumer {}: ending'.format(n))


async def producer(q, num_workers):
    print('producer: starting')
    # Add some numbers to the queue to simulate jobs
    for i in range(num_workers * 3):
        await q.put(i)
        print('producer: added task {} to the queue'.format(i))
    # Add None entries in the queue
    # to signal the consumers to exit
    print('producer: adding stop signals to the queue')
    for i in range(num_workers):
        await q.put(None)
    print('producer: waiting for queue to empty')
    await q.join()
    print('producer: ending')


async def main(loop, num_consumers):
    # Create the queue with a fixed size so the producer
    # will block until the consumers pull some items out.
    q = asyncio.Queue(maxsize=num_consumers)

    # Scheduled the consumer tasks.
    consumers = [
        loop.create_task(consumer(i, q))
        for i in range(num_consumers)
    ]

    # Schedule the producer task.
    prod = loop.create_task(producer(q, num_consumers))

    # Wait for all of the coroutines to finish.
    await asyncio.wait(consumers + [prod])


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop, 2))
finally:
    event_loop.close()
```
получим:
```python
consumer 0: starting
consumer 0: waiting for item
consumer 1: starting
consumer 1: waiting for item
producer: starting
producer: added task 0 to the queue
producer: added task 1 to the queue
consumer 0: has item 0
consumer 1: has item 1
producer: added task 2 to the queue
producer: added task 3 to the queue
consumer 0: waiting for item
consumer 0: has item 2
producer: added task 4 to the queue
consumer 1: waiting for item
consumer 1: has item 3
producer: added task 5 to the queue
producer: adding stop signals to the queue
consumer 0: waiting for item
consumer 0: has item 4
consumer 1: waiting for item
consumer 1: has item 5
producer: waiting for queue to empty
consumer 0: waiting for item
consumer 0: has item None
consumer 0: ending
consumer 1: waiting for item
consumer 1: has item None
consumer 1: ending
producer: ending
```

# Задачи

Во всех случаях подвисающие соединения, неожиданно отвалившиеся клиенты или их обилие не вешают сервер и не мешают другим клиентам получать данные. И всё это в один поток и без сложной ручной работы с select/poll.

## 0. Эхо-сервер

## 1. Сервер времени

Каждому подключенному раз в секунду посылают время.

## 1. IRC чат

Чат на TCP, где каждый может писать всем (типа IRC, только без комманд). В качестве клиента - telnet (или putty в режиме telnet или raw).

                                