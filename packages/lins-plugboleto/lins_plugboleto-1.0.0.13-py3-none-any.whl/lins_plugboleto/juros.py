class Juros(object):

    def __init__(self, juros):
        self.TituloCodigoJuros = str(juros['cod_juros'])
        data = juros['data_juros'].strftime('%d/%m/%Y')
        self.TituloDataJuros = data
        self.TituloValorJuros = str(juros['valor'])
