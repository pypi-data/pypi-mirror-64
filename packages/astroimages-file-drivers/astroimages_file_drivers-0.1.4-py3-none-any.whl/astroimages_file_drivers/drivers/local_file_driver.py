from ..driver import GenericFileDriver
from ..handler_enums import FILE_HANDLER_TYPE
from ..util.local_file_system import list_files_in_folder


class LocalFileDriver(GenericFileDriver):

    def get_type(self):
        return FILE_HANDLER_TYPE.LOCAL

    def get_files(self, folder_name, extension):
        return list_files_in_folder(folder_name, extension)

    def get_file(self, file_name):
        return {}
