from datetime import date

from jinja2 import Environment, FileSystemLoader

from decorators import AppRoute, Timer
from logger import Logger
from models import Engine
from observer import SmsNotifier, EmailNotifier
from serializer import BaseSerializer

routes = {}
site = Engine()
logger = Logger('test')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


def render(template_name, folder='templates', **context):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**context)


class TemplateView:
    """Базовый класс-контроллер для рендеринга шаблона,
    шаблонный паттерн
    """

    template_name = 'template.html'

    def get_template(self):
        return self.template_name

    def get_context_data(self, request):
        return {}

    def render_template_with_context(self, request):
        template_name = self.get_template()
        context = self.get_context_data(request)
        return '200 OK', render(template_name, **context)

    @Timer('Call base TemplateView')
    def __call__(self, request):
        logger.log(f'Вызов шаблона {self.template_name}')
        return self.render_template_with_context(request)


class ListView(TemplateView):
    """Базовый класс-контроллер для отображения списка данных по запросу,
    шаблонный паттерн
    """

    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self, request):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self, request):
        queryset = self.get_queryset(request)
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    """Базовый класс-контроллер для создания данных,
    шаблонный паттерн
    """

    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['params']

    def create_obj(self, params):
        pass

    @Timer('Call base CreateView')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


class UpdateView(TemplateView):
    template_name = 'update.html'

    @staticmethod
    def get_request_data(request):
        return request['params']

    def update_obj(self, params):
        pass

    @Timer('Call base UpdateView')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.update_obj(data)
            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


@AppRoute(routes=routes, url='/')
class Index(TemplateView):
    """Page-controller - Главная страница"""

    template_name = 'index.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['cur_date'] = date.today().strftime('%d.%m.%Y')
        return context


@AppRoute(routes=routes, url='/about/')
class About(TemplateView):
    """Page-controller - Страница о нас"""

    template_name = 'about.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        return context


class PageNotFound404:
    """Контроллер - страница не найдена"""

    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/courses_list/')
class CoursesListView(ListView):
    """Page-controller - страница со списком курсов"""

    template_name = 'courses-list.html'

    def get_queryset(self, request):
        category = site.find_category_by_id(int(request['params']['id']))
        return category.courses

    def get_context_data(self, request):
        context = super().get_context_data(request)
        category = site.find_category_by_id(int(request['params']['id']))
        context['name'] = category.name
        context['id'] = category.id
        return context


@AppRoute(routes=routes, url='/create_course/')
class CourseCreateView(CreateView):
    """Page-controller - страница для создания курса"""

    template_name = 'create-course.html'
    category = None

    def get_context_data(self, request):
        context = super().get_context_data(request)
        try:
            self.category = site.find_category_by_id(int(request['params']['id']))
        except KeyError:
            pass
        finally:
            context['name'] = self.category.name
            context['id'] = self.category.id
            return context

    def create_obj(self, data: dict):
        name = site.decode_value(data['name'])
        new_course = site.create_course('record', name, self.category)
        new_course.observers.append(sms_notifier)
        site.courses.append(new_course)


@AppRoute(routes=routes, url='/update_course/')
class CourseUpdateView(UpdateView):
    """Page-controller - страница для изменения курса"""

    template_name = 'update-course.html'
    course_name = None

    def get_context_data(self, request):
        context = super().get_context_data(request)
        try:
            self.course_name = site.decode_value(request['params']['name'])
        except KeyError:
            pass
        finally:
            context['name'] = self.course_name
            return context

    def update_obj(self, data: dict):
        new_course_name = site.decode_value(data['course'])
        current_course = site.get_course(self.course_name)
        current_course.name = new_course_name


@AppRoute(routes=routes, url='/copy_course/')
class CopyCourse(ListView):
    """Page-controller - страница для копирования курса"""

    template_name = 'courses-list.html'

    def get_queryset(self, request):
        return site.courses

    def get_context_data(self, request):
        context = super().get_context_data(request)
        name = site.decode_value(request['params']['name'])
        old_course = site.get_course(name)
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)
        context['name'] = new_course.category.name
        return context


@AppRoute(routes=routes, url='/create_category/')
class CategoryCreateView(CreateView):
    """Page-controller - страница для создания категории"""

    template_name = 'create-category.html'
    category_id = None

    def get_context_data(self, request):
        context = super().get_context_data(request)
        try:
            self.category_id = int(request['params']['id'])
        except KeyError:
            context['id'] = self.category_id
        return context

    def create_obj(self, data: dict):
        name = site.decode_value(data['name'])
        category = None
        if self.category_id:
            category = site.find_category_by_id(int(self.category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)


@AppRoute(routes=routes, url='/category_list/')
class CategoryListView(ListView):
    """Page-controller - страница для отображения списка категорий"""

    template_name = 'category-list.html'

    def get_queryset(self, request):
        queryset = site.categories
        return queryset


@AppRoute(routes=routes, url='/student_list/')
class StudentListView(ListView):
    """Page-controller - страница для отображения списка студентов"""

    template_name = 'student-list.html'
    queryset = site.students


@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):
    """Page-controller - страница для создания студента"""

    template_name = 'create-student.html'

    def create_obj(self, data: dict):
        name = site.decode_value(data['name'])
        new_student = site.create_user('student', name)
        site.students.append(new_student)


@AppRoute(routes=routes, url='/add_student/')
class AddStudentByCourseView(CreateView):
    """Page-controller - страница для добавления студента на курс"""

    template_name = 'add-student.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        if 'course' and 'student' in data \
                and data['course'] != 'Выберите курс' \
                and data['student'] != 'Выберите студента':
            course_name = site.decode_value(data['course'])
            course = site.get_course(course_name)
            student_name = site.decode_value(data['student'])
            student = site.get_student(student_name)
            course.add_student(student)


@AppRoute(routes=routes, url='/api/<id>/')
class CourseApi:
    """Тестовый запуск сериализатора,
    (нужно заранее создать, как минимум, объект категории)
    """

    def __call__(self, request):
        id = request.get('url_vars').get('id')
        category = site.find_category_by_id(int(id))
        return '200 OK', BaseSerializer(category).save()
