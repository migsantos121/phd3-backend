from .abstract_compressor import AbstractCompressor

__author__ = 'vedavidh'


class ZlibCompressor(AbstractCompressor):

    def __init__(self, *args, **kwargs):
        super(ZlibCompressor, self).__init__(*args, **kwargs)

    def _write_to_file(self, string_, file_name):
        with open(file_name, 'wb') as output_file:
            output_file.write(string_)

    def compress_string(self, string_):
        import zlib
        compressed_string = zlib.compress(string_)
        return compressed_string

    def compress_file(self, file_name, output_file_name=None):
        with open(file_name, 'rb') as input_file_:
            input_file_content = input_file_.read()
            compressed_string = self.compress_string(input_file_content)
            if output_file_name:
                self._write_to_file(compressed_string, output_file_name)

        return compressed_string

    def decompress_string(self, compressed_string):
        import zlib
        string_ = zlib.decompress(compressed_string)
        return string_

    def decompress_file(self, compressed_file_name, output_file_name=None):
        with open(compressed_file_name, 'rb') as input_file_:
            input_file_content = input_file_.read()
            decompressed_string = self.compress_string(input_file_content)
            if output_file_name:
                self._write_to_file(decompressed_string, output_file_name)

        return decompressed_string
