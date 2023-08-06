class Sacado(object):

    def __init__(self, cpfcnpj,nome,logradouro,numero,bairro,cep,cidade,complemento,pais,uf,email,telefone,celular):
        self.SacadoCPFCNPJ = str(cpfcnpj)
        self.SacadoNome = str(nome)
        self.SacadoEnderecoLogradouro = str(logradouro)
        self.SacadoEnderecoNumero = str(numero)
        self.SacadoEnderecoBairro = str(bairro)
        self.SacadoEnderecoCep = str(cep)
        self.SacadoEnderecoCidade = str(cidade)
        self.SacadoEnderecoComplemento = str(complemento)
        self.SacadoEnderecoPais = str(pais)
        self.SacadoEnderecoUf = str(uf)
        self.SacadoEmail = str(email)
        self.SacadoTelefone = str(telefone)
        self.SacadoCelular = str(celular)
