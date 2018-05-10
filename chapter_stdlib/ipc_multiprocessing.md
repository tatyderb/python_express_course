## Модуль muliprocessing - работа с процессами

В первом приближении программа на похожа на программу с тредами:
```python
import threading


def worker(num):
    """thread worker function"""
    print('Worker: %s' % num)


threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
```
То же самое для процессов, а не тредов:
```python
import multiprocessing


def worker(num):
    """thread worker function"""
    print('Worker:', num)


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()
```

### Методы класса Process

| Метод | Описание |
|-|---|
| start() | запускает процесс; вызывается 1 раз, перед run() |
| run() | то, что должен делать процесс. Process.run вызывает метод, переданный в аргументах конструктора с переданными там же аргументами. |
| join(_timeout_=None) | Ждет, пока этот процесс закончится или закончится таймаут. Возвращает всегда None. Вызывайте is_alive(), чтобы узнать жив процесс или нет. RuntimeError при попытке join текущий процесс (дедлок). |
| name | имя процесса, используется для идентификации, устанавливается в конструкторе. Может совпадать у разных процессов. |
| pid | pid, до реального создания вернет None |
| daemon | для процесса-демона нужно установить в True до вызова функции start(). **Демон не может иметь детей** |
| exitcode | код завершения ребенка. None, если он еще не завершился. -N (отрицательное число), если завершился по сигналу N. |
| terminate() | Завершает процесс. В UNIX посылает SIGTERM, в Windows вызывается TerminateProcess() |

Note that the start(), join(), is_alive(), terminate() and exitcode methods should only be called by the process that created the process object.

Подробнее о старте процесса. В модуле реализовано 3 метода старта нового процесса:

* **spawn**
The parent process starts a fresh python interpreter process. The child process will only inherit those resources necessary to run the process objects run() method. In particular, unnecessary file descriptors and handles from the parent process will not be inherited. Starting a process using this method is rather slow compared to using fork or forkserver.

Available on Unix and Windows. The default on Windows.

* **fork**
The parent process uses os.fork() to fork the Python interpreter. The child process, when it begins, is effectively identical to the parent process. All resources of the parent are inherited by the child process. Note that safely forking a multithreaded process is problematic.

Available on Unix only. The default on Unix.

* **forkserver**
When the program starts and selects the forkserver start method, a server process is started. From then on, whenever a new process is needed, the parent process connects to the server and requests that it fork a new process. The fork server process is single threaded so it is safe for it to use os.fork(). No unnecessary resources are inherited.

Available on Unix platforms which support passing file descriptors over Unix pipes.

Вывод: если ваша программа работала на UNIX, до старта дочерних процессов читая конфиг-файлы и открывая файлы и сетевые соединения, то на Windows этой информации нет - "пустой" новый процесс. Передавайте нужную информацию в конструкторе (dict конфига), shared memory и тп.

### exitcode

| Выход из дочернего процесса | exitcode этого процесса |
| `return n` | 0 |
| `return` | 0 |
| `sys.exit(n)` | число n |
| исключение | 1 |
| окончен послыкой сигнала N | -1 |

```python
# multiprocessing_exitcode.py
import multiprocessing
import sys
import time

def exit_error():
    sys.exit(1)

def exit_ok():
    return

def return_value():
    return 1

def raises():
    raise RuntimeError('There was an error!')

def terminated():
    time.sleep(3)

if __name__ == '__main__':
    jobs = []
    funcs = [
        exit_error,
        exit_ok,
        return_value,
        raises,
        terminated,
    ]
    for f in funcs:
        print('Starting process for', f.__name__)
        j = multiprocessing.Process(target=f, name=f.__name__)
        jobs.append(j)
        j.start()

    jobs[-1].terminate()

    for j in jobs:
        j.join()
        print('{:>15}.exitcode = {}'.format(j.name, j.exitcode))
```
Получим:
```python
$ python3 multiprocessing_exitcode.py

Starting process for exit_error
Starting process for exit_ok
Starting process for return_value
Starting process for raises
Starting process for terminated
Process raises:
Traceback (most recent call last):
  File ".../lib/python3.6/multiprocessing/process.py", line 258,
in _bootstrap
    self.run()
  File ".../lib/python3.6/multiprocessing/process.py", line 93,
in run
    self._target(*self._args, **self._kwargs)
  File "multiprocessing_exitcode.py", line 28, in raises
    raise RuntimeError('There was an error!')
RuntimeError: There was an error!
     exit_error.exitcode = 1
        exit_ok.exitcode = 0
   return_value.exitcode = 0
         raises.exitcode = 1
     terminated.exitcode = -15
```

