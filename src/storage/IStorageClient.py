from abc import ABCMeta, abstractmethod


class IStorageClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self, filename):
        raise NotImplementedError

    @abstractmethod
    def write(self, filename, data):
        raise NotImplementedError
