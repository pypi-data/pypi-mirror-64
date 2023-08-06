# Copyright © 2020 Noel Kaczmarek


class ServiceError(Exception):
    pass


class ServiceConnectError(ServiceError):
    pass


class ServiceManager(dict):
    def __init__(self, init={}):
        dict.__init__(self, init)

    def __setitem__(self, key, value):
        return super(ServiceManager, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(ServiceManager, self).__getitem__(name)

    def __delitem__(self, name):
        return super(ServiceManager, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        return ServiceManager(self)
