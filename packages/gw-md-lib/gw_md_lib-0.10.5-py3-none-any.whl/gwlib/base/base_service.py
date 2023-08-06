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


    def before_save(self):
        pass

    def after_save(self):
        pass

    def save(self, data=None):
        self.data = data
        self.__save()

    def delete(self, data=None):
        self.data = data

    def get(self, **filters):
        self.dao.get(**filters)
        
    def filter(self, **filters):
        self.dao.filter(**filters)


class UserService(BaseService):
    required_fields = []
    def __init__(self, session=None, model=None):
        super(UserService).__init__(session=session, model=model)
    required_fields = [""]






