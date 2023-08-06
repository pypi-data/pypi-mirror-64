class Cedente(object):

    def __init__(self, cedente):
        self.CedenteContaCodigoBanco = str(cedente['codigo_banco'])
        self.CedenteContaNumero = str(cedente['conta_numero'])
        self.CedenteContaNumeroDV = str(cedente['dv'])
        self.CedenteConvenioNumero = str(cedente['convenio'])
