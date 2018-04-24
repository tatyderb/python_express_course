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
