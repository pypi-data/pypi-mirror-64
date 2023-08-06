class Sacado(object):

    def __init__(self, sacado):
        self.SacadoCPFCNPJ = str(sacado['cpfcnpj'])
        self.SacadoNome = str(sacado['nome'])
        self.SacadoEnderecoLogradouro = str(sacado['logradouro'])
        self.SacadoEnderecoNumero = str(sacado['numero'])
        self.SacadoEnderecoBairro = str(sacado['bairro'])
        self.SacadoEnderecoCep = str(sacado['cep'])
        self.SacadoEnderecoCidade = str(sacado['cidade'])
        self.SacadoEnderecoComplemento = str(sacado['complemento'])
        self.SacadoEnderecoPais = str(sacado['pais'])
        self.SacadoEnderecoUf = str(sacado['uf'])
        self.SacadoEmail = str(sacado['email'])
        self.SacadoTelefone = str(sacado['telefone'])
        self.SacadoCelular = str(sacado['celular'])
