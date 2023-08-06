from .request.numero_doc import NumeroDoc


class NossoNumero(object):

    def __init__(self, environment):
        self.environment = environment

    def gerar_nossonumero(self):
        request = NumeroDoc(self.environment)

        return request.execute()