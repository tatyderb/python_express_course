## time - clock time

**timestamp** - количество секунд с 1 января 1970 года (Epoch).

Так как функции этого модуля обращаются к аналогичным функциям языка С, то они платформено-зависимые.

* **time()** - на основе системного вызова time() - "wall clock"
* **monotonic()** - used to measure elapsed time in a long-running process because it is guaranteed never to move backwards, even if the system time is changed.
* **perf_counter()** - самое высокое разрешение для коротких измерений времени (обычно измерение производительности).
* **clock()** - cpu time.
* **process_time()** -  returns the combined processor time and system time

### Сравним часы

TODO: сделать сравнение в виде таблицы:
|process_time | adjustable | implementation | monotonic | resolution | current |
|--|--|--|--|--|--|
|process_time | adjustable | implementation | monotonic | resolution | current |

```python
    clock:
        adjustable    : False
        implementation: clock()
        monotonic     : True
        resolution    : 0.001
        current       : 0.25

    monotonic:
        adjustable    : False
        implementation: clock_gettime(CLOCK_MONOTONIC)
        monotonic     : True
        resolution    : 3.8e-07
        current       : 519313.118129497

    perf_counter:
        adjustable    : False
        implementation: clock_gettime(CLOCK_MONOTONIC)
        monotonic     : True
        resolution    : 3.8e-07
        current       : 519313.118386327

    process_time:
        adjustable    : False
        implementation: clock_gettime(CLOCK_PROCESS_CPUTIME_ID)
        monotonic     : True
        resolution    : 0.015625
        current       : 0.25

    time:
        adjustable    : True
        implementation: clock_gettime(CLOCK_REALTIME)
        monotonic     : False
        resolution    : 0.015625
        current       : 1524093750.628306
```

### time.time() - wall clock time

```python
import time

print('time()               =', time.time())        # 1524116343.1965854
print('ctime()              =', time.ctime())       # Thu Apr 19 08:39:03 2018
later = time.time() + 15                            # 15 sec later
print('ctime(time()+15 sec) =', time.ctime(later))  # Thu Apr 19 08:39:18 2018
```

Так как _time()_ обращается к system clock, и они могут изменяться, когда пользовательские или системные сервисы пытаются синхронизировать время у многих компьютеров, то вызывая последовательно _time()_ можно получить времена как по возрастанию, так и по убыванию.

### time.monotonic() - время строго по возрастанию

Чтобы гарантированно получить время по возрастанию, используйте **monotonic()**.

Это не время с Эпохи. Это время, чтобы можно было сравнивать.

```python
import time

start = time.monotonic()
time.sleep(0.1)
end = time.monotonic()
print('start : {:>9.2f}'.format(start))
print('end   : {:>9.2f}'.format(end))
print('span  : {:>9.2f}'.format(end - start))
```
Получим:
```python
start : 543779.74
end   : 543779.84
span  :      0.10
```

### Processor Clock Time

_time()_ - возвращает wall clock time, **clock()** - processor clock time - реальное время, которое потратила программа на выполнение.

В примере считается md5 checksum. 

```python
import hashlib
import time

# Data to use to calculate md5 checksums
data = open(__file__, 'rb').read()

for i in range(5):
    h = hashlib.sha1()
    print(time.ctime(), ': {:0.3f} {:0.3f}'.format(
        time.time(), time.clock()))
    for i in range(300000):
        h.update(data)
    cksum = h.digest()
```
Получим:
```python
Thu Apr 19 09:19:08 2018 : 1524118748.980 0.234
Thu Apr 19 09:19:10 2018 : 1524118750.501 1.687
Thu Apr 19 09:19:12 2018 : 1524118752.074 3.155
Thu Apr 19 09:19:13 2018 : 1524118753.588 4.609
Thu Apr 19 09:19:15 2018 : 1524118755.113 6.077
```
time() изменился на 6.132999897, clock() - на 5.843 секунд.

Обычно, если процессор ничего не делает, processor time почти не изменяется. В примере процесс спит. Время wall clock идет, а processor time небольшой.

