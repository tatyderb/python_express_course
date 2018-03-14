class Person(object):
    def __init__(self, name, job=None, pay=0, part_time=1):
        self.name = name
        self.job = job
        self.base_pay = pay
        self.part_time = part_time
        
    def __str__(self):
        return '[Person: {}, {}]'.format(self.name, self.pay())
        
    def __repr__(self):
        return 'Person:[name={d.name}, base_pay={d.base_pay}, part_time={d.part_time}]'.format(d=self)
        
    def last_name(self):
        return self.name.split()[2]
        
    def pay(self):
        return int(self.base_pay * self.part_time)
        
class Teacher(object):      # Teacher НЕ наследует от Person
    HOUR_RATE = 200
    def __init__(self, name, pay=0, part_time=1, hours=0):
        self.person = Person(name, 'teacher', pay, part_time)   # вложенный объект
        self.hours = hours
        
    def pay(self):                  
        # перехватывает обращение и делегирует его к другим методам
        return self.person.pay() + self.hours * self.HOUR_RATE
        
    def __getattr__(self, attr):
        # делегирует обращения ко всем остальным атрибутам
        return getattr(self.person, attr)
        
    def __str__(self):
        # тоже требуется перегрузить
        return str(self.person)
        
if __name__ == '__main__':
    # Тестируем класс, только если запускаем файл
    bob = Person('Boris Alexeevich Ivanov')
    mike = Person('Mikhail Vladimirovich Kuznetsov', job='student', pay=5000, part_time=0.5)

    print(bob)                      # [Person: Boris Alexeevich Ivanov, 0]
    print(mike)                     # [Person: Mikhail Vladimirovich Kuznetsov, 2500]
    print(repr(mike))
    
    # добавили код - добавим тесты
    print(bob.last_name())          # Ivanov
    print(mike.last_name())         # Kuznetsov

    tanya = Teacher(name='Tatyana Vladimirovna Ovsyannikova', pay=10000, hours=6*4)
    print(tanya.pay())              # вызов измененной версии pay класса Teacher
    print(tanya.last_name())        # вызов унаследованного метода
    print(tanya)                    # вызов унаследованного метода
    
    for p in (bob, mike, tanya):
        print(p.pay())
        print(p)
