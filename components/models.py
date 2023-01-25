from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect

from components.mappers import BaseMapper
from components.observer import Subject
from components.unit_of_work import DomainObject


class User:
    """Абстрактный пользователь"""

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.get('id')

        if 'name' in kwargs:
            self.name = kwargs.get('name')


class Teacher(User, DomainObject):
    """Преподаватель от абстрактного пользователя"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Student(User, DomainObject):
    """Студент от абстрактного пользователя"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'courses' in kwargs:
            self.courses = kwargs.get('courses')


class UserFactory:
    """Фабрика пользователей - студента, преподавателя
    (фабричный метод)
    """

    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Category(DomainObject):
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


class Course(CoursePrototype, Subject, DomainObject):
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
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category):
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


class StudentMapper(BaseMapper):
    tablename = 'students'
    model = Student


class CategoryMapper(BaseMapper):
    tablename = 'categories'
    model = Category


class CourseMapper(BaseMapper):
    tablename = 'courses'
    model = Course


connection = connect('project.sqlite')


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Course):
            return CourseMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
