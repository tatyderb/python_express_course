# Работа со временем и датами

Для работы со временем и датами нужно импортировать пакет [datetime](https://docs.python.org/3/library/datetime.html). Он содержит модули:

* **time** - функции, соответствующие функциям языка С. clock time и the processor run time, перевод времени в строку по формату и разбор строки по формату.

* **datetime** - более высокоуровневый интерфейс работы с датами и временем и их комбинированными значениями (дата + время). Поддерживаются арифметические операции, сравнение и конфигурация таймзоны.

* **calendar** - формативанное представление недель, месяцев и лет. Тут вычисляем день недели по дате и тп.

## time - clock time

Так как функции этого модуля обращаются к аналогичным функциям языка С, то они платформено-зависимые.

* **time()** - на основе системного вызова time() - "wall clock"
* **monotonic()** - used to measure elapsed time in a long-running process because it is guaranteed never to move backwards, even if the system time is changed.
* **perf_counter()** - самое высокое разрешение для коротких измерений времени (обычно измерение производительности).
* **clock()** - cpu time.
* **process_time()** -  returns the combined processor time and system time

### Сравним часы

|process_time | adjustable | implementation | monotonic | resolution | current |
|--|--|--|--|--|--|
|process_time | adjustable | implementation | monotonic | resolution | current |


## Литература

* [документация по питону](https://docs.python.org/3/library/datetime.html#)
* [TutorialsPoint: Python - Date & Time](https://www.tutorialspoint.com/python/python_date_time.htm)  
* [Guru99](https://www.guru99.com/date-time-and-datetime-classes-in-python.html)
* Python Cookbook, chapter chapters 3.12-3.16
* [PyMOTW](https://pymotw.com/3/dates.html)