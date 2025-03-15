import hashlib
import urllib.parse


class Encryptor:
    def __init__(self, key):
        self.key = key

    def encode_data(self, data):
        return '&'.join(f"{k}={urllib.parse.quote(str(data[k]), safe='')}" for k in sorted(data.keys()))

    def cal_hash(self, input_string):
        _7032f5 = 0x15051505
        _cc1055 = _7032f5
        length = len(input_string)
        _19094e = length - 1

        while _19094e > 0:
            _7032f5 = 0x7fffffff & (_7032f5 ^ ord(input_string[_19094e]) << (length - _19094e) % 30)
            _cc1055 = 0x7fffffff & (_cc1055 ^ ord(input_string[_19094e - 1]) << _19094e % 30)
            _19094e -= 2

        return hex(_7032f5 + _cc1055)[2:].lower()