### Логирование

Подробнее смотри рецепты логирования.

Самый простой случай - все сообщения печатаем на stderr. Для этого в модуле muliprocessing есть уже сконфигурированный логгер **log_to_stderr**.

По умолчанию этот логер установлен в уровень NOTSET, когда нет никаких сообщений. Поэтому единственное, что вам нужно - установить нужный уровень:
```python
multiprocessing_log_to_stderr.py
import multiprocessing
import logging
import sys


def worker():
    print('Doing some work')
    sys.stdout.flush()


if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.DEBUG)
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
```
получим:
```python
$ python3 multiprocessing_log_to_stderr.py

[INFO/Process-1] child process calling self.run()
Doing some work
[INFO/Process-1] process shutting down
[DEBUG/Process-1] running all "atexit" finalizers with priority
>= 0
[DEBUG/Process-1] running the remaining "atexit" finalizers
[INFO/Process-1] process exiting with exitcode 0
[INFO/MainProcess] process shutting down
[DEBUG/MainProcess] running all "atexit" finalizers with
priority >= 0
[DEBUG/MainProcess] running the remaining "atexit" finalizers
```

Если нужно менять уровень логирования, то получим сначала ссылку на логер **get_logger()**:
```python
import multiprocessing
import logging
import sys


def worker():
    print('Doing some work')
    sys.stdout.flush()


if __name__ == '__main__':
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
```

### Наследуемся от класса Process

Как и в случает thread, можно не только передавать функцию в конструктор, и наследоваться от класса muliprocessing.Process, переопределяя функцию run().

```python
import multiprocessing

class Worker(multiprocessing.Process):

    def run(self):
        print('In {}'.format(self.name))
        return

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = Worker()
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
```

### Передача сообщений между процессами - Queue

Типичный сценарий использования процессов - разделить всю работу между несколькими работниками. Потом нужно будет собрать результаты этой работы. 

Простейший способ обмениваться информацией между процессами - очередь сообщений **Queue**, а объекты сериализуем модулем **pickle**.

```python
import multiprocessing

class MyFancyClass:

    def __init__(self, name):
        self.name = name

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        print('Doing something fancy in {} for {}!'.format(
            proc_name, self.name))

def worker(q):
    obj = q.get()
    obj.do_something()

if __name__ == '__main__':
    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()

    queue.put(MyFancyClass('Fancy Dan'))

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    p.join()
```
получим:
```python
Doing something fancy in Process-1 for Fancy Dan!
```

Теперь несколько процессов получают данные из **JoinableQueue** и пересылают результаты обратно родительскому процессу. Для остановки работников используется техника 'poison pill': после посылки реальных данных главный процесс посылает специальные "стоп" значения (которые точно не могут быть реальными данными). После получения этого значения, работник прекращает свой цикл обработки данных. Посылается по 1 стоп-сигналу на каждого работника. Родительский процесс использует join() очереди, чтобы дождаться, что все дети закончили посылать ему данные, и далее обрабатывает присланные результаты.

```python
import multiprocessing
import time

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('{}: Exiting'.format(proc_name))
                self.task_queue.task_done()
                break
            print('{}: {}'.format(proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)  # pretend to take time to do the work
        return '{self.a} * {self.b} = {product}'.format(
            self=self, product=self.a * self.b)

    def __str__(self):
        return '{self.a} * {self.b}'.format(self=self)


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print('Creating {} consumers'.format(num_consumers))
    consumers = [
        Consumer(tasks, results)
        for i in range(num_consumers)
    ]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 10
    for i in range(num_jobs):
        tasks.put(Task(i, i))

    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1
```
получим:
```python
Creating 8 consumers
Consumer-1: 0 * 0
Consumer-2: 1 * 1
Consumer-3: 2 * 2
Consumer-4: 3 * 3
Consumer-5: 4 * 4
Consumer-6: 5 * 5
Consumer-7: 6 * 6
Consumer-8: 7 * 7
Consumer-3: 8 * 8
Consumer-7: 9 * 9
Consumer-4: Exiting
Consumer-1: Exiting
Consumer-2: Exiting
Consumer-5: Exiting
Consumer-6: Exiting
Consumer-8: Exiting
Consumer-7: Exiting
Consumer-3: Exiting
Result: 6 * 6 = 36
Result: 2 * 2 = 4
Result: 3 * 3 = 9
Result: 0 * 0 = 0
Result: 1 * 1 = 1
Result: 7 * 7 = 49
Result: 4 * 4 = 16
Result: 5 * 5 = 25
Result: 8 * 8 = 64
Result: 9 * 9 = 81
```

