from jinja2 import Environment, FileSystemLoader


def render(template_name, folder='templates', **context):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**context)
