class Juros(object):

    def __init__(self, juros):
        self.TituloCodigoJuros = str(juros['TituloCodigoJuros'])
        data = juros['TituloDataJuros'].strftime('%d/%m/%Y')
        self.TituloDataJuros = data
        self.TituloValorJuros = str(juros['TituloValorJuros'])
