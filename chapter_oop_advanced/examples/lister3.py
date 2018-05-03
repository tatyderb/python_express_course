''' Выводит информацию об атрибутах экземпляра класса '''

class ListInstance(object):
    def __str__(self):
        s = '<Instance of {}, id = {}>:\n{}'.format(
                self.__class__.__name__,    # имя класса реального объекта
                id(self),
                self.__attrnames(self)          # список пар атрибут - значение
            ) + '\n'
        for cls in self.__class__.mro():
            s += '<Instance of {}, id = {}>:\n{}'.format(
                    cls.__name__,    # имя класса реального объекта
                    id(cls),
                    self.__attrnames(cls)          # список пар атрибут - значение
                ) + '\n'
        return s
                
    def __attrnames(self, cls):
        """Список пар атрибут - значение объекта в виде строки с отступом"""
        return '\n'.join(('\tname {} = {}'.format(
                            attr, 
                            '<>' if attr.startswith('__') and attr.endswith('__') else getattr(cls, attr)
                            ) 
                            for attr in sorted(cls.__dict__) 
                        ))
                            
if __name__ == '__main__':
    class A(object):
        def __init__(self, x):
            self.x = x
        
        def foo(self):
            pass
            
    class B(A, ListInstance):
        def __init__(self, x, y):
            super().__init__(x)
            self.y = y
            
        def bzz(self):
            pass

    # x = ListInstance()
    # print(x)
    
    b = B(1, 2)
    print(b)
