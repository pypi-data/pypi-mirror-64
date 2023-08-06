from .base import Base

class NumeroDoc(Base):

    def __init__(self, authorizedoc, environment):

        super(NumeroDoc, self).__init__(authorizedoc)

        self.environment = environment

    def execute(self):

        uri = '%snumerodoc' % (self.environment.api_doc)

        return self.send_request("POST", uri)