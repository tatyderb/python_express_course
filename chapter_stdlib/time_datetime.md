## datetime - time, date, date+time

Разбор и представление даты и времени, арифметические операции над ними, сравнение.

### datetime.time - чисто время (часы, минуты, секунды, милисекунды, таймзона)

Только время без даты.

```python
import datetime

t = datetime.time(1, 2, 3)
print(t)
print('hour       :', t.hour)
print('minute     :', t.minute)
print('second     :', t.second)
print('microsecond:', t.microsecond)
print('tzinfo     :', t.tzinfo)
```
получим:
```python
01:02:03
hour       : 1
minute     : 2
second     : 3
microsecond: 0
tzinfo     : None
```
**Диапазон данных:**

```python
import datetime

print('Earliest  :', datetime.time.min)
print('Latest    :', datetime.time.max)
print('Resolution:', datetime.time.resolution)
```
получим:
```python
Earliest  : 00:00:00
Latest    : 23:59:59.999999
Resolution: 0:00:00.000001
```

**Время не может устанавливаться точнее, чем в милисекундах**.

```python
import datetime

for m in [1, 0, 0.1, 0.6]:
    try:
        print('{:02.1f} :'.format(m),
              datetime.time(0, 0, 0, microsecond=m))
    except TypeError as err:
        print('ERROR:', err)
```
получим:
```python
1.0 : 00:00:00.000001
0.0 : 00:00:00
ERROR: integer argument expected, got float
ERROR: integer argument expected, got float
```

### datetime.date - дни, месяцы, года

```python
import datetime

today = datetime.date.today()
print(today)
print('ctime  :', today.ctime())
tt = today.timetuple()
print('tuple  : tm_year  =', tt.tm_year)
print('         tm_mon   =', tt.tm_mon)
print('         tm_mday  =', tt.tm_mday)
print('         tm_hour  =', tt.tm_hour)
print('         tm_min   =', tt.tm_min)
print('         tm_sec   =', tt.tm_sec)
print('         tm_wday  =', tt.tm_wday)
print('         tm_yday  =', tt.tm_yday)
print('         tm_isdst =', tt.tm_isdst)
print('ordinal:', today.toordinal())
print('Year   :', today.year)
print('Mon    :', today.month)
print('Day    :', today.day)
```
получаем:
```python
2018-04-19
ctime  : Thu Apr 19 00:00:00 2018
tuple  : tm_year  = 2018
         tm_mon   = 4
         tm_mday  = 19
         tm_hour  = 0
         tm_min   = 0
         tm_sec   = 0
         tm_wday  = 3
         tm_yday  = 109
         tm_isdst = -1
ordinal: 736803
Year   : 2018
Mon    : 4
Day    : 19
```

**ordinal** - количество _дней_ с 1 января 1 года.

```python
import datetime
import time

o = 736803
print('o               :', o)
print('fromordinal(o)  :', datetime.date.fromordinal(o))

t = time.time()
print('t               :', t)
print('fromtimestamp(t):', datetime.date.fromtimestamp(t))
```
получаем:
```python
o               : 736803
fromordinal(o)  : 2018-04-19
t               : 1524125286.857128
fromtimestamp(t): 2018-04-19
```

**Диапазон date**

```python
import datetime

print('Earliest  :', datetime.date.min)
print('Latest    :', datetime.date.max)
print('Resolution:', datetime.date.resolution)
```
получаем:
```python
Earliest  : 0001-01-01
Latest    : 9999-12-31
Resolution: 1 day, 0:00:00
```

** Создадим дату в виде строки и заменим в строке год**
```python
import datetime

d1 = datetime.date(2008, 3, 29)
print('d1:', d1.ctime())

d2 = d1.replace(year=2009)
print('d2:', d2.ctime())
```
получим
```python
d1: Sat Mar 29 00:00:00 2008
d2: Sun Mar 29 00:00:00 2009
```

Острожнее с таким заменами. Вы можете в дате 29 февраля високосного года заменить год на невисокосный. Что делать? Изменять год через timedelta.

### datetime.timedelta - разница времен

Если объект datetime - время отправления и прибытия поезда (с датой!), то timedelta - время в пути.

