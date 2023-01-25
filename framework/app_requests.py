from quopri import decodestring


class AppRequests:
    """Получение параметров запроса GET или POST в словарь params"""

    def __init__(self, method, environ):

        if method == 'POST':
            data = self.get_wsgi_input_data(environ)
            params = self.parse_wsgi_input_data(data)
            self.params = self.decode_value(params)

        if method == 'GET':
            data = environ['QUERY_STRING']
            self.params = self.parse_input_data(data)

    @staticmethod
    def parse_input_data(data: str) -> dict:
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        print(content_length)
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        if data:
            data_str = data.decode(encoding='utf-8')
            return self.parse_input_data(data_str)
        return {}

    @staticmethod
    def decode_value(data) -> dict:
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
