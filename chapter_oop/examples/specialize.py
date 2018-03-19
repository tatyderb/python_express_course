class Super:
    def method(self):
        print('in Super.method')    # Поведение по умолчанию
    def delegate(self):
        self.action()               # Ожидаемый метод

class Inheritor(Super):             # Наследует методы, как они есть
    pass

class Replacer(Super):              # Полностью замещает method
    def method(self):
        print('in Replacer.method')

class Extender(Super):              # Расширяет поведение метода method
    def method(self):
        print('starting Extender.method')
        Super.method(self)
        print('ending Extender.method')

class Provider(Super):              # Определяет необходимый метод
    def action(self):
        print('in Provider.action')

if __name__ == '__main__':
    for myclass in (Inheritor, Replacer, Extender):
        print('\n' + myclass.__name__ + '...')
        myclass().method()
    print('\nProvider...')
    x = Provider()
    x.delegate()