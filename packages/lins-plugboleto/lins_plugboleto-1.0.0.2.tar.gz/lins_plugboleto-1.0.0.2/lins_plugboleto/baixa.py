class Baixa(object):

    def __init__(self, prazo_baixa):
        if (prazo_baixa > 0):
            self.TituloCodBaixaDevolucao = '1'
            self.TituloPrazoBaixa = str(prazo_baixa)
