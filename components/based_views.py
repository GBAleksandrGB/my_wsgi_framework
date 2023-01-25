from components.decorators import Timer
from components.logger import Logger
from framework.templator import render

logger = Logger('test')


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