```python
import datetime

print('microseconds:', datetime.timedelta(microseconds=1))
print('milliseconds:', datetime.timedelta(milliseconds=1))
print('seconds     :', datetime.timedelta(seconds=1))
print('minutes     :', datetime.timedelta(minutes=1))
print('hours       :', datetime.timedelta(hours=1))
print('days        :', datetime.timedelta(days=1))
print('weeks       :', datetime.timedelta(weeks=1))
```
получим:
```python
microseconds: 0:00:00.000001
milliseconds: 0:00:00.001000
seconds     : 0:00:01
minutes     : 0:01:00
hours       : 1:00:00
days        : 1 day, 0:00:00
weeks       : 7 days, 0:00:00
```

**total_seconds()** - длительность в секундах (большое число)

```python
import datetime

for delta in [datetime.timedelta(microseconds=1),
              datetime.timedelta(milliseconds=1),
              datetime.timedelta(seconds=1),
              datetime.timedelta(minutes=1),
              datetime.timedelta(hours=1),
              datetime.timedelta(days=1),
              datetime.timedelta(weeks=1),
              ]:
    print('{:15} = {:8} seconds'.format(
        str(delta), delta.total_seconds())
    )
```
получим
```python
0:00:00.000001  =    1e-06 seconds
0:00:00.001000  =    0.001 seconds
0:00:01         =      1.0 seconds
0:01:00         =     60.0 seconds
1:00:00         =   3600.0 seconds
1 day, 0:00:00  =  86400.0 seconds
7 days, 0:00:00 = 604800.0 seconds
```

### Арифметические операции над временем

```python
import datetime

today = datetime.date.today()
print('Today    :', today)

one_day = datetime.timedelta(days=1)
print('One day  :', one_day)

yesterday = today - one_day
print('Yesterday:', yesterday)

tomorrow = today + one_day
print('Tomorrow :', tomorrow)

print()
print('tomorrow - yesterday:', tomorrow - yesterday)
print('yesterday - tomorrow:', yesterday - tomorrow)
```
получим:
```python
Today    : 2018-04-19
One day  : 1 day, 0:00:00
Yesterday: 2018-04-18
Tomorrow : 2018-04-20

tomorrow - yesterday: 2 days, 0:00:00
yesterday - tomorrow: -2 days, 0:00:00
```

Можно увеличить timedelta с помощью арифметических операций:
```python
import datetime

one_day = datetime.timedelta(days=1)
print('1 day    :', one_day)
print('5 days   :', one_day * 5)
print('1.5 days :', one_day * 1.5)
print('1/4 day  :', one_day / 4)

# assume an hour for lunch
work_day = datetime.timedelta(hours=7)
meeting_length = datetime.timedelta(hours=1)
print('meetings per day :', work_day / meeting_length)
```
получим
```python
1 day    : 1 day, 0:00:00
5 days   : 5 days, 0:00:00
1.5 days : 1 day, 12:00:00
1/4 day  : 6:00:00
meetings per day : 7.0
```

### Сравнение времен

```python
import datetime
import time

print('Times:')
t1 = datetime.time(12, 55, 0)
print('  t1:', t1)
t2 = datetime.time(13, 5, 0)
print('  t2:', t2)
print('  t1 < t2:', t1 < t2)

print()
print('Dates:')
d1 = datetime.date.today()
print('  d1:', d1)
d2 = datetime.date.today() + datetime.timedelta(days=1)
print('  d2:', d2)
print('  d1 > d2:', d1 > d2)
```
получаем
```python
Times:
  t1: 12:55:00
  t2: 13:05:00
  t1 < t2: True

Dates:
  d1: 2018-04-19
  d2: 2018-04-20
  d1 > d2: False
```

### Комбинируем дату и время

Класс **datetime** - и дата, и время вместе.

```python
import datetime

print('Now    :', datetime.datetime.now())
print('Today  :', datetime.datetime.today())
print('UTC Now:', datetime.datetime.utcnow())
print()

FIELDS = [
    'year', 'month', 'day',
    'hour', 'minute', 'second',
    'microsecond',
]

d = datetime.datetime.now()
for attr in FIELDS:
    print('{:15}: {}'.format(attr, getattr(d, attr)))
```
получим
```python
Now    : 2018-04-19 11:26:41.266448
Today  : 2018-04-19 11:26:41.266670
UTC Now: 2018-04-19 08:26:41.266753

year           : 2018
month          : 4
day            : 19
hour           : 11
minute         : 26
second         : 41
microsecond    : 267463
```

