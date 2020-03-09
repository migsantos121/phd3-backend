__author__ = 'kapeed2091'


def get_multimedia_file_from_base64(file_name, content, mime_type):
    import time
    import base64
    from django.core.files.base import ContentFile

    from ib_common.utilities.is_null_or_empty import is_null_or_empty

    try:
        if not is_null_or_empty(content):
            if not content.startswith('http'):
                file_name = file_name+'_'+str(time.time()).replace('.', '_')+'.'+mime_type
                file_ = ContentFile(base64.b64decode(content), name=file_name)
            else:
                file_ = content
        else:
            file_ = None
    except Exception as e:
        file_ = None
    return file_