### muliprocessing.Event

Аналогичен threading.Event.

Event может быть установлен или нет. Можно ждать event (быть может с ограничением по таймауту).

```python
import multiprocessing
import time


def wait_for_event(e):
    """Wait for the event to be set before doing anything"""
    print('wait_for_event: starting')
    e.wait()
    print('wait_for_event: e.is_set()->', e.is_set())


def wait_for_event_timeout(e, t):
    """Wait t seconds and then timeout"""
    print('wait_for_event_timeout: starting')
    e.wait(t)
    print('wait_for_event_timeout: e.is_set()->', e.is_set())


if __name__ == '__main__':
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(
        name='block',
        target=wait_for_event,
        args=(e,),
    )
    w1.start()

    w2 = multiprocessing.Process(
        name='nonblock',
        target=wait_for_event_timeout,
        args=(e, 2),
    )
    w2.start()

    print('main: waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    print('main: event is set')
```
получено:
```python
main: waiting before calling Event.set()
wait_for_event: starting
wait_for_event_timeout: starting
wait_for_event_timeout: e.is_set()-> False
main: event is set
wait_for_event: e.is_set()-> True
```

### muliprocessing.Lock

Аналогичен threading.Lock

**acquire()** - запрашивает лок. **release()** - освобождает лок.

Обратите внимание, что правильно обрернуть взятие-отпускание лога в try-finally блок:
```python
    lock.acquire()
    try:
        stream.write('Lock acquired directly\n')
    finally:
        lock.release()

```
или воспользуйтесь конструкцией **with**:
```python
def worker_with(lock, stream):
    with lock:
        stream.write('Lock acquired via with\n')
```

Полный код:
```python
import multiprocessing
import sys


def worker_with(lock, stream):
    with lock:
        stream.write('Lock acquired via with\n')


def worker_no_with(lock, stream):
    lock.acquire()
    try:
        stream.write('Lock acquired directly\n')
    finally:
        lock.release()


lock = multiprocessing.Lock()
w = multiprocessing.Process(
    target=worker_with,
    args=(lock, sys.stdout),
)
nw = multiprocessing.Process(
    target=worker_no_with,
    args=(lock, sys.stdout),
)

w.start()
nw.start()

w.join()
nw.join()
```
получим:
```python
Lock acquired via with
Lock acquired directly
```

### muliprocessing.Condition

Аналогичен threading.Condition

Процесс s1 отрабатывает stage_1. Процессы s2 отрабатывают stage_2.

Два потока работают на второй стадии в параллель, но только после того, как закончила работу первая стадия.

```python
import multiprocessing
import time


def stage_1(cond):
    """perform first stage of work,
    then notify stage_2 to continue
    """
    name = multiprocessing.current_process().name
    print('Starting', name)
    with cond:
        print('{} done and ready for stage 2'.format(name))
        cond.notify_all()


def stage_2(cond):
    """wait for the condition telling us stage_1 is done"""
    name = multiprocessing.current_process().name
    print('Starting', name)
    with cond:
        cond.wait()
        print('{} running'.format(name))


if __name__ == '__main__':
    condition = multiprocessing.Condition()
    s1 = multiprocessing.Process(name='s1',
                                 target=stage_1,
                                 args=(condition,))
    s2_clients = [
        multiprocessing.Process(
            name='stage_2[{}]'.format(i),
            target=stage_2,
            args=(condition,),
        )
        for i in range(1, 3)
    ]

    for c in s2_clients:
        c.start()
        time.sleep(1)
    s1.start()

    s1.join()
    for c in s2_clients:
        c.join()
```
получим:
```python
Starting stage_2[1]
Starting stage_2[2]
Starting s1
s1 done and ready for stage 2
stage_2[1] running
stage_2[2] running
```

### multiprocessing.Semaphore

