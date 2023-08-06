
from .base import Base

class CriarBoleto(Base):

    def __init__(self, authorize, environment):

        super(CriarBoleto, self).__init__(authorize)

        self.environment = environment

    def execute(self, criar_boleto):

        uri = '%s1/boletos/lote' % self.environment.api

        response = self.send_request("POST", uri, criar_boleto)

        criar_boleto.update_return(response)

        return response
