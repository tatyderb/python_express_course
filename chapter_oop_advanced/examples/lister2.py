''' Выводит информацию об атрибутах экземпляра класса '''

class ListInstance(object):
    def __str__(self):
        return '<Instance of {}, id = {}>:\n{}'.format(
                    self.__class__.__name__,    # имя класса реального объекта
                    id(self),
                    self.__attrnames()          # список пар атрибут - значение
                )
                
    def __attrnames(self):
        """Список пар атрибут - значение объекта в виде строки с отступом"""
        return '\n'.join(('\tname {} = {}'.format(
                            attr, 
                            '<>' if attr.startswith('__') and attr.endswith('__') else getattr(self, attr)
                            ) 
                            for attr in sorted(dir(self)) 
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

    x = ListInstance()
    print(x)
    
    b = B(1, 2)
    print(b)
