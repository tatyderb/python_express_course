# Логирование

**Логирование** - означает запись событий, которые случились во время работы программы.
Программисты пишут логирующие вызовы, чтобы показать, что случились определенные события.
Событие состоит из сообщения-описания и каких-то данных.
Событию так же приписывают важность или уровень(severity или level).

## Источники

* [Документация](https://docs.python.org/3/library/logging.html)
* [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
* [PEP 282 -- A Logging System](https://www.python.org/dev/peps/pep-0282/)
* [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
* Python Cookbook

# Логирование на коленке

## Логирование - проще не бывает

```python
import logging
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything
```
На консоль будет напечатано `WARNING:root:Watch out!`. Второе сообщение не будет напечатано, 
потому что по умолчанию выставлен уровень WARNING.

## Логируем в файл

Для логирования в файл определим имя этого файла. Например, `example.log`. Заодно установили уровень логирования.

```python
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```

## Логирование в простом скрипте

Нужно добавить простое логирование в скрипт. Самый простой вариант.

Используем модуль **logging**.

```python
import logging
def main():
    # Configure the logging system
    logging.basicConfig(
        filename='app.log',
        level=logging.ERROR
    )
    
    # Variables (to make the calls that follow work)
    hostname = 'www.python.org'
    item = 'spam'
    filename = 'data.csv'
    mode = 'r'
    
    # Example logging calls (insert into your program)
    logging.critical('Host %s unknown', hostname)
    logging.error("Couldn't find %r", item)
    logging.warning('Feature is deprecated')
    logging.info('Opening file %r, mode=%r', filename, mode)
    logging.debug('Got here')
    
if __name__ == '__main__':
    main()
```

Функции **critical(), error(), warning(), info(), debug()** дают возможность логировать сообщения разного уровня важности (по убыванию).

При конфигурации логирования **basicConfig** указывается уровень (аргумент level), по которому делают фильтрацию. Сообщения ниже уровнем игнорируются.

Аргументы в функциях логирования - как в printf языка С. Первый аргумент - форматная строка с форматными символами, следующие аргументы разбираются по указанному формату.

Запустив код выше получим файл _app.log_:
```python
CRITICAL:root:Host www.python.org unknown
ERROR:root:Could not find 'spam'
```

Изменим уровень логирования и формат логирующей строки:
```python
logging.basicConfig(
    filename='app.log',
    level=logging.WARNING,
    format='%(levelname)s:%(asctime)s:%(message)s'
)
```
Содержимое логов изменится:
```python
CRITICAL:2012-11-20 12:27:13,595:Host www.python.org unknown
ERROR:2012-11-20 12:27:13,595:Could not find 'spam'
WARNING:2012-11-20 12:27:13,595:Feature is deprecated
```

Можно не хардкодить конфигурацию логера в программе, а задавать ее в конфигурационном файле:
```python
import logging
import logging.config
def main():
    # Configure the logging system
    logging.config.fileConfig('logconfig.ini')
...
```
Содержимое logconfig.ini файла:
```python
[loggers]
keys=root

[handlers]
keys=defaultHandler

[formatters]
keys=defaultFormatter

[logger_root]
level=INFO
handlers=defaultHandler
qualname=root

[handler_defaultHandler]
class=FileHandler
formatter=defaultFormatter
args=('app.log', 'a')

[formatter_defaultFormatter]
format=%(levelname)s:%(name)s:%(message)s
```

**Логгер должен быть сконфигурирован до записи в него**

Для записи в **`stderr` вместо файла**, можно НЕ указывать файл, в который логируем при конфигурации:
```python
logging.basicConfig(level=logging.INFO)
```
Для **изменения уровня логирования во время исполнения программы** укажите в конфигурации новый уровень:
```python
logging.getLogger().level = logging.DEBUG
```

### Если хотим, чтобы логфайл перезаписывался при каждом запуске

**filemode** - способ открытия логфайла. Откроем его не с 'a' (по умолчанию), а с 'w'.

```python
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
```

### Устанавливаем уровень логирования через командную строку

Пусть наша переменная `loglevel` связана с ключом `--log` в командной строке и может быть установлена, например в `--log=INFO`.

```python
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, ...)
```

## Логирование программы из нескольких файлов

Пусть наша программа написана в нескольких файлах (модулях) и мы хотим писать ее логи из разных файлов в единый лог-файл.

Программа: главный модуль myapp.py и еще один файл с кодом в mylib.py.

**Конфигурация логера - до его первого использования**

```python
# myapp.py
import logging
import mylib

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    mylib.do_something()
    logging.info('Finished')

if __name__ == '__main__':
    main()
```
в другом файле используем уже готовый логер:
```python
# mylib.py
import logging

def do_something():
    logging.info('Doing something')
```
Получаем лог:
```python
INFO:root:Started
INFO:root:Doing something
INFO:root:Finished
```

## Изменение формата логирования

Вместо формата по умолчанию можно настроить свой формат логирования. Укажите параметр **format** в конфигурации.

```python
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')
```
получим
```python
DEBUG:This message should appear on the console
INFO:So should this
WARNING:And this, too
```
### Таблица атрибутов формата

| Attribute name | Format | Description |
|--|--|----|
| args | You shouldn't need to format this yourself. | The tuple of arguments merged into msg to produce message, or a dict whose values are used for the merge (when there is only one argument, and it is a dictionary). |
| asctime | %(asctime)s | Human-readable time when the LogRecord was created. By default this is of the form '2003-07-08 16:49:45,896' (the numbers after the comma are millisecond portion of the time). |
| created | %(created)f | Time when the LogRecord was created (as returned by time.time()). |
| exc_info | You shouldn't need to format this yourself. | Exception tuple (a la sys.exc_info) or, if no exception has occurred, None. |
| filename | %(filename)s | Filename portion of pathname. |
| funcName | %(funcName)s | Name of function containing the logging call. |
| levelname | %(levelname)s | Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'). |
| levelno | %(levelno)s | Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL). |
| lineno | %(lineno)d | Source line number where the logging call was issued (if available). |
| message | %(message)s | The logged message, computed as msg % args. This is set when Formatter.format() is invoked. |
| module | %(module)s | Module (name portion of filename). |
| msecs | %(msecs)d | Millisecond portion of the time when the LogRecord was created. |
| msg | You shouldn't need to format this yourself. | The format string passed in the original logging call. Merged with args to produce message, or an arbitrary object (see Using arbitrary objects as messages). |
| name | %(name)s | Name of the logger used to log the call. |
| pathname | %(pathname)s | Full pathname of the source file where the logging call was issued (if available). |
| process | %(process)d | Process ID (if available). |
| processName | %(processName)s | Process name (if available). |
| relativeCreated | %(relativeCreated)d | Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded. |
| stack_info | You shouldn't need to format this yourself. | Stack frame information (where available) from the bottom of the stack in the current thread, up to and including the stack frame of the logging call which resulted in the creation of this record. |
| thread | %(thread)d | Thread ID (if available). |
| threadName | %(threadName)s | Thread name (if available). |

### Дата и время в сообщении

```python
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is when this event was logged.')
```
получим
```python
2010-12-12 11:41:42,612 is when this event was logged.
```

По умолчанию формат ISO8601, если нужен свой формат, укажите его в параметре **datefmt** при задании конфигурации.
```python
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')
```
получим
```python
12/12/2010 11:46:36 AM is when this event was logged.
```
Формат даты и времени такой же, как для функции [time.strftime()](https://docs.python.org/3/library/time.html#time.strftime)


# Продвинутое логирование

## Как это работает?

Объекты:
* **Logger** (логер) - предоставляет интерфейс, которым пользуются в коде.
* **Handler** (обработчик) - посылает запись лога (созданную логером) куда нужно.
* **Filter** (фильтр) - фильтрует записи, которые нужно выводить.
* **Formatter** (форматер) - определяет в каком виде выводим записи.

Информация о событии логирования передается в виде записи (экземпляра [LogRecord](https://docs.python.org/3/library/logging.html#logging.LogRecord) ) между логерами, обработчиками, фильтрами и форматерами.

Для логирования вызваются методы экземпляра класса Logger (далее называем их логерами). Каждый экземпляр имеет имя, и они упорядочены в иерархии пространства имен с использованием точки как разделителя.

Например, логер _scan_ - родитель логера _scan.txt_, _scan.html_ и _scan.pdf_. 

Обычно логер модуля называют по имени модуля:
```python
logger = logging.getLogger(__name__)
```
Базовый логер **root**. Он - прародитель всех остальных логеров.
Его имя `root`, именно его используют методы **critical(), error(), warning(), info(), debug()**. Функции и методы имеют одинаковые имена.

Можно выводить сообщения различными способами:
* в файл;
* HTTP GET/POST;
* email через SMTP;
* сокеты;
* очереди сообщений;
* ОС-зависимые механизмы: syslog или NT event log (Windows).
Куда выводить определяют обработчики (handler).
Можно создать свой обработчик, если вам не хватило встроенных обработчиков.

По умолчанию логер никуда не выводит. Чтобы определить куда выводить (на консоль или в файл), используют конфигурацию логера. В примере это был basicConfig(). Когда вы вызывает функции логирования debug(), info(), warning(), error() и critical(), они проверяют, установленно ли куда выводить, и если не установлено, то по умолчанию устанавливают в `sys.stderr` в формате по умолчанию, прежде чем передавать сообщение логеру root.

Формат, устанавливаемый basicConfig по умолчанию это
```python
severity:logger name:message
```
его можно изменить, установив свой [Formatter object](https://docs.python.org/3/library/logging.html#formatter-objects)

## Logger Flow

()[../assets/logging_flow.png]

## Loggers (логеры)

Logger нужен для:
* предоставить методы для прикладного кода для логирования.
* отфильтровать какие сообщения должны появиться согласно важности и фильтрам.
* доставить записи нужным обработчикам.

Основные методы логера - это установка конфигурации и собственно создание записей.

Методы конфигурации логера:

* **Logger.setLevel()** - определяет с какого уровня и выше будут записываться сообщения. Уровни логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL. Если установлен уровень INFO, то сообщения уровня DEBUG выводиться НЕ будут, все остальные - будут.
* **Logger.addHandler()** и **Logger.removeHandler()** - добавляет и удаляет обработчик к этому логеру.
* **Logger.addFilter()** и **Logger.removeFilter()** - добавляет и удаляет фильтр к логеру. Фильтры обычно вам не нужны, используются для сложного логирования.

После конфигурации логера можно пользоваться его методами для создания сообщения.

* **Logger.debug(), Logger.info(), Logger.warning(), Logger.error(),  Logger.critical()** создают запись (record), в которой определено сообщение (message) и уровень.

* **Logger.exception()** похож на **Logger.error()**. Разница в том, что Logger.exeption() посылает stacktrace. Используйте этот метод в try .. except блоке.

* **Logger.log()** получает уровень в виде аргумента.

* **getLogger()** возвращает ссылку на объект логера с указанным именем (если указано имя) или root (по умолчанию). Имена объеденены в иерархическую структуру, с разделителем точка. Множественные вызовы этого метода для одного и того же имени возвращают указатель на один и тот же объект.

Логеры foo.bar, foo.bar.baz, foo.bam - наследники логера foo.

У логеров есть эффективный уровень. Если в логере не выставлен явно уровень, то берется уровень родителя и используется как эффективный уровень этого ребенка. Если у родителя нет явно выставленного уровня, то ищется в родителе родителя и так далее вверх по иерархии, пока не найдется явно выставленный уровень.
В логере root гарантированно есть явно выставленный уровень. По умолчанию он выставлен в WARNING.
Эффективный уровень используют для принятия решения - передавать событие обработчику или нет (уровень события слишком низкий).

Дочерние логеры передают сообщения вверх по цепочке обработчиков, связанных с родительскими логерами. Поэтому можно не определять обработчики для каждого логера, а настроить обработчик на логере и создавать дочерние логеры по мере необходимости. (Можно отключить это распространение сообщений вверх по иерархии выставив атрибут логера propagate=False).

## Handlers (обработчики)

Объект Handler отвечает за направление соответствующих сообщений (на основе их важности) туда, куда определено в этом обработчике. У объекта класса Logger может быть добавлено ноль или более обработчиков с помощью **[addHandler()](https://docs.python.org/3/library/logging.html#logging.Logger.addHandler)** метода.
Например, приложение может посылать все сообщения в лог-файл, все error или выше на stdout, все critical - на email. В этом случае нужно 3 обработчика, где каждый обработчик посылает сообщения определенного уровня в определенное место.

В стандартной библиотеке есть набор обработчиков (см. Полезные обработчики); в тьюториалах показываются в основном StreamHandler и FileHandler.

Если вы пользуетесь стандартными обработчиками (а не пишете свой класс обработчика), то вам могут понадобиться методы:
* **setLevel()** - такой же, как в логере. Определяет, начиная с какой важности сообщения будут посылаться туда, куда определяет обработчик. Зачем два одинаковых метода - в логере и в обработчике? В логере определяется, посылается вообще сообщение или нет, а в обработчике - посылается ли оно (если послано) в handler destination.
* **setFormatter()** - определяет Formatter, которым пользуется этот обработчик.
* **addFilter()** и **removeFilter()** - сконфигурировать / деконфигурировать фильтр для обработчика.

Ваше приложение не должно использовать непосредственно объекты класса Handler, а пользоваться его наследниками.

## Formatters (форматеры)

Форматеры определяют, какой будет порядок, структура и содержимое сообщения. В отличие от базового класса logging.Handler, ваше приложение может создавать свои (под)классы форматеров, если вам нужно особое поведение. У конструктора три параметра: message format string, a date format string and a style indicator.

```python
logging.Formatter.__init__(fmt=None, datefmt=None, style='%')
```
Если нет форматной строки fmt, то используем строку сообщения как есть. Если нет формата даты datefmt, то по умолчанию формат даты `%Y-%m-%d %H:%M:%S` с милисекундами на конце. style (стиль) может быть %, '{' или '$' (по умолчанию %).

Если стиль %, то форматная строка fmt использует стиль `%(<dictionary key>)s` для подстановки строк; возможные ключи описаны в таблице атрибутов.

Если стиль '{', то форматная строка fmt предполагает стиль совместимый с str.format() (с использованием keyword arguments).

При стиле '$' форматная строка должна быть написана в стиле string.Template.substitute()

Этот формат сообщения показывает время в human-readable виде, важность и само сообщение в следующем порядке:

```python
'%(asctime)s - %(levelname)s - %(message)s'
```

Из [документации по Formatter](https://docs.python.org/3/library/logging.html#logging.Formatter):
Formatters use a user-configurable function to convert the creation time of a record to a tuple. By default, time.localtime() is used; to change this for a particular formatter instance, set the converter attribute of the instance to a function with the same signature as time.localtime() or time.gmtime(). To change it for all formatters, for example if you want all logging times to be shown in GMT, set the `converter` attribute in the Formatter class (to time.gmtime for GMT display).

## Конфигурируем логер

3 способа конфигурации логера:
* Создаем логеры, обработчики, форматеры в коде на питоне и вызываем методы конфигурации, которые были описаны выше.
* Создаем файл конфигурации логера и вызываем функцию **fileConfig()**
* Создаем словарь конфигурации логера и передаем его в функцию **dictConfig()**, [схема словаря](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)

```python
logging.config.fileConfig(fname, defaults=None, disable_existing_loggers=True)
logging.config.dictConfig(config)
```
Приведем примеры всех трех способов.

### Создаем логер и связанные с ним объекты в коде

```python
import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```
получим:
```python
$ python simple_logging_module.py
2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
2005-03-19 15:10:26,620 - simple_example - INFO - info message
2005-03-19 15:10:26,695 - simple_example - WARNING - warn message
2005-03-19 15:10:26,697 - simple_example - ERROR - error message
2005-03-19 15:10:26,773 - simple_example - CRITICAL - critical message
```

### Конфиг-файл логера

Конфиг-файл `logging.conf`:
```python
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=
```

читаем его в программе:
```python
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```
получаем:
```python
$ python simple_logging_config.py
2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
2005-03-19 15:38:55,979 - simpleExample - INFO - info message
2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message
```

При вызове функции по умолчанию параметр **disable_existing_loggers=True**.

Note that the class names referenced in config files need to be either relative to the logging module, or absolute values which can be resolved using normal import mechanisms. Thus, you could use either WatchedFileHandler (relative to the logging module) or mypackage.mymodule.MyHandler (for a class defined in package mypackage and module mymodule, where mypackage is available on the Python import path).

### Словарь конфигурации

Словарь можно записывать в отдельный файл в JSON или YAML формате.

```python
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
loggers:
  simpleExample:
    level: DEBUG
    handlers: [console]
    propagate: no
root:
  level: DEBUG
  handlers: [console]
```

### Что будет, если логер не сконфигурировать?

Если система логирования никак не была сконфигурирована, то возможна ситуация, что событие должно быть залогировано, но у нас нет ни одного обработчика для этого события. В этом случае поведение зависит от версиии Python.

* Python ДО 3.2:
  * If logging.raiseExceptions is False (production mode), the event is silently dropped.
  * If logging.raiseExceptions is True (development mode), a message 'No handlers could be found for logger X.Y.Z' is printed once.
* Python 3.2 или более свежие версии:

The event is output using a 'handler of last resort', stored in logging.lastResort. This internal handler is not associated with any logger, and acts like a StreamHandler which writes the event description message to the current value of sys.stderr (therefore respecting any redirections which may be in effect). No formatting is done on the message - just the bare event description message is printed. The handler's level is set to WARNING, so all events at this and greater severities will be output.
To obtain the pre-3.2 behaviour, logging.lastResort can be set to None.

## Логирование в библиотеке

Вы пишите модуль, логирование в котором хочется держать отдельно от логирования основной программы, где он используется.

Создайте свой логгер и пишите в него.

logging.NullHandler - обработчик, который "ничего не делает"

```python
# somelib.py
import logging

log = logging.getLogger(__name__)           # во время import нашего модуля выполнится этот код
log.addHandler(logging.NullHandler())

# Example function (for testing)
def func():
    log.critical('A Critical Error!')
    log.debug('A debug message')
```
В этой конфигурации по умолчанию нет ни одного логера (и не будет логирования!):

```python
>>> import somelib
>>> somelib.func()
>>>
```
Однако, как только логирующая система будет сконфигурирована, начнут появляться сообщения для лога:
```python
>>> import logging
>>> logging.basicConfig()
>>> somelib.func()
CRITICAL:somelib:A Critical Error!
>>>
```

Библиотеки - это особый случай логирования, потому что неизвестно, в каком окружении будет работать библиотека.
В общем случае, не стоит писать библиотеку так, чтобы она сама конфигурировала логирующую систему, 
или делала какие-то предположения о существующей конфигурации логера. Лучше позаботьтесь об изоляции.

Вызов **getLogger(\_\_name\_\_)** создает объект логера с тем же именем, что и вызывающий модуль. 
Так как все модули имеют уникальные имена, получаем специальный объект логера, отделенный от других логеров.

Операция **log.addHandler(logging.NullHandler())**  - привязывает null handler к только что созданному объекту логера.
Этот null handler по умолчанию игнорирует все логирующие сообщения. Таким образом, 
если библиотека используется, но логер не был сконфигурирован, никакие сообщения или предупреждения никуда не будут записаны.

Стоит конфигурировать логер отдельной библиотеке независимо от других настроек логирования. Например:

```python
>>> import logging
>>> logging.basicConfig(level=logging.ERROR)
>>> import somelib
>>> somelib.func()
CRITICAL:somelib:A Critical Error!
>>> # Change the logging level for 'somelib' only
>>> logging.getLogger('somelib').level=logging.DEBUG
>>> somelib.func()
CRITICAL:somelib:A Critical Error!
DEBUG:somelib:A debug message
```

Здесь корневой логер был настроен только чтобы пропускать сообщения с уровнем ERROR или выше. 
Однако, у логера модуля somelib был установлен уровень DEBUG. Локальные настройки более приоритетны, чем глобальные.

Эту особенность можно использовать для отладки отдельной библиотеки, не влючая отладку других частей.

# Useful Handlers
In addition to the base Handler class, many useful subclasses are provided:

* StreamHandler instances send messages to streams (file-like objects).
* FileHandler instances send messages to disk files.
* BaseRotatingHandler is the base class for handlers that rotate log files at a certain point. It is not meant to be instantiated directly. Instead, use RotatingFileHandler or TimedRotatingFileHandler.
* RotatingFileHandler instances send messages to disk files, with support for maximum log file sizes and log file rotation.
* TimedRotatingFileHandler instances send messages to disk files, rotating the log file at certain timed intervals.
* SocketHandler instances send messages to TCP/IP sockets. Since 3.4, Unix domain sockets are also supported.
* DatagramHandler instances send messages to UDP sockets. Since 3.4, Unix domain sockets are also supported.
* SMTPHandler instances send messages to a designated email address.
* SysLogHandler instances send messages to a Unix syslog daemon, possibly on a remote machine.
* NTEventLogHandler instances send messages to a Windows NT/2000/XP event log.
* MemoryHandler instances send messages to a buffer in memory, which is flushed whenever specific criteria are met.
* HTTPHandler instances send messages to an HTTP server using either GET or POST semantics.
* WatchedFileHandler instances watch the file they are logging to. If the file changes, it is closed and reopened using the file name. This handler is only useful on Unix-like systems; Windows does not support the underlying mechanism used.
* QueueHandler instances send messages to a queue, such as those implemented in the queue or multiprocessing modules.
* NullHandler instances do nothing with error messages. They are used by library developers who want to use logging, but want to avoid the 'No handlers could be found for logger XXX' message which can be displayed if the library user has not configured logging. See Configuring Logging for a Library for more information.
