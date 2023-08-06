from .request.criar_boleto import CriarBoleto
from .request.busca_boleto import BuscaBoleto


class PlugBoleto(object):

    def __init__(self, authorize, environment):

        self.environment = environment
        self.authorize = authorize

    def criar_boleto(self, criar_boleto):

        request = CriarBoleto(self.authorize, self.environment)

        return request.execute(criar_boleto)

    def consulta_boleto(self, id_integracao):
        request = BuscaBoleto(self.merchant, self.environment)

        return request.execute(id_integracao)

    def link_boleto(self, empresa, id_integracao):
        uri = 'https://plugboleto.com.br/impresao/%s1/%s' % (empresa, id_integracao)

        return uri