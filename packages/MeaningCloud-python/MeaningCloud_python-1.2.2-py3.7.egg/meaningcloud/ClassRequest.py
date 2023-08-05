import meaningcloud.Request


class ClassRequest(meaningcloud.Request):

    endpoint = 'class-1.1'
    otherparams = None
    extraheaders = None
    type_ = ""

    def __init__(self, key, txt=None, url=None, doc=None, model='IPTC_en', otherparams=None, extraheaders=None, server='https://api.meaningcloud.com/'):
        """
        ClassRequest constructor

        :param key:
            license key
        :param txt:
            Text to use in the API calls
        :param url:
            Url to use in the API calls
        :param doc:
            File to use in the API calls
        :param model:
            Name of the model to use in the classification
        :param otherparams:
            Array where other params can be added to be used in the API call
        :param server:
            String with the server the requests will be sent to
        """

        if server[len(server)-1] != '/':
            server += '/'

        self._params = {}
        meaningcloud.Request.__init__(self, (server + self.endpoint), key)
        self.otherarams = otherparams
        self.extraheaders = extraheaders
        self._url = server + self.endpoint

        self.addParam('key', key)
        self.addParam('model', model)

        if txt:
            type_ = 'txt'
        elif doc:
            type_ = 'doc'
        elif url:
            type_ = 'url'
        else:
            type_ = 'default'

        options = {'doc': lambda: self.setContentFile(doc),
                   'url': lambda: self.setContentUrl(url),
                   'txt': lambda: self.setContentTxt(txt),
                   'default': lambda: self.setContentTxt(txt)
                   }
        options[type_]()
        if (otherparams):
            for key in otherparams:
                self.addParam(key, otherparams[key])

    def sendReq(self):
        return self.sendRequest(self.extraheaders)
