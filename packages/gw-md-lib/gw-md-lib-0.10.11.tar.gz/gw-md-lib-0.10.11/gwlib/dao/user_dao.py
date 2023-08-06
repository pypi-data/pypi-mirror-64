from gwlib.base.base_dao import BaseDAO


class UserDAO(BaseDAO):

    def save(self, **data):
        password = data.pop("password")
        model = self.model(**data)
        model.set_password(password)
        self.session.add(model)
        self.session.commit()
