class Juros(object):

    def __init__(self, cod_juros,data_juros,valor):
        self.TituloCodigoJuros = str(cod_juros)
        data = data_juros.strftime('%d/%m/%Y')
        self.TituloDataJuros = data
        self.TituloValorJuros = str(valor)
