from .objectJSON import ObjectJSON


class Sacado(ObjectJSON):

    def __init__(self, sacado):
        self.SacadoCPFCNPJ = str(sacado['SacadoCPFCNPJ'])
        self.SacadoNome = str(sacado['SacadoNome'])
        self.SacadoEnderecoLogradouro = str(sacado['SacadoEnderecoLogradouro'])
        self.SacadoEnderecoNumero = str(sacado['SacadoEnderecoNumero'])
        self.SacadoEnderecoBairro = str(sacado['SacadoEnderecoBairro'])
        self.SacadoEnderecoCep = str(sacado['SacadoEnderecoCep'])
        self.SacadoEnderecoCidade = str(sacado['SacadoEnderecoCidade'])
        self.SacadoEnderecoComplemento = str(sacado['SacadoEnderecoComplemento'])
        self.SacadoEnderecoPais = str(sacado['SacadoEnderecoPais'])
        self.SacadoEnderecoUf = str(sacado['SacadoEnderecoUf'])
        self.SacadoEmail = str(sacado['SacadoEmail'])
        self.SacadoTelefone = str(sacado['SacadoTelefone'])
        self.SacadoCelular = str(sacado['SacadoCelular'])
