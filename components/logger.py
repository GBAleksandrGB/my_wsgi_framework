from components.writers import FileWriter, ConsoleWriter


class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]

        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer_1=FileWriter(), writer_2=ConsoleWriter()):
        self.name = name
        self.writer_1 = writer_1
        self.writer_2 = writer_2

    def log(self, text):
        self.writer_1.write(text)
        self.writer_2.write(text)