```python
import time

template = '{} - {:0.2f} - {:0.2f}'

print(template.format(
    time.ctime(), time.time(), time.clock())
)

for i in range(3, 0, -1):
    print('Sleeping', i)
    time.sleep(i)
    print(template.format(
        time.ctime(), time.time(), time.clock())
    )
```
получим
```python
Thu Apr 19 09:29:30 2018 - 1524119370.68 - 0.19
Sleeping 3
Thu Apr 19 09:29:33 2018 - 1524119373.68 - 0.19
Sleeping 2
Thu Apr 19 09:29:35 2018 - 1524119375.68 - 0.19
Sleeping 1
Thu Apr 19 09:29:36 2018 - 1524119376.69 - 0.19
```

Вызов _sleep()_ приостанавливает выполнение текущего thread до тех пор, пока система его не разбудет. Если в программе 1 thread, то приложение ничего не делает пока спит.

### Performance Counter

Мерить производительность лучше с помощью **perf_counter()**

Как и в _monotonic()_, это не время с Эпохи, это время чтобы сравнивать.

```python
import hashlib
import time

# Data to use to calculate md5 checksums
data = open(__file__, 'rb').read()

loop_start = time.perf_counter()

for i in range(5):
    iter_start = time.perf_counter()
    h = hashlib.sha1()
    for i in range(300000):
        h.update(data)
    cksum = h.digest()
    now = time.perf_counter()
    loop_elapsed = now - loop_start
    iter_elapsed = now - iter_start
    print(time.ctime(), ': {:0.3f} {:0.3f}'.format(
        iter_elapsed, loop_elapsed))
```
получим:
```python
Thu Apr 19 09:57:08 2018 : 2.216 2.216
Thu Apr 19 09:57:10 2018 : 2.212 4.428
Thu Apr 19 09:57:13 2018 : 2.192 6.620
Thu Apr 19 09:57:15 2018 : 1.856 8.477
Thu Apr 19 09:57:16 2018 : 1.915 10.392
```

### Время как структура struct_time

Когда нужно время, разбитое на составляющие части (год, месяц, день, час,  день недели и тп), используйте struct_time

* **gmtime()** - время в UTC
* **localtime()** - время в локальной таймзоне компьютера
* **mktime()** - из времени (структуры) получить timestamp

```python
import time

def show_struct(s):
    print('  tm_year :', s.tm_year)
    print('  tm_mon  :', s.tm_mon)
    print('  tm_mday :', s.tm_mday)
    print('  tm_hour :', s.tm_hour)
    print('  tm_min  :', s.tm_min)
    print('  tm_sec  :', s.tm_sec)
    print('  tm_wday :', s.tm_wday)
    print('  tm_yday :', s.tm_yday)
    print('  tm_isdst:', s.tm_isdst)


print('gmtime:')
show_struct(time.gmtime())
print('\nlocaltime:')
show_struct(time.localtime())
print('\nmktime:', time.mktime(time.localtime()))
```
получим:
```python
gmtime:
  tm_year : 2018
  tm_mon  : 4
  tm_mday : 19
  tm_hour : 7
  tm_min  : 4
  tm_sec  : 25
  tm_wday : 3
  tm_yday : 109
  tm_isdst: 0

localtime:
  tm_year : 2018
  tm_mon  : 4
  tm_mday : 19
  tm_hour : 10
  tm_min  : 4
  tm_sec  : 25
  tm_wday : 3
  tm_yday : 109
  tm_isdst: 0

mktime: 1524121465.0
```

### Time zone

Функции определения времени используют таймзоны заданные в программе или в таймзоне системы по умолчанию. Изменение таймзоны не изменяет реальное время, только его представление.

Для изменения таймзоны установите с помощью **tzset()** переменную окружения TZ. У таймзоны много специфической информации. Обычно используют имя таймзоны, чтобы библиотеки более низкого уровня получили эту информацию.

Изменим несколько раз таймзону и посмотрим на результат работы функций:

