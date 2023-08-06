from .base import Base

class NumeroDoc(Base):

    def __init__(self, environment):

        super(NumeroDoc, self).__init__()

        self.environment = environment

    def execute(self):

        uri = '%snumerodoc' % (self.environment.apinumerodoc)

        return self.request_numerodoc("POST", uri)