Иногда полезно обеспечить одновременный достп к ресурсу многим процессам, но ограничить количество этих процессов.

Например, пул соединений может поддерживать ограниченное количество одновременных соединений, или сетевое приложение может поддерживать фиксированное количество одновременных скачиваний.

В этих случаях удобно использовать семафоры Semaphore. В отличие от Lock, где 1 значение - взведено (1) или нет (0), семафор поддерживает значения от 0 до n.

В этом примере класс ActivePool просто служит удобным способом отслеживания процессов, выполняемых в данный момент. Реальный пул ресурсов, вероятно, выделит соединение или другое значение для нового активного процесса и вернет значение, когда задача будет выполнена. Здесь пул просто используется для хранения имен активных процессов, чтобы показать, что одновременно работают только три.

In this example, the ActivePool class simply serves as a convenient way to track which processes are running at a given moment. A real resource pool would probably allocate a connection or some other value to the newly active process, and reclaim the value when the task is done. Here, the pool is just used to hold the names of the active processes to show that only three are running concurrently.

```python
import random
import multiprocessing
import time

class ActivePool:

    def __init__(self):
        super(ActivePool, self).__init__()
        self.mgr = multiprocessing.Manager()
        self.active = self.mgr.list()
        self.lock = multiprocessing.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)

    def __str__(self):
        with self.lock:
            return str(self.active)


def worker(s, pool):
    name = multiprocessing.current_process().name
    with s:
        pool.makeActive(name)
        print('Activating {} now running {}'.format(
            name, pool))
        time.sleep(random.random())
        pool.makeInactive(name)


if __name__ == '__main__':
    pool = ActivePool()
    s = multiprocessing.Semaphore(3)
    jobs = [
        multiprocessing.Process(
            target=worker,
            name=str(i),
            args=(s, pool),
        )
        for i in range(10)
    ]

    for j in jobs:
        j.start()

    while True:
        alive = 0
        for j in jobs:
            if j.is_alive():
                alive += 1
                j.join(timeout=0.1)
                print('Now running {}'.format(pool))
        if alive == 0:
            # all done
            break
```
получим:
```python
Activating 0 now running ['0', '1', '2']
Activating 1 now running ['0', '1', '2']
Activating 2 now running ['0', '1', '2']
Now running ['0', '1', '2']
Now running ['0', '1', '2']
Now running ['0', '1', '2']
Now running ['0', '1', '2']
Activating 3 now running ['0', '1', '3']
Activating 4 now running ['1', '3', '4']
Activating 6 now running ['1', '4', '6']
Now running ['1', '4', '6']
Now running ['1', '4', '6']
Activating 5 now running ['1', '4', '5']
Now running ['1', '4', '5']
Now running ['1', '4', '5']
Now running ['1', '4', '5']
Activating 8 now running ['4', '5', '8']
Now running ['4', '5', '8']
Now running ['4', '5', '8']
Now running ['4', '5', '8']
Now running ['4', '5', '8']
Now running ['4', '5', '8']
Activating 7 now running ['5', '8', '7']
Now running ['5', '8', '7']
Activating 9 now running ['8', '7', '9']
Now running ['8', '7', '9']
Now running ['8', '9']
Now running ['8', '9']
Now running ['9']
Now running ['9']
Now running ['9']
Now running ['9']
Now running []
```

### Managing Shared State

В предыдущем примере список активных процессов поддерживался централизованно в экземпляре ActivePool через специальный тип list() в классе muliprocessing.Manager. Manager координирует доступ к совместо используемым ресурсам между всеми его пользователями.

В примере ниже все процессы будут писать в единый (совместно используемый) словарь.

```python
import multiprocessing
import pprint


def worker(d, key, value):
    d[key] = value


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    jobs = [
        multiprocessing.Process(
            target=worker,
            args=(d, i, i * 2),
        )
        for i in range(10)
    ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print('Results:', d)
```
получаем:
```python
Results: {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 14,
8: 16, 9: 18}
```

### Shared Namespace

В добавок к list и dict класс Manager может создавать совместно используемые namespace.

Любое значение имени, добавленное в Namespace, видно во всех клиентах, у которых есть этот экземпляр Namespace.

