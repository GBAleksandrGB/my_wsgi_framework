from copy import deepcopy
from quopri import decodestring

from observer import Subject


class User:
    """Абстрактный пользователь"""

    def __init__(self, name):
        self.name = name


class Teacher(User):
    """Преподаватель от абстрактного пользователя"""

    def __init__(self, name):
        super().__init__(name)


class Student(User):
    """Студент от абстрактного пользователя"""

    def __init__(self, name):
        super().__init__(name)
        self.courses = []


class UserFactory:
    """Фабрика пользователей - студента, преподавателя
    (фабричный метод)
    """

    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Category:
    """Абстрактная модель категории"""

    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)

        if self.category:
            result += self.category.course_count()

        return result


class CoursePrototype:
    """Прототип курсов обучения"""

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    """Абстрактный курс от прототипа"""

    def __init__(self, name, category: Category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    """Интерактивный курс от абстрактной модели курса"""

    pass


class RecordCourse(Course):
    """Запись курса от абстрактной модели курса"""

    pass


class CourseFactory:
    """Фабрика курсов - интерактивного, в записи
    (фабричный метод)
    """

    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Engine:
    """Механизм создания пользователя, категории, курса"""

    def __init__(self):
        self.teachers = []
        self.students = []
        self.categories = []
        self.courses = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item

    def get_student(self, name):
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')
