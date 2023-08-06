# -*- coding: utf8 -*-
import hashlib


class MD5(object):

    @staticmethod
    def md5(s):
        if isinstance(s, str):
            s = s.encode('utf-8')
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()
