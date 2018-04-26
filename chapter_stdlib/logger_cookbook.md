# Рецепты использования логера

Перевод [Logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

Содержание:
* [Логирование в нескольких модулях](#logging_cookbook_1)
* [Логирование в нескольких threads](#logging_cookbook_2)
* [Много handler и formatter](#logging_cookbook_3)
* [Logging to multiple destinations](#logging_cookbook_4)
* [Configuration server example](#logging_cookbook_5)
* [Dealing with handlers that block](#logging_cookbook_6)
* [Sending and receiving logging events across a network](#logging_cookbook_7)
* [Adding contextual information to your logging output](#logging_cookbook_8)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)
* [](#logging_cookbook_1)

## <a name="logging_cookbook_1"></a> Логирование в нескольких модулях

Если несколько раз вызвать `logging.getLogger('someLogger')` получим ссылку на один и тот же объект, даже если вызываем из разных модулей, но в рамках одного процесса интерпретатора питона.

Прикладной код может определять и конфигурировать родительский логер в одном модуле и создавать (но не конфигурировать) дочерний логер в отдельном модуле, и все вызовы в дочернем логере будут переданы родительскому логеру.

Главный модуль:
```python
import logging
import auxiliary_module

# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('creating an instance of auxiliary_module.Auxiliary')
a = auxiliary_module.Auxiliary()
logger.info('created an instance of auxiliary_module.Auxiliary')
logger.info('calling auxiliary_module.Auxiliary.do_something')
a.do_something()
logger.info('finished auxiliary_module.Auxiliary.do_something')
logger.info('calling auxiliary_module.some_function()')
auxiliary_module.some_function()
logger.info('done with auxiliary_module.some_function()')
```

Модуль auxiliary:
```python
import logging

# create logger
module_logger = logging.getLogger('spam_application.auxiliary')

class Auxiliary:
    def __init__(self):
        self.logger = logging.getLogger('spam_application.auxiliary.Auxiliary')
        self.logger.info('creating an instance of Auxiliary')

    def do_something(self):
        self.logger.info('doing something')
        a = 1 + 1
        self.logger.info('done doing something')

def some_function():
    module_logger.info('received a call to "some_function"')
```

получим:
```python
2005-03-23 23:47:11,663 - spam_application - INFO -
   creating an instance of auxiliary_module.Auxiliary
2005-03-23 23:47:11,665 - spam_application.auxiliary.Auxiliary - INFO -
   creating an instance of Auxiliary
2005-03-23 23:47:11,665 - spam_application - INFO -
   created an instance of auxiliary_module.Auxiliary
2005-03-23 23:47:11,668 - spam_application - INFO -
   calling auxiliary_module.Auxiliary.do_something
2005-03-23 23:47:11,668 - spam_application.auxiliary.Auxiliary - INFO -
   doing something
2005-03-23 23:47:11,669 - spam_application.auxiliary.Auxiliary - INFO -
   done doing something
2005-03-23 23:47:11,670 - spam_application - INFO -
   finished auxiliary_module.Auxiliary.do_something
2005-03-23 23:47:11,671 - spam_application - INFO -
   calling auxiliary_module.some_function()
2005-03-23 23:47:11,672 - spam_application.auxiliary - INFO -
   received a call to 'some_function'
2005-03-23 23:47:11,673 - spam_application - INFO -
   done with auxiliary_module.some_function()
```

## <a name="logging_cookbook_2"></a> Логирование в нескольких threads

Никаких дополнительных усилий. Все работает. Работает и с большим количеством thread.

```python
import logging
import threading
import time

def worker(arg):
    while not arg['stop']:
        logging.debug('Hi from myfunc')
        time.sleep(0.5)

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    info = {'stop': False}
    thread = threading.Thread(target=worker, args=(info,))
    thread.start()
    while True:
        try:
            logging.debug('Hello from main')
            time.sleep(0.75)
        except KeyboardInterrupt:
            info['stop'] = True
            break
    thread.join()

if __name__ == '__main__':
    main()
```
получим (пока не напечатаем stop):
```python
   0 Thread-1 Hi from myfunc
   3 MainThread Hello from main
 505 Thread-1 Hi from myfunc
 755 MainThread Hello from main
1007 Thread-1 Hi from myfunc
1507 MainThread Hello from main
1508 Thread-1 Hi from myfunc
2010 Thread-1 Hi from myfunc
2258 MainThread Hello from main
2512 Thread-1 Hi from myfunc
3009 MainThread Hello from main
3013 Thread-1 Hi from myfunc
3515 Thread-1 Hi from myfunc
3761 MainThread Hello from main
4017 Thread-1 Hi from myfunc
4513 MainThread Hello from main
4518 Thread-1 Hi from myfunc
```

## <a name="logging_cookbook_3"></a>  Много handler и formatter

Добавляйте сколько хотите:
```python
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```

## <a name="logging_cookbook_4"></a> Logging to multiple destinations

Хотим логировать и в файл, и на консоль. При этом с разными уровнями важности и в разном формате.

```python
import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/temp/myapp.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')
```
получим на консоль:
```python
root        : INFO     Jackdaws love my big sphinx of quartz.
myapp.area1 : INFO     How quickly daft jumping zebras vex.
myapp.area2 : WARNING  Jail zesty vixen who grabbed pay from quack.
myapp.area2 : ERROR    The five boxing wizards jump quickly.
```
получим в файл (примерно):
```python
10-22 22:19 root         INFO     Jackdaws love my big sphinx of quartz.
10-22 22:19 myapp.area1  DEBUG    Quick zephyrs blow, vexing daft Jim.
10-22 22:19 myapp.area1  INFO     How quickly daft jumping zebras vex.
10-22 22:19 myapp.area2  WARNING  Jail zesty vixen who grabbed pay from quack.
10-22 22:19 myapp.area2  ERROR    The five boxing wizards jump quickly.
```
Заметим, DEBUG сообщения попали только в файл. Остальные и на консоль, и  в файл.

Вы можете использовать другие обработчики, а не только FileHandler и StreamHandler.

## <a name="logging_cookbook_5"></a>  Configuration server example

```python
import logging
import logging.config
import time
import os

# read initial config file
logging.config.fileConfig('logging.conf')

# create and start listener on port 9999
t = logging.config.listen(9999)
t.start()

logger = logging.getLogger('simpleExample')

try:
    # loop through logging calls to see the difference
    # new configurations make, until Ctrl+C is pressed
    while True:
        logger.debug('debug message')
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')
        time.sleep(5)
except KeyboardInterrupt:
    # cleanup
    logging.config.stopListening()
    t.join()
```

Далее скрипт получает имя файла и посылает этот файл на сервер, чтобы этот файл стал новой конфигурацией логера. Перед посылкой файла посылается его длина.

```python
#!/usr/bin/env python
import socket, sys, struct

with open(sys.argv[1], 'rb') as f:
    data_to_send = f.read()

HOST = 'localhost'
PORT = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('connecting...')
s.connect((HOST, PORT))
print('sending config...')
s.send(struct.pack('>L', len(data_to_send)))
s.send(data_to_send)
s.close()
print('complete')
```
## <a name="logging_cookbook_6"></a> Dealing with handlers that block

Иногда вам нужно, чтобы обработчик не блокировал поток, в котором вы создаете сообщение. Пример такого сценария - веб приложение.

Например, SMTPHandler может долго обрабатывать сообщение по не зависящим от разработчика причинам. Любой сетевой хендлер может может слишком долго выполнять DNS запрос и это вы тоже не можете контролировать.

Решение состоит из двух частей.

В первой части используйте QueueHandler для тех логеров, в которые пишут из тредов с, чья производительность критична. Сообщения просто попадают в очередь (которую стоит сделать достаточность большой емкости или вообще без ограничения на ее размер). Запись в очередь обычно делается достаточно быстро. Однако, стоит ловить случай переполнения очереди.

Если вы разработчик библиотеки с тредами, чувствительными к производительности, удостоверьтесь, что эта особенность задокументирована (вместе с предложением присоединять только QueueHandler к вашим логерам), чтобы помочь другим программистам, которые будут использовать ваш код.

Второй частью решения является QueueListener, который разработан как соотвествующая часть к QueueHandler. 
QueueListener очень простой: он передает очередь и некоторые обработчики и стартует внутренний thread, который слушает его очередь, получает LogRecords, посланные из QueueHandler (или быть может из другого источника LogRecords). Очередные LogRecords удаляются из очереди и передаются обработчикам для обработки.

Выгода в отдельном QueueListener классе в том, что вы можете использовать один и тот же экземпляр для обслуживания множества QueueHandler. Это более resource-friendly, чем, скажем иметь версию QueueHandler в отдельном треде. 

Пример использования этих двух классов. (import опущены):

```python
que = queue.Queue(-1)  # no limit on size
queue_handler = QueueHandler(que)
handler = logging.StreamHandler()
listener = QueueListener(que, handler)
root = logging.getLogger()
root.addHandler(queue_handler)
formatter = logging.Formatter('%(threadName)s: %(message)s')
handler.setFormatter(formatter)
listener.start()
# The log output will display the thread which generated
# the event (the main thread) rather than the internal
# thread which monitors the internal queue. This is what
# you want to happen.
root.warning('Look out!')
listener.stop()
```
получим:
```python
MainThread: Look out!
```

Использование 1 QueueListener и множества QueueHandler смотрите в примере Logging to a single file from multiple processes

## <a name="logging_cookbook_7"></a> Sending and receiving logging events across a network

Допустим, вы хотите посылать логирующие события по сети и обрабатывать их при получении. Проще всего добавить SocketHandler к root логеру в тех местах, где события посылаются:

Тут посылаем:
```python
import logging, logging.handlers

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')
```

Тут получаем и обрабатываем с использованием модуля `socketserver`:
```python
import pickle
import logging
import logging.handlers
import socketserver
import struct


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)

class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = True

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

def main():
    logging.basicConfig(
        format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')
    tcpserver = LogRecordSocketReceiver()
    print('About to start TCP server...')
    tcpserver.serve_until_stopped()

if __name__ == '__main__':
    main()
```

Сначала должен стартовать сервер, потом клиенты. 

На стороне клиентов ничего в консоль не пишется.

На стороне сервера получаем:
```python
About to start TCP server...
   59 root            INFO     Jackdaws love my big sphinx of quartz.
   59 myapp.area1     DEBUG    Quick zephyrs blow, vexing daft Jim.
   69 myapp.area1     INFO     How quickly daft jumping zebras vex.
   69 myapp.area2     WARNING  Jail zesty vixen who grabbed pay from quack.
   69 myapp.area2     ERROR    The five boxing wizards jump quickly.
```
Note that there are some security issues with pickle in some scenarios. If these affect you, you can use an alternative serialization scheme by overriding the makePickle() method and implementing your alternative there, as well as adapting the above script to use your alternative serialization.

## <a name="logging_cookbook_8"></a> Adding contextual information to your logging output

Sometimes you want logging output to contain contextual information in addition to the parameters passed to the logging call. For example, in a networked application, it may be desirable to log client-specific information in the log (e.g. remote client’s username, or IP address). Although you could use the extra parameter to achieve this, it’s not always convenient to pass the information in this way. While it might be tempting to create Logger instances on a per-connection basis, this is not a good idea because these instances are not garbage collected. While this is not a problem in practice, when the number of Logger instances is dependent on the level of granularity you want to use in logging an application, it could be hard to manage if the number of Logger instances becomes effectively unbounded.

## <a name="logging_cookbook_9"></a> 

## <a name="logging_cookbook_10"></a> 
