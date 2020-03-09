__author__ = 'kapeed2091'


def multimedia_thumbnail_file_name(self, file_name):
    import datetime
    import os
    import uuid

    app_label = self._meta.app_label
    model_name = self._meta.model_name
    file_path, file_extension = os.path.splitext(file_name)
    url = app_label + '/' + model_name + '/thumbnails/' + str(uuid.uuid1()) + '_' + str(datetime.datetime.now()).strip()\
        .replace(' ', '_') + file_extension
    return url
