from ..driver import GenericFileDriver
from ..handler_enums import FILE_HANDLER_TYPE


class NullFileDriver(GenericFileDriver):

    def get_type(self):
        return FILE_HANDLER_TYPE.NULL

    def get_files(self, folder_name, extension):
        return ['NullFileDriver']

    def get_file(self, file_name):
        return {
            'NullFileDriver': NullFileDriver
        }
