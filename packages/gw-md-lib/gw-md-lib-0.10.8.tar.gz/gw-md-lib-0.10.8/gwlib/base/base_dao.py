from sqlalchemy.orm import Query
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from gwlib.base.errors import FieldNotInModel


class BaseDAO:
    include_logical_deleted = False

    def __init__(self, session, model):
        self.model = model
        self.session = session

    def change_model(self, model):
        self.model = model

    @property
    def queryset(self):
        """

        :rtype: Query
        """
        if not self.include_logical_deleted:
            return self.model.query.filter_by(deleted=False)
        else:
            return self.model.query

    def save(self, **data):
        model = self.model(**data)
        self.session.add(model)
        self.session.commit()

    def __get(self, **filters):
        try:
            query = self.queryset.filter_by(**filters)
            obj = query.one_or_none()
            if obj is None:
                return NoResultFound

        except MultipleResultsFound:
            raise MultipleResultsFound
        return obj

    def update(self, data, **filters):
        obj = self.__get(**filters)
        for field, value in data.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
            else:
                raise FieldNotInModel

        self.session.commit(self.model)

    def delete(self, **filters):
        obj = self.__get(**filters)
        if hasattr(obj, "delete"):
            obj.delete = True
        self.session.commit(self.model)

    def filter(self, **filters):
        query = self.queryset.filter_by(**filters)
        return query.all()

    def get(self, **filters):
        return self.__get(**filters)


