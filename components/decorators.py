import time


class AppRoute:
    """Front-controller - декоратор для маршрутизации"""

    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Timer:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def time_measure(func):
            def timed(*args, **kwargs):
                start = time.monotonic()
                result = func(*args, **kwargs)
                end = time.monotonic()
                delta = end - start
                print(f'Время выполнения {self.name}: {delta:2.3f} ms')
                return result
            return timed
        return time_measure(cls)

