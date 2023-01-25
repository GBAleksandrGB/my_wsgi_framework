import threading


class UnitOfWork:
    """
    Паттерн UNIT OF WORK.
    Объединяет в одном потоке операции получения из БД,
    изменения или сохранения в БД записей, представленных
    в виде объекта-маппера.
    """

    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj, schema):
        self.new_objects.append({'object': obj, 'schema': schema})

    def register_dirty(self, obj, schema):
        self.dirty_objects.append({'object': obj, 'schema': schema})

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):

        for obj in self.new_objects:
            self.MapperRegistry.get_mapper(obj['object']).insert(**obj['schema'])

        self.new_objects.clear()

    def update_dirty(self):

        for obj in self.dirty_objects:
            self.MapperRegistry.get_mapper(obj['object']).update(obj['object'], **obj['schema'])

        self.dirty_objects.clear()

    def delete_removed(self):

        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)

        self.removed_objects.clear()

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls) -> object:
        return cls.current.unit_of_work


class DomainObject:
    def mark_new(self, schema):
        UnitOfWork.get_current().register_new(self, schema)

    def mark_dirty(self, schema):
        UnitOfWork.get_current().register_dirty(self, schema)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)
