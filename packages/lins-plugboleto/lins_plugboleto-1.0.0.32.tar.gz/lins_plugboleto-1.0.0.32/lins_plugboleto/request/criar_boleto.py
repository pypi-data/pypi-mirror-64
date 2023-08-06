
from .base import Base

class CriarBoleto(Base):

    def __init__(self, authorize, environment):

        super(CriarBoleto, self).__init__(authorize)

        self.environment = environment

    def execute(self, criar_boleto):

        uri = '%sboletos/lote' % self.environment.api

        response = self.send_request("POST", uri, criar_boleto)

        sucesso = response['_dados']['_sucesso']
        if sucesso:
            criar_boleto.update_return(response)
        else:
            return response['_dados']['_falha'][0]

        return response
