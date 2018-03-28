# Задачи

## Срезы списка

На одной строке через пробел даны целые числа. Напечатайте (1 ответ в 1 строку следующие мини-задачи).

Пример печати результата для введеного списка a = \[10, 7, -6, 11, 13, 5, 1, 8, 13\]

| Задача | Результат |
|---|---|
| Напечатать список | \[10, 7, -6, 11, 13, 5, 1, 8, 13\] |
| первое число списка | 10 |
| последнее число списка | 13 |
| первые пять чисел списка | \[10, 7, -6, 11, 13\]|
| весь список, кроме последних двух чисел |  \[10, 7, -6, 11, 13, 5, 1\] |
| все числа с четными номерами (считая, что индексация начинается с 0) |  \[10, -6, 13, 1, 13\] |
| все числа с нечетными номерами |  \[7, 11, 5, 8\] |
| все числа в обратном порядке | \[13, 8, 1, 5, 13, 11, -6, 7, 10\]|
| все числа строки через один в обратном порядке, начиная с последнего | \[13, 1, 13,  -6, 10\] |
| длину списка | 9 |
| Заменить 2 первых числа на 1 22 333 | \[1, 22, 333, -6, 11, 13, 5, 1, 8, 13\]|

## Расширение файла

Даны имена файлов (путь) по 1 файлу на строку. Напечатать все расширения файлов (после последней точки, без пробельных символов). Можно не вводить имена файлов, а создать список строк и отлаживать код на нем.
```python
Input:
/cygdrive/c/Users/taty/GitBook/Library/tatyderb/python-express-course/chapter_seq/README.md
summary.html
../keys.png
C:\tmp\example.py
# Output:
md
html
png
py
```

## Убрать повторы

Даны числа на одной строке через пробел. Напечатайте каждое число только 1 раз. Порядок печати - произвольный.
```python
# Input:
5 3 4 -1 -2 5 7 3
# Output: (порядок печати может отличаться)
-1 -2 3 4 5 7
```

## Только один раз

Даны числа на одной строке через пробел. Напечатайте каждое число только 1 раз. Порядок печати - в том, в котором числа первый раз встретились в последовательности.
```python
# Input:
5 3 4 -1 -2 5 7 3
# Output: (строго такой порядок печати)
5 3 4 -1 -2 7
```

## Уникальные числа

Даны числа на одной строке через пробел. Только те числа, которые были уникальными в исходной последовательности. Порядок печати любой.

```python
# Input:
5 3 4 -1 -2 5 7 3
# Output:
4 -1 -2 7
```
## Страны и города

Дан список городов по странам в формате страна и города через пробел.

Выведите список город страны где есть города с таким именем. Список отсортировать.

```python
Input:
Russia Moscow Samara Peterburg Omsk
Ukraina Kiev Kharkov Nezhin
USA NewYork Peterburg Dallas Austin Houston
Output:
Austin USA
Dallas USA
Houston USA
Kiev Ukraina
Kharkov Ukraina
Moscow Russia
Nezhin Ukraina
NewYork USA
Omsk Russia
Peterburg Russia USA
Samara Russia
```

## Даты

На каждой строке написана дата в формате dd/mm/yyyy. Выведите даты в порядке возрастания в формате yyyy/mm/dd.

```
Input:
01/12/1910
31/05/0861
22/06/2014

Output:
0861/05/31
1910/12/01
2014/06/22
```

## Рост, вес

Даны рос и вес каждого человека. Отсортировать по уменьшению роста. При одинаковом росте сначала печатать больший вес.
```python
Input:
156 66.2
178 66.8
178 56.4

Output:
178 66.8
178 56.4
156 66.2
```

## Скобки-1

Дана скобочная последовательность из скобок ( и ) на одной строке. Напечатайте YES, если скобочная последовательность правильная. Иначе напечатайте NO.

Правильная скобочная последовательность:
* ()
* (()())
* (())
Неправильная скобочная последовательность:
* (()
* ())
* )(

## Скобки-2
Дана скобочная последовательность из скобок разных типов (){}\[\]<> на одной строке. Напечатайте YES, если скобочная последовательность правильная. Иначе напечатайте NO.

Правильная скобочная последовательность:
* ()
* (()<>)
* ({})

Неправильная скобочная последовательность:
* (()
* ())
* )(
* (<)>