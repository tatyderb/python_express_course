## Сжатые файлы

Используйте пакеты для чтения и записи.

```python
# gzip compression
import gzip

with gzip.open('somefile.gz', 'rt') as fin:
    text = fin.read()
    
with gzip.open('otherfile.gz', 'wt') as fout:
    fout.write(text)    
```

При этом выполняется кодирование/декодирование юникода. Если хотите писать как есть, используйте бинарную моду 'rb' и 'wb'.

| Архивация | Пакет |
|--|--|
| gzip | gzip |
| bz2 | bz2 |