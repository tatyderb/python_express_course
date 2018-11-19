## Работа с путями

Модуль знает о разнице между формированием путей в UNIX и Windows и сам делает нужные преобразования.

Опирается на следующие операции:
```python
os.sep - The separator between portions of the path (e.g., "/" or "\").
os.extsep - The separator between a filename and the file "extension" (e.g., ".").
os.pardir - The path component that means traverse the directory tree up one level (e.g., "..").
os.curdir - The path component that refers to the current directory (e.g., ".").
```

Примеры манипуляции с путями:

```python
>>> import os
>>> path = '/Users/beazley/Data/data.csv'
>>> # Get the last component of the path
>>> os.path.basename(path)
'data.csv'
>>> # Get the directory name
>>> os.path.dirname(path)
'/Users/beazley/Data'
>>> # Join path components together
>>> os.path.join('tmp', 'data', os.path.basename(path))
'tmp/data/data.csv'
>>> # Expand the user's home directory
>>> path = '~/Data/data.csv'
>>> os.path.expanduser(path)
'/Users/beazley/Data/data.csv'
>>> # Split the file extension
>>> os.path.splitext(path)
('~/Data/data', '.csv')
```

### Проверка существования

```python
>>> import os
>>> os.path.exists('/etc/passwd')
True
>>> os.path.exists('/tmp/spam')
False
```

## Проверка типа файла и ссылки на файл

```python
>>> # Is a regular file
>>> os.path.isfile('/etc/passwd')
True
>>> # Is a directory
>>> os.path.isdir('/etc/passwd')
False
>>> # Is a symbolic link
>>> os.path.islink('/usr/local/bin/python3')
True
>>> # Get the file linked to
>>> os.path.realpath('/usr/local/bin/python3')
'/usr/local/bin/python3.3'
```

## Размер, дата создания, 

```python
>>> os.path.getsize('/etc/passwd')
3669
>>> os.path.getmtime('/etc/passwd')
1272478234.0
>>> import time
>>> time.ctime(os.path.getmtime('/etc/passwd'))
'Wed Apr 28 13:10:34 2010'
```
Если операция невозможно, возникает исключение.
```python
>>> os.path.getsize('/Users/guido/Desktop/foo.txt')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "/usr/local/lib/python3.3/genericpath.py", line 49, in getsize
return os.stat(filename).st_size
PermissionError: [Errno 13] Permission denied: '/Users/guido/Desktop/foo.txt'
```

## Получить список содержимого директории

```python
import os
names = os.listdir('somedir')
```
Подробнее:
```python
import os.path

# Get all regular files
names = [name for name in os.listdir('somedir')
         if os.path.isfile(os.path.join('somedir', name))]

# Get all dirs
dirnames = [name for name in os.listdir('somedir')
            if os.path.isdir(os.path.join('somedir', name))]
```
### Все файлы по маске 

```python
import os

# Get all *.py files
pyfiles = [name for name in os.listdir('somedir')
            if name.endswith('.py')]
```
или модуль `glob`:
```python
import glob
pyfiles = glob.glob('somedir/*.py')
```
или модуль `fnmatch`
```python
from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('somedir')
    if fnmatch(name, '*.py')]
```

## File metadata

```python
# Example of getting a directory listing
import os
import os.path
import glob
pyfiles = glob.glob('*.py')

# Get file sizes and modification dates
name_sz_date = [(name, os.path.getsize(name), os.path.getmtime(name))
                for name in pyfiles]
for name, size, mtime in name_sz_date:
    print(name, size, mtime)
    
# Alternative: Get file metadata
file_metadata = [(name, os.stat(name)) for name in pyfiles]
for name, meta in file_metadata:
    print(name, meta.st_size, meta.st_mtime)
```