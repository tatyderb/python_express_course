## Запуск сторонней программы - модуль subprocess

Модуль создает отдельные процессы. Сделан для удобного запуска сторонних команд.

Запускаем функцией **(subprocess.run())[https://docs.python.org/3/library/subprocess.html]** (начиная с версии 3.5). Если нужно что-то специфическое, используем непосредственно внутренний интерфейс **Popen**.

В старых версиях были функции **call**, **check**, **check_output**.

Не забываем **import subprocess**

```
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None)
```
Запускает то, что передано в аргументах, ждет когда исполнится и возвращает экземпляр CompletedProcess.

```python
>>> subprocess.run(["ls", "-l"])  # doesn't capture output
CompletedProcess(args=['ls', '-l'], returncode=0)

>>> subprocess.run("exit 1", shell=True, check=True)
Traceback (most recent call last):
  ...
subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1

>>> subprocess.run(["ls", "-l", "/dev/null"], stdout=subprocess.PIPE)
CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0,
stdout=b'crw-rw-rw- 1 root root 1, 3 Jan 23 16:23 /dev/null\n')
```
При shell=True можно не только задать одной строкой `'ls -l /dev/null'`, но и использовать переменные `'cd $HOME'` 

Законченный код:
```python
try:
    completed = subprocess.run(
        'echo to stdout; echo to stderr 1>&2; exit 1',
        check=True,
        shell=True,
        stdout=subprocess.PIPE,
    )
except subprocess.CalledProcessError as err:
    print('ERROR:', err)
else:
    print('returncode:', completed.returncode)
    print('Have {} bytes in stdout: {!r}'.format(
        len(completed.stdout),
        completed.stdout.decode('utf-8'))
    )
# OUTPUT:    
# to stderr
# ERROR: Command 'echo to stdout; echo to stderr 1>&2; exit 1'
# returned non-zero exit status 1    
```
### отключим check=True:
```python
import subprocess

try:
    completed = subprocess.run(
        'echo to stdout; echo to stderr 1>&2; exit 1',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
except subprocess.CalledProcessError as err:
    print('ERROR:', err)
else:
    print('returncode:', completed.returncode)
    print('Have {} bytes in stdout: {!r}'.format(
        len(completed.stdout),
        completed.stdout.decode('utf-8'))
    )
    print('Have {} bytes in stderr: {!r}'.format(
        len(completed.stderr),
        completed.stderr.decode('utf-8'))
    )
# OUTPUT:
# returncode: 1
# Have 10 bytes in stdout: 'to stdout\n'
# Have 10 bytes in stderr: 'to stderr\n'    
```
**run() c check=True эквивалентно check_call()**

### Работа непосредственно с PIPE

Можно использовать непосредственно Popen, чтобы проконтролировать как выполняется команда и как обрабатываются ее input и output. Например, передавая различные аргументы в stdin, stdout и stderr можно имитировать изменения в os.popen().

```python
import subprocess

print('read:')
proc = subprocess.Popen(
    ['echo', '"to stdout"'],
    stdout=subprocess.PIPE,
)
stdout_value = proc.communicate()[0].decode('utf-8')
print('stdout:', repr(stdout_value))

# OUTPUT:
# read:
# stdout: '"to stdout"\n'
```
Подадим данные на stdin.

Для одноразовой посылки на stdin используйте communicate(). Аналогично использованию os.popen() с модой 'w'.
```python
print('write:')
proc = subprocess.Popen(
    ['cat', '-'],
    stdin=subprocess.PIPE,
)
proc.communicate('stdin: to stdin\n'.encode('utf-8'))

# OUTPUT:
# write:
# stdin: to stdin
```

#### Заменяем shell pipe line

Если вам хочется получить (отфильтровать, подменить) передаваемые данные:
Заменяем shell pipe line `dmesg | grep hda`:
```python
p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
output = p2.communicate()[0]
```
Если передать `stdout=subprocess.DEVNULL`, то на `completed.stdout` попадет None.

Сразу и stdin, и stdout:
```python
import subprocess

print('popen2:')

proc = subprocess.Popen(
    ['cat', '-'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)
msg = 'through stdin to stdout'.encode('utf-8')
stdout_value = proc.communicate(msg)[0].decode('utf-8')
print('pass through:', repr(stdout_value))

# OUTPUT:
# popen2:
# pass through: 'through stdin to stdout'
```

#### Перехватываем stderr

```python
import subprocess

print('popen3:')
proc = subprocess.Popen(
    'cat -; echo "to stderr" 1>&2',
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
msg = 'through stdin to stdout'.encode('utf-8')
stdout_value, stderr_value = proc.communicate(msg)
print('pass through:', repr(stdout_value.decode('utf-8')))
print('stderr      :', repr(stderr_value.decode('utf-8')))

# OUTPUT:
# popen3:
# pass through: 'through stdin to stdout'
# stderr      : 'to stderr\n'
```

#### Перенаправляем stderr на стандартный stdout

`stderr = subprocess.STDOUT` вместо PIPE:

```python
import subprocess

print('popen4:')
proc = subprocess.Popen(
    'cat -; echo "to stderr" 1>&2',
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
msg = 'through stdin to stdout\n'.encode('utf-8')
stdout_value, stderr_value = proc.communicate(msg)
print('combined output:', repr(stdout_value.decode('utf-8')))
print('stderr value   :', repr(stderr_value))

# OUTPUT:
# popen4:
# combined output: 'through stdin to stdout\nto stderr\n'
# stderr value   : None
```

#### Цепочка вызовов

Одна команда перенаправляет выход на вход другой. Для иллюстрации напишем код, выполняющий `cat index.rst | grep ".. literalinclude" | cut -f 3 -d:` (заметим, его можно выполнить непосредственно subprocess.run, указав shell=True):
```python
import subprocess

cat = subprocess.Popen(
    ['cat', 'index.rst'],
    stdout=subprocess.PIPE,
)

grep = subprocess.Popen(
    ['grep', '.. literalinclude::'],
    stdin=cat.stdout,
    stdout=subprocess.PIPE,
)

cut = subprocess.Popen(
    ['cut', '-f', '3', '-d:'],
    stdin=grep.stdout,
    stdout=subprocess.PIPE,
)

end_of_pipe = cut.stdout

print('Included files:')
for line in end_of_pipe:
    print(line.decode('utf-8').strip())
```

#### TODO

Посмотреть, нужно ли добавлять примеры из:

https://pymotw.com/3/subprocess/

Interacting with Another Command и далее

Посмотреть кукбуки
