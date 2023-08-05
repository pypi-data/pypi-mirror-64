

class BaseDAO:
    def __init__(self, session, model, data):
        self.model = model
        self.session = session

    def save(self, **kwargs):
        self.model(data)
        self.session.add(self.model)
        self.session.commit()

    def update(self):
        self.model(**self.data)
        self.session.add(self.model)
        self.session.commit()

    def delete(self):
        self.model(**self.data)
        self.session.add(self.model)
        self.session.commit()

    def get(self):
        self.model(**self.data)
        self.session.add(self.model)
        self.session.commit()