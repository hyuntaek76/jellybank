import os
from django.conf import settings
from tempfile import SpooledTemporaryFile
from storages.backends.s3boto3 import S3Boto3Storage




__all__ = (
    'S3StaticStorage',
    'S3DefaultStorage',
)


# 정적 파일용
class S3StaticStorage(S3Boto3Storage):
    default_acl = 'public-read'
    location = 'static'


# 미디어 파일용
class S3DefaultStorage(S3Boto3Storage):
    default_acl = 'private'
    location = 'media'

    def _save_content(self, obj, content, parameters):
    # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified size
        content_autoclose = SpooledTemporaryFile()

        # Write our original content into our copy that will be closed by boto3
        content_autoclose.write(content.read())

        # Upload the object which will auto close the content_autoclose instance
        super(S3DefaultStorage, self)._save_content(obj, content_autoclose, parameters)

        # Cleanup if this is fixed upstream our duplicate should always close
        if not content_autoclose.closed:
            content_autoclose.close()
