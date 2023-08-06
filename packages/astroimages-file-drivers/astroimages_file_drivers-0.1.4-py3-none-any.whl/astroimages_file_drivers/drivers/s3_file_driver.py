from ..driver import GenericFileDriver
from ..handler_enums import FILE_HANDLER_TYPE


class S3FileDriver(GenericFileDriver):

    def get_type(self):
        return FILE_HANDLER_TYPE.S3

    def get_files(self, folder_name, extension):
        return []

    def get_file(self, file_name):
        return {}
