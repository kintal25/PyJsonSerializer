import datetime
import JsonSerializer


class Employee(object):
    def __init__(self, name: str = None, age: int = None):
        self.name = name
        self.age = age
        return


class Company(object):
    def __init__(self, name: str = "", creationDate: datetime.datetime = None, isActive = False, employees: [Employee] = None,):
        self.name = name
        self.employees = [] if employees is None else employees
        self.creationDate = datetime.datetime.now() if creationDate is None else creationDate
        self.isActive = isActive


def Check():
    obj = [
        Company("Big Company", datetime.datetime(2019, 5, 10), True, [
            Employee("Ivan Ivanov", 52),
            Employee("Stepan Nicolaevich"),
            Employee("Kendrick Lamar", 33),
            Employee("Big Bossov", 26)
        ]),
        Company("Small Company", datetime.datetime(2019, 5, 10), True, [
            Employee("Mr Black", 28),
            Employee("Mrs White", 82)
        ])
    ]

    objJson = JsonSerializer.ToJson(obj)
    objNew = JsonSerializer.FromJson(objJson)
