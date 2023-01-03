class ConsoleWriter:
    """Паттерг Стратегия.
    Пишет в консоль некий текст.
    Используется в модуле logger.py
    """

    def write(self, text):
        print(text)


class FileWriter:
    """Паттерг Стратегия.
    Пишет в файл некий текст.
    Используется в модуле logger.py
    """

    def write(self, text):
        with open('log.txt', 'a', encoding='UTF-8') as f:
            f.write(f'{text}\n')
