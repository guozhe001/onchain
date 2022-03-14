# encoding=utf8


class CryptoException(Exception):
    def __init__(self, *args, **kwargs):
        super(CryptoException, self).__init__(*args, **kwargs)
