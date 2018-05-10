# Concurrency: процессы (process) и потоки (thread)

## Источники

* (threading)[https://docs.python.org/3/library/threading.html] - документация
* (subprocess)[https://docs.python.org/3/library/subprocess.html] - документация

* Саммерфильд, глава 9
* Корутины:
  * (intermediate python)[https://lancelote.gitbooks.io/intermediate-python/content/book/coroutines.html]
  * (Coroutines)[http://www.dabeaz.com/coroutines/Coroutines.pdf] - презентация David Beazley http://www.dabeaz.com Presented at PyCon'2009, Chicago, Illinois
  * (Combinatorial Generation Using Coroutines With Examples in Python)[https://sahandsaba.com/combinatorial-generation-using-coroutines-in-python.html]
* асинхронность:  
  * (Understanding Asynchronous IO With Python 3.4's Asyncio And Node.js)[https://sahandsaba.com/understanding-asyncio-node-js-python-3-4.html]
* GIL
  * (New GIL)[http://www.dabeaz.com/python/NewGIL.pdf] - презентация David Beazley 
* (pymotw)[https://pymotw.com/3/concurrency.html]
  * (pymotw)[https://pymotw.com/3/threading/index.html]
  * (pymotw)[https://pymotw.com/3/subprocess/index.html]

* Python cookbook, chapter 12, Concurrency
* (Python Cookbook by David Ascher, Alex Martelli)[https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch06.html] Chapter 6. Threads, Processes, and Synchronization

* (И еще раз о GIL в Python)[https://habr.com/post/238703/] - обзор производительности разных решений для параллельных вычислений
* (Учимся писать многопоточно)[https://habr.com/post/149420/]
* (Синхронизация потоков в Python)[http://www.quizful.net/post/thread-synchronization-in-python] перевод (Thread Synchronization Mechanisms in Python)[http://effbot.org/zone/thread-synchronization.htm]

## Зачем нужна concurrency

* Эффективнее используем многоядерную архитектуру.
* Разделяем логику программы на полностью или частично асинхронные секции (пингуем несколько серверов одновременно).

## Синхронизация доступа к ресурсам

Если можно разбить задачу на независимые подзадачи БЕЗ синхронизации - сделайте это.

### Проблема producer-consumer

Один (thread, process) producer производит числа от 0 до 9. Другой такой же объект - consumer - "потребляет" эти числа.

Если нет синхронизации, то могут возникнуть проблемы.
```python
import threading

x = 0

def producer():
    global x
    for i in range(5):
        x = i
        print('producer', x)

def consumer():
    global x
    for i in range(5):
        print('consumer', x)


# init threads
t1 = threading.Thread(target=producer, args=())
t2 = threading.Thread(target=consumer, args=())

# start threads
t1.start()
t2.start()

# join threads to the main thread
t1.join()
t2.join()
print('Main', x)
```
Продьюсер может очень быстро производить числа, а консьюмер тупит.
```python
producer 0
producer 1
producer 2
producer 3
producer 4
consumer 4
consumer 4
consumer 4
consumer 4
consumer 4
Main 4
```

Или наоборот, продьюсер еще не успел произвести число (потому что в него добавили в начало sleep(1), например), а консьюмер уже его хочет обработать.
```python
consumer 0
consumer 0
consumer 0
consumer 0
consumer 0
producer 0
producer 1
producer 2
producer 3
producer 4
Main 4
```

## Атомарность операций

Пусть id вычисляет какой-то номер нашего объекта, например, денежной купюры, карты или номер паспорта. Очевидно, что они должны быть уникальными и идти один за другим.

Напишем для этого код:
```python
id = 0

def get_id():
    global id
    ... do something with id ...
    id += 1
```
Если запустить в один тред, то все работает хорошо. Если запустить в несколько тредов, то получаем, например, дублирование номеров. Почему?

Операция `id += 1` - НЕ **атомарная**.

Атомарной называют операцию, которая выполняется за 1 шаг без возможности ее прерывания.

`id += 1` состоит из 3 операций: чтения id, вычисления числа на 1 больше, чем прочитанное и запись результата в id. В любой момент времени между операциями может произойти переключение на другой поток.

Атомарные операции:
* чтение или изменение одного атрибута объекта
* чтение или изменение одной глобальной переменной
* выборка элемента из списка
* модификация списка "на месте" (т.е. с помощью метода append)
* выборка элемента из словаря
* модификация словаря "на месте" (т.е. добавление элемента, или вызов метода clear)

Заметьте, или чтение, или изменение атрибута - атомарны, но чтение и последующее изменение атрибута - НЕ атомарная операция.

### Критическая секция

участок исполняемого кода программы, в котором производится доступ к общему ресурсу (данным или устройству), который не должен быть одновременно использован более чем одним потоком (процессом) исполнения. При нахождении в критической секции двух (или более) процессов возникает состояние «гонки» («состязания»).

Атомарность операции не гарантирует, что она не является критической секцией. Очистка словаря - атомарная операция. Но если в это время этот же словарь кто-то перебирает в цикле, то очевидно, что и очистка, и перебор общего словаря - это критические секции.

Для корректной работы критических секций программы используют разные механизмы синхронизации.