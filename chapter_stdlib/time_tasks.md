# Задачи

## 0. Создать файл (директорию) со временем запуска теста

Запускается программа. Для хранения данных конкретного запуска создайте файл с датой и временем этого запуска в формате yyyymmdd_hhmm.txt

## 1. Сколько времени длился тест

Дан файл логов теста (bet.log). Первая колонка - timestamp. Напечатать сколько времени длился тест в днях (если длился более суток), часах, минутах и секундах. 

### 1.1 Длительность времени теста записать в часах в дробном формате

Например, если тест длился 1 день 3 часа 15 минут, вывести `27.25 h`

# Прочие задачи - разобрать и записать формально.


1. Написать функции преобразования из строки (заданного формата + информация о том что строка в UTC, в локальном или в заданном поясе, это могут быть три отдельные задачи) в unix timestamp.
2. Потом из UNIX timestamp в строку заданного формата (и в заданном часовом поясе).
3. Округлить до ближайшей 10-минутки (15-минутки, часа или ещё чего), обычно делаю через преобразование к timestamp, округление и обратное преобразование, может придумаешь что-то лучше.
4. Вывод дат когда будут следующие семинары (взять текущую дату и в цикле прибавлять дельту в 7 дней, опционально пропускать праздники)
5. Что-то про вывод дней недели.
6. Вывод дат для годичного отчёта с детализацией по месяцам: взять текущую дату (она может передаваться как параметр), truncate до начала года (т.е. до первого января текущего года, через replace или ещё как), потом в цикле выводить записи вида "первый день - последний день" до текущего дня (не из параметра, а именно текущего, т.е. идём до конца года, не залезая в будущее) или до 31го декабря (что раньше), примеры:
а)
2018-01-01 - 2018-01-31
2018-02-01 - 2018-02-28
2018-03-01 - 2018-03-23
б)
2016-01-01 - 2016-01-31
2016-02-01 - 2016-02-29
...
2016-12-01 - 2016-12-31
Подсказка: в цикле прибавлять дельту в одни сутки, переходить на новую строку когда месяц текущих просматриваемых суток не равен месяцу предыдущих. Есть другой вариант: идти по первым числам месяцев и вычитать один день.
7. Вывод дат с детализацией по дням, аналогично предыдущей задаче (многоточия потому что мне влом копировать, в выводе их не должно быть):
2018-01: 1 2 3 ... 31
2018-02: 1 2 ... 28
2018-03: 1 2 ... 23