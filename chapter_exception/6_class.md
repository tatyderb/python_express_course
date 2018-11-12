## Свои исключения

Старайтесь их не делать. Поищите в иерархии уже существующих наиболее подходящий.

Иногда специфика задачи требует свои исключения. Например, когда рассчетная задача и какой-то параметр (например, размер трещины) вдруг становится невозможным физически (отрицательным или слишком большим). Тогд имеет смысл ввести свое исключение. Но можно использовать ValueError.

Простейший пример: в исключении нужно только имя типа. Тогда наследуйтесь от Exception и ничего не изменяйте.
```python
class MyException(Exception):
    pass
```
Использовать точно так же, как другие типы исключений.

Пример посложнее: добавим новое исключение HostNotFound, который содержит в себе имя хоста.

```python
class HostNotFound(Exception):
    def __init__( self, host ):
        self.host = host
        Exception.__init__(self, 'Host Not Found exception: missing %s' % host)
```
использование:
```python
try:
    raise HostNotFound("taoriver.net")
except HostNotFound, exc:
    # Handle exception.
    print exc               # -> 'Host Not Found exception: missing taoriver.net'
    print exc.host          # -> 'taoriver.net'
```
