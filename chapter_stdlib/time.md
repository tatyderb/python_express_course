# Работа со временем и датами

Для работы со временем и датами нужно импортировать пакет [datetime](https://docs.python.org/3/library/datetime.html).

* **[time](https://docs.python.org/3/library/time.html)** - функции, соответствующие функциям языка С. clock time и the processor run time, перевод времени в строку по формату и разбор строки по формату.

* **[datetime](https://docs.python.org/3/library/datetime.htm)** - более высокоуровневый интерфейс работы с датами и временем и их комбинированными значениями (дата + время). Поддерживаются арифметические операции, сравнение и конфигурация таймзоны.

* **calendar** - формативанное представление недель, месяцев и лет. Тут вычисляем день недели по дате и тп.

## time
Таблица преобразования типов:

|From \ To | timestamp | time tuple | string |
|-|-|-|-|
| timestamp |-| gmtime (UTC) <br/> localtime (local time)|-|
| time tuple | [calendar.timegm](https://docs.python.org/3/library/calendar.html#calendar.timegm) (UTC) <br/> mktime (local time)|-| strftime |
| string |-| strptime |-|

## Таблица форматов

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

## Литература

* [документация по питону](https://docs.python.org/3/library/datetime.html#)
* [TutorialsPoint: Python - Date & Time](https://www.tutorialspoint.com/python/python_date_time.htm)  
* [Guru99](https://www.guru99.com/date-time-and-datetime-classes-in-python.html)
* Python Cookbook, chapter chapters 3.12-3.16
* [PyMOTW](https://pymotw.com/3/dates.html)