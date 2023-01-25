import os
from wsgiref.simple_server import make_server
from wsgi_static_middleware import StaticMiddleware

from components.front_controllers import fronts
from framework.app import App, DebugApp, FakeApp
from views import routes


class GetInputApp:
    """Обработчик ввода пользователя перед запуском приложения.
    'f' - запускает FakeApp, 'd' - DebugApp.
    Если нужен стандартный режим App, то можно ничего не вводить.
    """

    def __init__(self, inp):
        match inp:
            case "f":
                self.inp = FakeApp
            case "d":
                self.inp = DebugApp
            case _:
                self.inp = App

    def get_app(self):
        return self.inp


BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'static')]
USER_INPUT = input('Введите "F" или "D", если требуется нестандартный режим работы приложения: ')

application = GetInputApp(USER_INPUT).get_app()(routes, fronts)
app_static = StaticMiddleware(application, static_root='static', static_dirs=STATIC_DIRS)

with make_server('', 8080, app_static) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
