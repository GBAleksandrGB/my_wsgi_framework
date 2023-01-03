from pprint import pprint

from app_requests import AppRequests
from routing import Router
from views import PageNotFound404


class App:
    """Основное приложение"""

    def __init__(self, routes):
        self.routes = routes
        self.request = {}
        self.router = Router(self.request, self.routes)

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        method = environ['REQUEST_METHOD']
        self.request['method'] = method
        self.request['params'] = AppRequests(method, environ).params
        print(self.request)
        view = self.router.get_view(path, PageNotFound404)
        code, body = view(self.request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('UTF-8')]


class DebugApp(App):
    """Логирующий ответ с типом запроса и параметрами"""

    def __init__(self, routes):
        self.application = App(routes)
        super().__init__(routes)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        pprint(env)
        return self.application(env, start_response)


class FakeApp(App):
    """Фейковый ответ на все запросы пользователя"""

    def __init__(self, routes):
        self.application = App(routes)
        super().__init__(routes)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Hello from Fake']
