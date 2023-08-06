from .reflection import *


class Object(object):
    def __init__(self, fields={}):
        self.__dict__ = fields

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def getFieldValue(self, key):
        return self.__dict__[key]

    def setFieldValue(self, key, value):
        self.__dict__[key] = value

    def getFieldKeys(self):
        return getFieldKeys(self)

    def getFieldValues(self):
        return getFieldValues(self)

    def getFields(self):
        return getFields(self)

    def getPublicFields(self):
        return getPublicFields(self)

    def getPrivateFields(self):
        return getPrivateFields(self)

    def getMethods(self):
        return getMethods(self)

    def getPublicMethods(self):
        return getPublicMethods(self)

    def getPrivateMethods(self):
        return getPrivateMethods(self)
