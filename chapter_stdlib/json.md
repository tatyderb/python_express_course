# JSON

**Сериализация** - представление данных в удобном для пересылки по сети виде.

Разработка схемы сохранения сохранения данных.

Версионность. Обратная и прямая совместимость. 

Почему не стоит использовать pickle.

## Источники

* [https://pythonspot.com/tag/json/](https://pythonspot.com/tag/json/)
* [https://www.programiz.com/python-programming/json](https://www.programiz.com/python-programming/json) - описание функций по нему
* [https://realpython.com/python-json/](https://realpython.com/python-json/) - сериализация классов по нему

## JSON терминолгия

JSON - JavaScript Object Notation. Обычно используется для обмена данными между сервером и веб-приложениями.

Как выглядит типичные данные на json? Очень похоже на словарь (dict) в python.

```python
{
    "firstName": "Jane",
    "lastName": "Doe",
    "hobbies": ["running", "sky diving", "singing"],
    "age": 35,
    "children": [
        {
            "firstName": "Alice",
            "age": 6
        },
        {
            "firstName": "Bob",
            "age": 8
        }
    ]
}
```

Таблица соотвествия встроенных типов данных в Python и json.

Encoder, наследованный от json.JSONEncoder

Python | JSON
---|---
dict | object
list (tuple) | array
str | string
int, float | number
True | true
False | false
None | null
класс | JSON

## import json

Пакет json входит в стандартную поставку. 

## Разбор JSON данных (parse json)

### Разбор строки json.loads (s - значит строка)

Обычно json представляют в виде строки. Строка превращается в словарь функцией **loads(str)**:
```python
import json

person = '{"name": "Bob", "languages": ["English", "Fench"]}'
person_dict = json.loads(person)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print( person_dict)

# Output: ['English', 'French']
print(person_dict['languages'])
```

### Чтение из файла json.load

Сохраним данные в формате json в файле person.json:
```python
{"name": "Bob", 
"languages": ["English", "Fench"]
}
```

Прочитаем этот файл и конвертируем данные в словарь:
```python
import json

with open('person.json') as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(data)
```

## Конвертация в json

### Конвертация словаря в строку json.dumps (s - значит строка)

```python
import json

person_dict = {'name': 'Bob',
'age': 12,
'children': None
}
person_json = json.dumps(person_dict)

# Output: {"name": "Bob", "age": 12, "children": null}
print(person_json)
```

### Конвертация словаря в файл json.dump

```python

import json

person_dict = {
    "name": "Bob",
    "languages": ["English", "Fench"],
    "married": True,
    "age": 32
}

with open('person.txt', 'w') as json_file:
  json.dump(person_dict, json_file)
```

Получим файл person.txt:
```python
{"name": "Bob", "languages": ["English", "Fench"], "married": true, "age": 32}
```

#№# Свой формат разделителей

Если не устраивают разделители , и : между полями, то можно задать свой набор разделителей в параметре separators=(". ", " = ").

Значения по умолчанию  separators=(", ", ": ")

```python
import json

x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

# use . and a space to separate objects, and a space, a = and a space to separate keys from their values:
print(json.dumps(x, indent=4, separators=(". ", " = ")))
```
Получим
```python
{
    "name" = "John".
    "age" = 30.
    "married" = true.
    "divorced" = false.
    "children" = [
        "Ann".
        "Billy"
    ],
    "pets" = null.
    "cars" = [
        {
            "model" = "BMW 230".
            "mpg" = 27.5
        }.
        {
            "model" = "Ford Edge".
            "mpg" = 24.1
        }
    ]
}
```

### Типы данных

Заметим, что load и loads возвращает словарь с ключами-строками. Если ранее ключи были числами, то эта информация потеряна.

```python
loads(dumps(x)) != x   # если х был ключом НЕ строкой
```

### pretty print (удобная печать) через indent

Для анализа (и поиска ошибок) удобно печатать json в human-readable виде.

```python
import json

person_string = '{"name": "Bob", "languages": "English", "numbers": [2, 1.6, null]}'

# Getting dictionary
person_dict = json.loads(person_string)

# Pretty Printing JSON string back
print(json.dumps(person_dict, indent = 4, sort_keys=True))
```
* indent - отступы в виде количества пробелов (None по умолчанию);
* sort_keys - надо ли сортировать ключи (False по умолчанию).

получим:
```python
{
    "languages": "English",
    "name": "Bob",
    "numbers": [
        2,
        1.6,
        null
    ]
}
```

## Сериализация несериализуемых объектов (классов)

### \_\_dict\_\_ или vars()

Можно из несериализуемого объекта ob делаеть сериализуемый словарь, используя \_\_dict\_\_ явно или как результат вызова функции vars().

```python
import json

class Person(object):
    def __init__(self):
        self.name = 'John'
        self.age = 25
        self.id = 1

person = Person()

#save to file
dt = {}
dt.update(vars(person))
print(dt, type(dt))
with open("/home/test/person.txt", "w") as file:
    json.dump(dt, file)
```

В файле /home/test/person.txt получим
```python
{"id": 1, "age": 25, "name": "John"}
```

Если у нас есть вложенные объекты, то лучше передать функцию, которая из объекта делает словарь:

```python
# https://blog.softhints.com/python-convert-object-to-json-3-examples/
import json

class error:
    def __init__(self):
        self.errorCode="server issue"
        self.errorMessage="201"


class BaseRespone():
    def __init__(self):
        self.success = "data fetch successfully"
        self.data={"succss":"msg"}
        self.error1 = error()

def obj_to_dict(obj):
   return obj.__dict__


bs = BaseRespone()
# json_string = json.dumps(bs.__dict__,  default = obj_to_dict)
json_string = json.dumps(bs,  default = obj_to_dict)
print('json_string=', json_string, type(json_string))

json_string1 = json.loads(json_string)
print('json_string1=', json_string1, type(json_string1))
```
получим:
```python
('json_string=', '{"error1": {"errorCode": "server issue", "errorMessage": "201"}, "data": {"succss": "msg"}, "success": "data fetch successfully"}', <type 'str'>)
('json_string1=', {u'error1': {u'errorCode': u'server issue', u'errorMessage': u'201'}, u'data': {u'succss': u'msg'}, u'success': u'data fetch successfully'}, <type 'dict'>)
```

Или, как мы уже видели ранее, используем встроенную функцию **vars()**:
```python
json_string = json.dumps(bs,  default = vars)
```

### Упрощение представлия объекта

Возьмем комплексное число. Оно не сериализуется.

```python
>>> z = 3 + 8j
>>> type(z)
<class 'complex'>
>>> json.dumps(z)
TypeError: Object of type 'complex' is not JSON serializable
```
Попробуем упростить его представление и восстановить объект из упрощеного представления, чтобы полученный объект был равен исходному.

```python
>>> z.real
3.0
>>> z.imag
8.0
>>> complex(3, 8) == z
True
```
То есть для представления комплексного числа достаточно значений z.real и z.imag.

Сериализуем и десериализуем объект, пользуясь этим упрощенным представлением.

### Encoding Custom Type via default parameter

Передадим в метод dump параметр **default**. Питон будет вызывать переданную функцию каждый раз, когда объект не будет сериализоваться естественным образом (как строки, списки или числа и тп.)

```python
class Elf:
    pass
def encode_complex(z):
    if isinstance(z, complex):
        return (z.real, z.imag)
    else:
        type_name = z.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")
        
>>> json.dumps(9 + 5j, default=encode_complex)
'[9.0, 5.0]'
>>> json.dumps(elf, default=encode_complex)
TypeError: Object of type 'Elf' is not JSON serializable
```
Можно закодировать комплесное число как tuple, можно сделать из него словарь (как мы делали раньше).

### Encoding Custom Type via JSONEncoder subclass

Напишем класс, который наследуется от класса **JSONEncoder** и переопределяет метод **default(self, z)**.

```python
class ComplexEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, complex):          # комплексное число? упрощаем!
            return (z.real, z.imag)
        else:                               # остальные объекты - обычное поведение
            super().default(self, z)
```
вызываем json.dumps() или ComplexEncoder().encode():
```python
>>> json.dumps(2 + 5j, cls=ComplexEncoder)
'[2.0, 5.0]'

>>> encoder = ComplexEncoder()
>>> encoder.encode(3 + 6j)
'[3.0, 6.0]'
```

### Decoding Custom Types

Проблема: если мы декодируем полученную строку '[3.0, 6.0]', то получим список чисел, а не комплексное число.

```python
>>> complex_json = json.dumps(4 + 17j, cls=ComplexEncoder)
>>> json.loads(complex_json)
[4.0, 17.0]   
```
Нужно определить какие данные *необходимы и достаточны* для восстановления прежнего объекта.

Допустим, у нас есть такой файл complex_data.json:
```python
{
    "__complex__": true,
    "real": 42,
    "imag": 36
}
```
Восстановим из него данные с помощью функции:
```python
def decode_complex(dct):
    if "__complex__" in dct:
        return complex(dct["real"], dct["imag"])
    return dct
```
Восстановление:
```python
>>> with open("complex_data.json") as complex_data:
...     data = complex_data.read()
...     z = json.loads(data, object_hook=decode_complex)
... 
>>> type(z)
<class 'complex'>
```

Даже если объект состоит из набора таких данных, то этот подход продолжет работать. Пусть в файле лежит список комплексных чисел:
```python
[
  {
    "__complex__":true,
    "real":42,
    "imag":36
  },
  {
    "__complex__":true,
    "real":64,
    "imag":11
  }
]
```
Восстановим их как раньше:
```python
>>> with open("complex_data.json") as complex_data:
...     data = complex_data.read()
...     numbers = json.loads(data, object_hook=decode_complex)
... 
>>> numbers
[(42+36j), (64+11j)]
```

# Задача

Дописать в проект игры save и load.

Можно в каждом классе реализовать функцию to_json и статический метод from_json.