import hashlib

from gwlib.base.base_dao import BaseDAO
from gwlib.base.errors import FieldRequired


class BaseService:
    def __init__(self, session=None, model=None):
        self.data = {}
        self.dao = BaseDAO(session=session, model=model)

    def validate(self):
        pass

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


class UserService(BaseService):
    required_fields = ["username"]

    def __init__(self, session=None, model=None):
        super(UserService).__init__(session=session, model=model)

    def validate(self):
        for key in self.required_fields:
            if key not in self.data:
                raise FieldRequired

cdb_prod = Server("https://admin:linkaform2018server.@couchdb.linkaform.com")
username = "username"
user_id = 000
cdb_prod.remove_user(username)
account = "account_0000"
cdb_prod.add_user(username, password, [account])




