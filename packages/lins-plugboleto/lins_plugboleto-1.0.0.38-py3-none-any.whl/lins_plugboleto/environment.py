class Environment(object):

    def __init__(self, sandbox):

        # Production
        if not sandbox:
            self.api = 'https://plugboleto.com.br/api/v1/'
            self.apidoc = 'https://grupolinsferrao.com.br/api/v1'
            self.apinumerodoc = 'http://127.0.0.1:5000/api-numerodoc-plugboleto/'
        else:
            self.api = 'http://homologacao.plugboleto.com.br/api/v1/'
            self.apidoc = 'https://sandbox-grupolinsferrao.com.br/api/v1'
            self.apinumerodoc = 'http://127.0.0.1:5000/api-numerodoc-plugboleto/'