# Логирование

## Источники

* [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
* [PEP 282 -- A Logging System](https://www.python.org/dev/peps/pep-0282/)
* [Logging HOWTO](https://docs.python.org/3/howto/logging.htm)
* Python Cookbook

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

## Логирование в библиотеке

Вы пишите модуль, логирование в котором хочется держать отдельно от логирования основной программы, где он используется.

Создайте свой логгер и пишите в него.

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
With this configuration, no logging will occur by default. For example:
```python
>>> import somelib
>>> somelib.func()
>>>
```
However, if the logging system gets configured, log messages will start to appear. For
example:
```python
>>> import logging
>>> logging.basicConfig()
>>> somelib.func()
CRITICAL:somelib:A Critical Error!
>>>
```

Libraries present a special problem for logging, since information about the environment
in which they are used isn’t known. As a general rule, you should never write
library code that tries to configure the logging system on its own or which makes assumptions
about an already existing logging configuration. Thus, you need to take great
care to provide isolation.

The call to getLogger(__name__) creates a logger module that has the same name as
the calling module. Since all modules are unique, this creates a dedicated logger that is
likely to be separate from other loggers.

The log.addHandler(logging.NullHandler()) operation attaches a null handler to
the just created logger object. A null handler ignores all logging messages by default.
Thus, if the library is used and logging is never configured, no messages or warnings
will appear.

One subtle feature of this recipe is that the logging of individual libraries can be independently
configured, regardless of other logging settings. For example, consider the
following code:

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
Here, the root logger has been configured to only output messages at the ERROR level or
higher. However, the level of the logger for somelib has been separately configured to
output debugging messages. That setting takes precedence over the global setting.

The ability to change the logging settings for a single module like this can be a useful
debugging tool, since you don’t have to change any of the global loggin
