## Сравнение

* В отличие от \_\_add\_\_ и \_\_radd\_\_ методы сравнения не имеют правосторонних версий. Если операцию поддерживает только один операнд, используется зеркальный метод сравнения (методы \_\_lt\_\_ и \_\_gt\_\_ зеркальны друг другу)

* Не факт, что истинность операции == означает ложность !=. В этом случае реализуйте оба метода: \_\_eq\_\_ и \_\_ne\_\_.

* Метод \_\_cmp\_\_ и встроенный метод cmp() устарели. Не используйте их.
