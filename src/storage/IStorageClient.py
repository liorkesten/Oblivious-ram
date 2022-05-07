from abc import ABCMeta, abstractmethod


class IStorageClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self, filename) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def write(self, filename, data) -> bytes:
        raise NotImplementedError
