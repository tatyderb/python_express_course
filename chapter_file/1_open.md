## Подробнее о функции open

```python
open (file, mode='r', buffering=None, encoding=None, errors=None, newline=None, closefd=True)
```
OSError - если произошла ошибка.

Режимы открытия файла:

| Character | Meaning |
|--|----|
| 'r' | open for reading (default) |
| 'w' | open for writing, truncating the file first |
| 'x' | open for exclusive creation, failing if the file already exists |
| 'a' | open for writing, appending to the end of the file if it exists |
| 'b' | binary mode |
| 't' | text mode (default) |
| '+' | open a disk file for updating (reading and writing) |

* *buffering*
  * 0 - ВЫключить буферизацию (работает только в бинарной моде);
  * 1 - line buffering;
  * >1 - указывается размер буфера;
  * None:
    * бинарные файлы буферизуем с фиксированным размером буфера [io.DEFAULT_BUFFER_SIZE](https://docs.python.org/dev/library/io.html#io.DEFAULT_BUFFER_SIZE)
    * "интерактивные" текстовые файлы (терминалы, т.е. где [isatty()](https://docs.python.org/dev/library/io.html#io.IOBase.isatty) вернул `True` работают с линейной буферизацией;
    * прочие текствые файлы - как и бинарные.
    
* encoding - указывает кодировку файла (только в текстовой моде!)

* errors - как обрабатывается произошедшая ошибка:
  * `strict` или `None` - генерируется исключение ValueError;
  * `ignore` - так можно потерять данные;
  * `replace` - заменяет "непонятные" символы на `?`;
  * специфические замены:
    * `surrogateescape` - will represent any incorrect bytes as code points in the Unicode Private Use Area ranging from U+DC80 to U+DCFF. These private code points will then be turned back into the same bytes when the surrogateescape error handler is used when writing data. This is useful for processing files in an unknown encoding.
    * `xmlcharrefreplace` - заменяет на `&#nnn;`
    * `backslashreplace` - заменяет на Python’s backslashed escape sequences
    * `namereplace` - заменяет на `\N{...}`
  
* `newline` - обработка концов строк в текстовой моде.
  * чтение:
    * `None` - любые концы строк транслируются в '\n';
    * '' - концы строк приходят как есть;
    * '\n', '\r', '\r\n' - концами строк считаются только указанные последовательности и именно они стоят в конце строки при чтении.
  * запись:
    * `None` - все EOL транслируются в os.linesep
    * '' или '\n' - символы без изменений
    * '\n', '\r', '\r\n' - EOL конвертируются в указанные символы.


The newly created file is non-inheritable.

A file descriptor has an “inheritable” flag which indicates if the file descriptor can be inherited by child processes. Since Python 3.4, file descriptors created by Python are non-inheritable by default.

On UNIX, non-inheritable file descriptors are closed in child processes at the execution of a new program, other file descriptors are inherited.

On Windows, non-inheritable handles and file descriptors are closed in child processes, except for standard streams (file descriptors 0, 1 and 2: stdin, stdout and stderr), which are always inherited. Using spawn* functions, all inheritable handles and all inheritable file descriptors are inherited. Using the subprocess module, all file descriptors except standard streams are closed, and inheritable handles are only inherited if the close_fds parameter is False.

The following example uses the dir_fd parameter of the **os.open()** function to open a file relative to a given directory:

```python
import os
dir_fd = os.open('somedir', os.O_RDONLY)
def opener(path, flags):
    return os.open(path, flags, dir_fd=dir_fd)

with open('spamspam.txt', 'w', opener=opener) as f:
    print('This will be written to somedir/spamspam.txt', file=f)

os.close(dir_fd)  # don't leak a file descriptor
```