```python
import time
import os


def show_zone_info():
    print('  TZ    :', os.environ.get('TZ', '(not set)'))
    print('  tzname:', time.tzname)
    print('  Zone  : {} ({})'.format(
        time.timezone, (time.timezone / 3600)))
    print('  DST   :', time.daylight)
    print('  Time  :', time.ctime())
    print()


print('Default :')
show_zone_info()

ZONES = [
    'GMT',
    'Europe/Amsterdam',
]

for zone in ZONES:
    os.environ['TZ'] = zone
    time.tzset()
    print(zone, ':')
    show_zone_info()
```
получим:
```python
Default :
  TZ    : Europe/Moscow
  tzname: ('MSK', 'MSD')
  Zone  : -10800 (-3.0)
  DST   : 1
  Time  : Thu Apr 19 10:15:33 2018

GMT :
  TZ    : GMT
  tzname: ('GMT', '   ')
  Zone  : 0 (0.0)
  DST   : 0
  Time  : Thu Apr 19 07:15:33 2018

Europe/Amsterdam :
  TZ    : Europe/Amsterdam
  tzname: ('CET', 'CEST')
  Zone  : -3600 (-1.0)
  DST   : 1
  Time  : Thu Apr 19 09:15:33 2018
```

## Преобразование времени в строку и разбор строки

* **strftime(format, _tupletime_)** - из структуры в строку по формату, если _tupletime_ не задан, то берется текущее время.
* **strptime(string, _format_)** - из строки в структуру (как в gmtime или localtime)

Таблица преобразования типов:
|From \ To | timestamp | time tuple | string |
|-|-|-|-|
| timestamp |-| gmtime (UTC) <br/> localtime (local time)|-|
| time tuple | [calendar.timegm](https://docs.python.org/3/library/calendar.html#calendar.timegm) (UTC) <br/> mktime (local time)|-| strftime |
| string |-| strptime |-|

```python
import time


def show_struct(s):
    print('  tm_year :', s.tm_year)
    print('  tm_mon  :', s.tm_mon)
    print('  tm_mday :', s.tm_mday)
    print('  tm_hour :', s.tm_hour)
    print('  tm_min  :', s.tm_min)
    print('  tm_sec  :', s.tm_sec)
    print('  tm_wday :', s.tm_wday)
    print('  tm_yday :', s.tm_yday)
    print('  tm_isdst:', s.tm_isdst)


now = time.ctime(1483391847.433716)
print('Now:', now)

parsed = time.strptime(now)
print('\nParsed:')
show_struct(parsed)

print('\nFormatted:',
      time.strftime("%a %b %d %H:%M:%S %Y", parsed))
```
получим
```python
Now: Tue Jan  3 00:17:27 2017

Parsed:
  tm_year : 2017
  tm_mon  : 1
  tm_mday : 3
  tm_hour : 0
  tm_min  : 17
  tm_sec  : 27
  tm_wday : 1
  tm_yday : 3
  tm_isdst: -1

Formatted: Tue Jan 03 00:17:27 2017
```

### Таблица форматов

| Directive | Meaning |
|-|----|
| %a | Locale’s abbreviated weekday name. |
| %A | Locale’s full weekday name. |
| %b | Locale’s abbreviated month name. |
| %B | Locale’s full month name. |
| %c | Locale’s appropriate date and time representation. |
| %d | Day of the month as a decimal number [01,31]. |
| %H | Hour (24-hour clock) as a decimal number [00,23]. |
| %I | Hour (12-hour clock) as a decimal number [01,12]. |
| %j | Day of the year as a decimal number [001,366]. |
| %m | Month as a decimal number [01,12]. |
| %M | Minute as a decimal number [00,59]. |
| %p | Locale’s equivalent of either AM or PM. |
| %S | Second as a decimal number [00,61]. |
| %U | Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0. |
| %w | Weekday as a decimal number [0(Sunday),6]. |
| %W | Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0. |
| %x | Locale’s appropriate date representation. |
| %X | Locale’s appropriate time representation. |
| %y | Year without century as a decimal number [00,99]. |
| %Y | Year with century as a decimal number. |
| %z | Time zone offset indicating a positive or negative time difference from UTC/GMT of the form +HHMM or -HHMM, where H represents decimal hour digits and M represents decimal minute digits [-23:59, +23:59]. |
| %Z | Time zone name (no characters if no time zone exists). |
| %% | A literal '%' character. |
