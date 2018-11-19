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
