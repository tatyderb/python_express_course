## Чтение и запись в файл

Часто используемые операции над файлами:

| Операция | Интерпретация | 
|---|-----|
| output = open(r’C:\spam', 'w') | Открывает файл для записи | 
| input = open('data', 'r') | Открывает файл для чтения | 
| input = open('data') | То же самое, 'r' - по умолчанию | 
| aString = input.read() | Чтение файла целиком в единственную строку | 
| aString = input.read(N) | Чтение следующих N символов (или байтов) в строку | 
| aString = input.readline() | Чтение следующей текстовой строки (включая символ конца строки) в строку | 
| aList = input.readlines() | Чтение файла целиком в список строк (включая символ конца строки) | 
| output.write(aString) | Запись строки символов (или байтов) в файл | 
| output.writelines(aList) | Запись всех строк из списка в файл | 
| output.close() | Закрытие файла вручную (выполняется по окончании работы с файлом) | 
| output.flush() | Выталкивает выходные буферы на диск, файл остается открытым | 
| anyFile.seek(N) | Изменяет текущую позицию в файле для следующей операции, смещая ее на N байтов от начала файла. | 
| for line in open('data'):<br/>&nbsp;&nbsp;операции над line | Итерации по файлу, построчное чтение | 
| open('f.txt', encoding='latin-1') | Файлы с текстом Юникода в Python 3.0 (строки типа str) | 
| open('f.bin', 'rb') | Файлы с двоичными данными в Python 3.0 (строки типа bytes) | 

### Читаем файл построчно

Если файл текстовый, то это итерируемая (по строкам) величина:

```python
with open('some.txt') as fin:
    for line in fin:
        print(line)
```

Отдельно читаем первую строку, потом остальные:
```python
with open('some.txt') as fin:
    line = next(fin)
    print('first line:', line)
    
    for line in fin:
        print(line)
```

Или с помощью метода `readline()`:
```python
with open('some.txt') as fin:
    line = fin.readline()
    print('first line:', line)
    
    while line:
        line = fin.readline()
        print(line)
```

### Текст - список строк

Чтобы прочитать весь файл в список строк, используйте функцию `readlines` (-s говорит, что "много") или преобразуйте объект файл в список.

```python
with open('some.txt') as fin:
    text = fin.readlines()
```
или
```python
with open('some.txt') as fin:
    text = list(fin)
```

### Чтение бинарного потока

Функция **read(size)** возвращает строку, если файл открывали в текстовой моде или байтовый объект (бинарная мода).

Если `size` не указан или <0, то пытается прочитаться весь файл. Забота о памяти - это ваша проблема, а не питона. Не читайте так большие файлы.

Положительная `size` - размер буфера для чтения в байтах.

Если файл закончился, `read` вернет пустую строку ''.

```python
with open('text.txt') as f:
    s = f.read(1)
    print(s)        # H
    s = f.read()
    print(s)        # ello, world!\nThe end.\n
```

### Запись в файл print

```python
print('Hello', file=fin)
```

### Запись в файл write
```python
fin.write(b'Hello')     # b'Hello' - массив байт, не строка
```

### Чтение-запись текста как потока байтов

Не забывайте, что нужно кодировать и декодировать байты.

```python
with open('somefile.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')

with open('somefile.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))
```

### Открыть файл на запись, только если такого файла нет

Не хотим испортить уже существующий файл. Хотим открывать только новый. 

Использовать 'x' вместо 'w' в режиме открытия файла.