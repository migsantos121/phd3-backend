from abc import ABCMeta
from abc import abstractmethod
__author__ = 'vedavidh'


class AbstractCompressor(object):

    def __init__(self, *args, **kwargs):
        pass

    __metaclass__ = ABCMeta

    @abstractmethod
    def compress_string(self, string_):
        pass

    @abstractmethod
    def compress_file(self, file_name, output_file_name):
        pass

    @abstractmethod
    def decompress_string(self, compressed_string):
        pass

    @abstractmethod
    def decompress_file(self, compressed_file_name, output_file_name):
        pass
