# Файл конфигурации

Задать конфиграционный файл можно разными способами:
* написать python код и выполнить его;
* сохранить данные в json формате и читать их;
* написать .ini файл.

Для разбора _.ini_ файла воспользуйтесь модулем [configparser](https://docs.python.org/3/library/configparser.html)

Файл в human readable формате, данные разделены на секции. В разных секциях могут быть переменные с одинаковыми именами. Значения переменных разных типов. Есть комментарии.

Пример файла, который надо разобрать:
```python
; config.ini
; Sample configuration file

[installation]
library=%(prefix)s/lib
include=%(prefix)s/include
bin=%(prefix)s/bin
prefix=/usr/local

# Setting related to debug configuration
[debug]
log_errors=true
show_warnings=False

[server]
port: 8080
nworkers: 32
pid-file=/tmp/spam.pid
root=/www/root
signature:
    =================================
    Brought to you by the Python Cookbook
    =================================
```
Код для разбора файла:
```python
>>> from configparser import ConfigParser
>>> cfg = ConfigParser()
>>> cfg.read('config.ini')
['config.ini']
>>> cfg.sections()
['installation', 'debug', 'server']
>>> cfg.get('installation','library')
'/usr/local/lib'
>>> cfg.getboolean('debug','log_errors')
True
>>> cfg.getint('server','port')
8080
>>> cfg.getint('server','nworkers')
32
>>> print(cfg.get('server','signature'))
=================================
Brought to you by the Python Cookbook
=================================
>>>
```

Модификация конфиг-файла с помощью **cfg.write()**:
```python
>>> cfg.set('server','port','9000')
>>> cfg.set('debug','log_errors','False')
>>> import sys
>>> cfg.write(sys.stdout)
[installation]
library = %(prefix)s/lib
include = %(prefix)s/include
bin = %(prefix)s/bin
prefix = /usr/local
[debug]
log_errors = False
show_warnings = False
[server]
port = 9000
nworkers = 32
pid-file = /tmp/spam.pid
root = /www/root
signature =
=================================
Brought to you by the Python Cookbook
=================================
>>>
```

## Разница между _.ini_ файлом и куском кода на питоне

** Меньше ограничений на формат записи**

Эти записи эквивалентны:
```python
prefix=/usr/local
prefix: /usr/local
```
Имена переменных не зависят от регистра:
```python
>>> cfg.get('installation','PREFIX')
'/usr/local'
>>> cfg.get('installation','prefix')
'/usr/local'
```

В булевские переменные можно писать разумные значения: (эти записи эквивалентны)
```python
log_errors = true
log_errors = TRUE
log_errors = Yes
log_errors = 1
```

**Конфиг-файл не обязан исполняться сверху вниз**

Возможны подстановки переменных (переменная определена после использования):
```python
[installation]
library=%(prefix)s/lib
include=%(prefix)s/include
bin=%(prefix)s/bin
prefix=/usr/local
```

## Несколько конфигурационных файлов

Можно сливать прочитанные конфигурации в общую конфигурацию.

Пусть пользователь имеет свой конфиг-файл:
```python
; ~/.config.ini
[installation]
prefix=/Users/beazley/test
[debug]
log_errors=False
```
Можно слить его с ранее прочитанной конфигурацией:
```python
>>> cfg.get('installation', 'prefix')
'/usr/local'
>>> # Merge in user-specific configuration
>>> import os
>>> cfg.read(os.path.expanduser('~/.config.ini'))
['/Users/beazley/.config.ini']
>>> cfg.get('installation', 'prefix')
'/Users/beazley/test'
>>> cfg.get('installation', 'library')
'/Users/beazley/test/lib'
>>> cfg.getboolean('debug', 'log_errors')
False
```

Observe how the override of the prefix variable affects other related variables, such as
the setting of library. This works because variable interpolation is performed as late
as possible. You can see this by trying the following experiment:

```python
>>> cfg.get('installation','library')
'/Users/beazley/test/lib'
>>> cfg.set('installation','prefix','/tmp/dir')
>>> cfg.get('installation','library')
'/tmp/dir/lib'
>>>
```

Finally, it’s important to note that Python does not support the full range of features you
might find in an .ini file used by other programs (e.g., applications on Windows). Make
sure you consult the configparser documentation for the finer details of the syntax
and supported features.

## Задача

Добавить в игру файл конфигурации. Определить в нем ключевые параметры игры: максимальное количество игроков, начальный размер руки, диалект правил и тп.
