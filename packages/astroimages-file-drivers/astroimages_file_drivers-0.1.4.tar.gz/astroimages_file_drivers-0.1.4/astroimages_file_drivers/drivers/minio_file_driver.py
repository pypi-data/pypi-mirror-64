from ..driver import GenericFileDriver
from ..handler_enums import FILE_HANDLER_TYPE


class MinioFileDriver(GenericFileDriver):

    def get_type(self):
        return FILE_HANDLER_TYPE.MINIO

    def get_files(self, folder_name, extension):
        return []

    def get_file(self, file_name):
        return {}