Есть так же **fromordinal()** и **fromtimestamp()**

```python
import datetime

t = datetime.time(1, 2, 3)
print('t :', t)

d = datetime.date.today()
print('d :', d)

dt = datetime.datetime.combine(d, t)
print('dt:', dt)
```
получим:
```python
t : 01:02:03
d : 2018-04-19
dt: 2018-04-19 01:02:03
```

### Разбор строки и преобразование в строку

По умолчанию объект datetime представлен в ISO-8601 формате (YYYY-MM-DDTHH:MM:SS.mmmmmm).

**strftime()** - представим в виде строки, используя другие форматы.
**strptime()** - из строки (parse) в объект datetime

```python
import datetime

format = "%a %b %d %H:%M:%S %Y"

today = datetime.datetime.today()
print('ISO     :', today)

s = today.strftime(format)
print('strftime:', s)

d = datetime.datetime.strptime(s, format)
print('strptime:', d.strftime(format))
```
получим
```python
ISO     : 2018-04-19 11:31:58.397024
strftime: Thu Apr 19 11:31:58 2018
strptime: Thu Apr 19 11:31:58 2018
```

**format** поддерживает форматирование datetime

```python
import datetime

today = datetime.datetime.today()
print('ISO     :', today)
print('format(): {:%a %b %d %H:%M:%S %Y}'.format(today))
```
получим
```python
ISO     : 2018-03-18 16:20:35.006116
format(): Sun Mar 18 16:20:35 2018
```

#### Что получим по каким форматам

если возьмем 5:00 PM January 13, 2016 in the US/Eastern time zone:

| Symbol | Meaning | Example |
|-|---|--|
| %a | Abbreviated weekday name | 'Wed' |
| %A | Full weekday name | 'Wednesday' |
| %w | Weekday number – 0 (Sunday) through 6 (Saturday) | '3' |
| %d | Day of the month (zero padded) | '13' |
| %b | Abbreviated month name | 'Jan' |
| %B | Full month name | 'January' |
| %m | Month of the year | '01' |
| %y | Year without century | '16' |
| %Y | Year with century | '2016' |
| %H | Hour from 24-hour clock | '17' |
| %I | Hour from 12-hour clock | '05' |
| %p | AM/PM | 'PM' |
| %M | Minutes | '00' |
| %S | Seconds | '00' |
| %f | Microseconds | '000000' |
| %z | UTC offset for time zone-aware objects | '-0500' |
| %Z | Time Zone name | 'EST' |
| %j | Day of the year | '013' |
| %W | Week of the year | '02' |
| %c | Date and time representation for the current locale | 'Wed Jan 13 17:00:00 2016' |
| %x | Date representation for the current locale | '01/13/16' |
| %X | Time representation for the current locale | '17:00:00' |
| %% | A literal % character | '%' |

### Таймзона

Within datetime, time zones are represented by subclasses of tzinfo. Since tzinfo is an abstract base class, applications need to define a subclass and provide appropriate implementations for a few methods to make it useful.

datetime does include a somewhat naive implementation in the class timezone that uses a fixed offset from UTC, and does not support different offset values on different days of the year, such as where daylight savings time applies, or where the offset from UTC has changed over time.

```python
import datetime

min6 = datetime.timezone(datetime.timedelta(hours=-6))
plus6 = datetime.timezone(datetime.timedelta(hours=6))
d = datetime.datetime.now(min6)

print(min6, ':', d)
print(datetime.timezone.utc, ':',
      d.astimezone(datetime.timezone.utc))
print(plus6, ':', d.astimezone(plus6))

# convert to the current system timezone
d_system = d.astimezone()
print(d_system.tzinfo, '      :', d_system)
```
получим
```python
UTC-06:00 : 2018-04-19 02:40:28.133666-06:00
UTC : 2018-04-19 08:40:28.133666+00:00
UTC+06:00 : 2018-04-19 14:40:28.133666+06:00
MSK       : 2018-04-19 11:40:28.133666+03:00
```

**The third party module pytz is a better implementation for time zones. It supports named time zones, and the offset database is kept up to date as changes are made by political bodies around the world.**
