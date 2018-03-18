# Строки

## Строковые типы

* [bytearray](https://docs.python.org/3/library/stdtypes.html?highlight=bytearray#bytearray)
* [bytes](https://docs.python.org/3/library/stdtypes.html?highlight=bytearray#bytes) (НЕизменяемое)
* [str](https://docs.python.org/3/library/stdtypes.html?highlight=bytearray#text-sequence-type-str) (НЕизменяемое)

## Как задаются строки

* 'в одинарных кавычках', "двойных кавычках", 'фильм "Титаник"' или "фильм 'Титаник'"
* тройные кавычки из ' или ":
  * многострочная строка; (html)
  * docstring
  * комментарий (лучше так не делать)
* 'C:\\\\new\\\\text.dat' - escape-последовательности \\n, \\t, \\r
* r'C:\\new\\text.dat' - экранирует escape-последовательности (сделано, чтобы удобно было писать regexp)
* u'Unicode string' - строка юникода

## Методы строки

* сложение **'abc'+'xyzb**
```python
>>> 'abc'+'xyz'
'abcxyz'
```

* умножение **'hi'*3**
```python
>>> 'hi' * 3
'hihihi'
```

* <, >, <=, >=, ==, != - _побайтовое_ сравнение строк
  * символы юникода могут быть представлены по-разному, например, символ 0x00C5 может быть представлен как \[0xE2, 0x84, 0xAB\], \[0xC3, 0x85\] и \[0x41, 0xCC, 0x8A\]. 
  
Используем **unicodedata.normalize(form='NFKD')** "Normalization Form Compatibility Decomposition" – нормализация в форме совместимой декомпозиции), то, передав ей строку, содержащую символ 0x00C5, представленный любой из допустимых последовательностей байтов, мы получим строку с символами в кодировке UTF-8, где интересующий нас символ всегда будет представлен последовательностью \[0x41, 0xCC, 0x8A\].

  * порядок сортировки некоторых символов зависит от языка, в шведском a с двумя точками будет идти после z, а немецком он будет сортироваться, как если бы это была строка 'ae'
  
  * подробнее о проблемах сортировки юникода см unicode.org/reports/tr10

* Срезы
```python
>>>'Hello'[1]
e
>>>'Hello'[1:3]
el
>>>'Hello, world!'[1:10:2]
'el,wr'
```

* Проверка, что **строка пустая**
```python
if s:
    print('Строка пустая')
else:
    print('Строка НЕ пустая')
```
Потому что:
```python
>>> bool(s)
False
>>> bool('Hello')
True
```

* **in** - проверка, что в строке содержится подстрока
```python
>>> 'el' in 'Hello'
True
```
*   Проверки:
    * str.**isalnum**()
    * str.**isalpha**()
    * str.**isdecimal**()
    * str.**isdigit**()
    * str.**isidentifier**()
    * str.**islower**()
    * str.**isnumeric**()
    * str.**isprintable**()
    * str.**isspace**()
    * str.**istitle**()
    * str.**isupper**()

*   Большие и маленькие буквы:
    * str.**capitalize**()
    * str.**casefold**()
    * str.**swapcase**()
    * str.**title**()
    * str.**upper**()
    * str.**lower**()
    
*   Выравнивание:
    * str.**center**()
    * str.**ljust**()
    * str.**rjust**()

*   Убрать символы (пробелы)
    * str.**lstrip**()
    * str.**rstrip**()
    * str.**strip**()
```python
>>> '   spacious   '.strip()
'spacious'
>>> 'www.example.com'.strip('cmowz.')
'example'
>>> comment_string = '#....... Section 3.2.1 Issue #32 .......'
>>> comment_string.strip('.#! ')
'Section 3.2.1 Issue #32'
```
* Из табуляций в пробелы
    * str.**expandtabs**()
```python
>>> '01\t012\t0123\t01234'.expandtabs()
'01      012     0123    01234'
>>> '01\t012\t0123\t01234'.expandtabs(4)
'01  012 0123    01234'
```
*   Делаем строку
    * str.**zfill**() - заполняем строку нулями.
```python
>>> "42".zfill(5)
'00042'
>>> "-42".zfill(5)
'-0042'
```
*   Кодировка:
    * str.**encode**(encoding="utf-8")

*   Шифрование:
    * str.**maketrans**()
    * str.**translate**(table)

*   Форматирование:
    * str.**format**()
    * str.**format_map**()

*   Проверки (подстрока в строке)
    * str.**count**(sub) - сколько раз входит (без пересечений)
    * **in** - поиск подстроки в строке
    * str.**endswith**(sub) - str оканчивается на sub
    * str.**startswith**(sub) - 

*   **Индекс** начала подстроки в строке, (иначе проверяем как 'el' in 'Hello')
    * str.**find**(sub\[, start\[, end\]\]) - возвращает -1, если подстроки нет
    * str.**index**(sub\[, start\[, end\]\]) - кидает ValueError, если подстроки нет
    * str.**rfind**(sub\[, start\[, end\]\])
    * str.**rindex**(sub\[, start\[, end\]\])

*   Разделение и склейка
    * str.**partition**() - разделить на 3 части - до, разделитель, после
    * str.**rpartition**()
    * str.**rsplit**()
    * str.**split**(sep=None, maxsplit=-1) - разделить по sep на много частей
```python
>>> '1,2,3'.split(',')
['1', '2', '3']
>>> '1,2,3'.split(',', maxsplit=1)
['1', '2,3']
>>> '1,2,,3,'.split(',')
['1', '2', '', '3', '']
```
    * str.**join**(iterable)
```python
>>> a = ['hi', 'ha', 'ho']
>>> '-'.join(a)
'hi-ha-ho'
```
    * str.**splitlines**()
```python
>>> 'ab c\n\nde fg\rkl\r\n'.splitlines()
['ab c', '', 'de fg', 'kl']
>>> 'ab c\n\nde fg\rkl\r\n'.splitlines(keepends=True)
['ab c\n', '\n', 'de fg\r', 'kl\r\n']
```
*   Поиск и замена:
    * str.**replace**(old, new, \[count\])
```python
>>>'AAAAAA'.replace('AA', 'A')
'AAA'
>>> S = 'xxxxSPAMxxxxSPAMxxxx'
>>> S.replace('SPAM', 'EGGS')    # Заменить все найденные подстроки
‘xxxxEGGSxxxxEGGSxxxx’
>>> S.replace('SPAM', 'EGGS', 1) # Заменить одну подстроку
'xxxxEGGSxxxxSPAMxxxx'
```

*   Коды символов
    * **ord**(символ) - ASCII code символа
    * **chr**(ascii_code) - получить символ
```python
>>> ord('a')
97
>>> chr(97)
'a'
```