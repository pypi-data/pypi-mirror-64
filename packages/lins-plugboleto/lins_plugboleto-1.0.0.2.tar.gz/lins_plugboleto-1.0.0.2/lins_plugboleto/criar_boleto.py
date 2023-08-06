
from .objectJSON import ObjectJSON


class CriarBoleto(ObjectJSON):

    def __init__(self, nosso_numero,valor,numero_doc,dataemi,local_pagamento,prazo_vencimento):
        self.idintegracao = None
        self.situacao = None
        self.sacado = None
        #self.SacadoNome = None
        #self.SacadoEnderecoLogradouro = None
        #self.SacadoEnderecoNumero = None
        #self.SacadoEnderecoBairro = None
        #self.SacadoEnderecoCep = None
        #self.SacadoCPFCNPJ = None
        #self.SacadoEnderecoCidade = None
        #self.SacadoEnderecoComplemento = None
        #self.SacadoEnderecoPais = None
        #self.SacadoEnderecoUf = None
        #self.SacadoEmail = None
        #self.SacadoTelefone = None
        #self.SacadoCelular = None
        self.cedente = None
        #self.CedenteContaCodigoBanco = None
        #self.CedenteContaNumero = None
        #self.CedenteContaNumeroDV = None
        #self.CedenteConvenioNumero = None
        #self.cedente = None
        #self.titulo =None
        self.TituloNossoNumero = str(nosso_numero)
        self.TituloValor = str(valor)
        self.TituloNumeroDocumento = str(numero_doc)
        dataemissao = dataemi.strftime('%d/%m/%Y')
        self.TituloDataEmissao = dataemissao
        datavencimento = abs(dataemissao + prazo_vencimento)
        datavencimento = datavencimento.strftime('%d/%m/%Y')
        self.TituloDataVencimento = datavencimento
        self.TituloAceite = None
        self.TituloDocEspecie = None
        self.TituloLocalPagamento = local_pagamento
        self.juros = None
        #self.TituloCodigoJuros = None
        #self.TituloDataJuros = None
        #self.TituloValorJuros = None
        self.multa = None
        #self.TituloCodigoMulta = None
        #self.TituloDataMulta = None
        #self.TituloValorMultaTaxa = None
        self.protesto = None
        #self.TituloCodProtesto = None
        #self.TituloPrazoProtesto = None
        self.baixa = None
        #self.TituloCodBaixaDevolucao = None
        #self.TituloPrazoBaixa = None
        self.mensagens = None
        #self.TituloMensagem01 = None
        #self.TituloMensagem02 = None
        #self.TituloMensagem03 = None
        #self.sacadoravalista = None
        self.outros = None
        #self.TituloEmissaoBoleto = None
        #self.TituloCategoria = None
        #self.TituloPostagemBoleto = None
        #self.TituloCodEmissaoBloqueto = None
        #self.TituloCodDistribuicaoBloqueto = None
        #self.TituloOutrosAcrescimos = None
        #self.TituloInformacoesAdicionais = None
        #self.TituloInstrucoes = None
        #self.TituloParcela = None
        #self.TituloVariacaoCarteira = None
        #self.TituloCodigoReferencia = None
        #self.TituloTipoCobranca = None

    def update_return(self, r):
        dados = r.get('_dados') or {}
        sucesso = dados.get('_sucesso') or {}
        self.idintegracao = sucesso.get('idintegracao')
        self.situacao = sucesso.get('situacao')
        self.TituloNumeroDocumento = sucesso.get('TituloNumeroDocumento')
        self.TituloNossoNumero = sucesso.get('TituloNossoNumero')
        self.cedente.CedenteContaCodigoBanco = sucesso.get('CedenteContaCodigoBanco')
        self.cedente.CedenteContaNumero = sucesso.get('CedenteContaNumero')
        self.cedente.CedenteConvenioNumero = sucesso.get('CedenteConvenioNumero')