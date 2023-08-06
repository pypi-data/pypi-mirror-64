import hashlib

from gwlib.base.base_dao import BaseDAO
from gwlib.base.errors import FieldRequired


class BaseService:
    required_fields = []

    def __init__(self, session=None, model=None):
        self.data = {}
        self.dao = BaseDAO(session=session, model=model)

    def validate(self):
        for key in self.required_fields:
            if key not in self.data:
                raise FieldRequired

    def __save(self):
        self.validate()
        self.before_save()
        self.dao.save(**self.data)
        self.after_save()

    def __update(self, **filters):
        self.dao.update(**self.data, **filters)

    def before_save(self):
        pass

    def after_save(self):
        pass

    def save(self, data=None):
        self.data = data
        self.__save()

    def update(self, data=None, **filters):
        self.data = data
        self.__update(**filters)

    def delete(self, data=None):
        self.data = data

    def get(self, **filters):
        self.dao.get(**filters)
        
    def filter(self, **filters):
        self.dao.filter(**filters)






