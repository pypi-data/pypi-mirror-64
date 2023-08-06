class Environment(object):

    def __init__(self, sandbox):

        # Production
        if not sandbox:
            self.api = 'https://plugboleto.com.br/api/v1/'
            self.apidoc = 'https://grupolinsferrao.com.br/api/v1'
        else:
            self.api = 'http://homologacao.plugboleto.com.br/api/v1/'
            self.apidoc = 'https://sandbox-grupolinsferrao.com.br/api/v1'