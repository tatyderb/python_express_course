import json

class Person(object):
    def __init__(self):
        self.name = 'John'
        self.age = 25
        self.id = 1

person = Person()

#save to file
dt = {}
dt.update(vars(person))
print(dt, type(dt))
print(vars(person))
#with open("/home/test/person.txt", "w") as file:
#    json.dump(dt, file)