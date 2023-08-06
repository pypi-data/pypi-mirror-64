from abc import ABC, abstractmethod


class GenericFileDriver(ABC):

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_files(self, folder_name, extension):
        pass

    @abstractmethod
    def get_file(self, file_name):
        pass
