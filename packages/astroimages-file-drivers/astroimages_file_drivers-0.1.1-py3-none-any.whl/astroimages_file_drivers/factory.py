import astroimages_file_drivers.handler_enums as handler_enums

# TODO: Ugly code, need to be refactored
import astroimages_file_drivers.drivers.minio_file_driver as minio_file_driver
import astroimages_file_drivers.drivers.local_file_driver as local_file_driver
import astroimages_file_drivers.drivers.null_file_driver as null_file_driver
import astroimages_file_drivers.drivers.s3_file_driver as s3_file_driver

_handlers = {
        handler_enums.FILE_HANDLER_TYPE.NULL: null_file_driver.NullFileDriver,
        handler_enums.FILE_HANDLER_TYPE.LOCAL: local_file_driver.LocalFileDriver,
        handler_enums.FILE_HANDLER_TYPE.S3: s3_file_driver.S3FileDriver,
        handler_enums.FILE_HANDLER_TYPE.MINIO: minio_file_driver.MinioFileDriver
    }


def get_file_driver(handler_type):
    return _handlers[handler_type]()