```python
import multiprocessing


def producer(ns, event):
    ns.value = 'This is the value'
    event.set()


def consumer(ns, event):
    try:
        print('Before event: {}'.format(ns.value))
    except Exception as err:
        print('Before event, error:', str(err))
    event.wait()
    print('After event:', ns.value)


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    event = multiprocessing.Event()
    p = multiprocessing.Process(
        target=producer,
        args=(namespace, event),
    )
    c = multiprocessing.Process(
        target=consumer,
        args=(namespace, event),
    )

    c.start()
    p.start()

    c.join()
    p.join()
```
получаем:
```python
Before event, error: 'Namespace' object has no attribute 'value'
After event: This is the value
```

**Модификация изменяемых переменных НЕ поддерживается автоматически**

В примере сохраняем в namespace ссылку на list (изменяемый тип). В одном процессе изменяем по ссылке его содержимое, в другом процессе ничего не знают об изменениях.
```python
import multiprocessing


def producer(ns, event):
    # DOES NOT UPDATE GLOBAL VALUE!
    ns.my_list.append('This is the value')
    event.set()


def consumer(ns, event):
    print('Before event:', ns.my_list)
    event.wait()
    print('After event :', ns.my_list)


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    namespace.my_list = []

    event = multiprocessing.Event()
    p = multiprocessing.Process(
        target=producer,
        args=(namespace, event),
    )
    c = multiprocessing.Process(
        target=consumer,
        args=(namespace, event),
    )

    c.start()
    p.start()

    c.join()
    p.join()
```
получилось: (да ничего не получилось! консьюмер так и не узнал об изменениях в продьюсере!)
```python
Before event: []
After event : []
```
**Для обновления содержимого изменяемой переменной свяжите заново объект namespace с этой переменной.**

(To update the list, attach it to the namespace object again.)

А для списка лучше используйте специальный тип из Manager.list(), а не из Manager.namespace()

### Пул процессов

Если задача может быть разбита на независимые подзадачи, которые можно распределить между исполнителями, то для этого использовать класс Pool.
return values работ собираются в список, который будет возвращен как результат работы всего пула.

Аргументы конструктора Pool включает количество процессов и функцию, которая будет выполняться, когда стартует дочерний процесс (1 функция на 1 ребенка).

Результат метода map() эквивалентен встроенной функции map(), за исключением того, что отдельные задачи выполняются параллельно. Так как пул обрабатывает его входные значения параллельно, close() и join() используются для того, чтобы синхронизировать родительский и дочерние процессы для необходимой зачистки (cleanup).

```python
import multiprocessing


def do_calculation(data):
    return data * 2


def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == '__main__':
    inputs = list(range(10))
    print('Input   :', inputs)

    builtin_outputs = map(do_calculation, inputs)
    print('Built-in:', builtin_outputs)

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
    )
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print('Pool    :', pool_outputs)
```
получим:
```python
Input   : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Built-in: <map object at 0x1007b2be0>
Starting ForkPoolWorker-3
Starting ForkPoolWorker-4
Starting ForkPoolWorker-5
Starting ForkPoolWorker-6
Starting ForkPoolWorker-1
Starting ForkPoolWorker-7
Starting ForkPoolWorker-2
Starting ForkPoolWorker-8
Pool    : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

По умолчанию Pool создает фиксированное количество рабочих процессов и передает им задачи до тех пор, пока задачи не закончатся. Установка параметра `maxtasksperchild` заставит пул рестартовать дочерний процесс после того, как он выполнит указанное число заданий, предотвращая долго выполняющиеся дочерние процессы от расхода системных ресурсов.

By default, Pool creates a fixed number of worker processes and passes jobs to them until there are no more jobs. Setting the maxtasksperchild parameter tells the pool to restart a worker process after it has finished a few tasks, preventing long-running workers from consuming ever more system resources.

Изменим только вызов конструктора Pool:
```python
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
        maxtasksperchild=2,
    )
```

The pool restarts the workers when they have completed their allotted tasks, even if there is no more work. In this output, eight workers are created, even though there are only 10 tasks, and each worker can complete two of them at a time.

```python
Input   : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Built-in: <map object at 0x1007b21d0>
Starting ForkPoolWorker-1
Starting ForkPoolWorker-2
Starting ForkPoolWorker-4
Starting ForkPoolWorker-5
Starting ForkPoolWorker-6
Starting ForkPoolWorker-3
Starting ForkPoolWorker-7
Starting ForkPoolWorker-8
Pool    : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

