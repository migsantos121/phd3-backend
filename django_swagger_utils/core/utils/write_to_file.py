def write_to_file(content, path, init_required=True):
    """
    writes given content to a file
    :param content: content to be written
    :param path: path of file
    :param init_required: true or false
    :return:
    """
    from django_swagger_utils.core.utils.mk_dirs import MkDirs
    MkDirs().mk_dir_if_not_exits(file_name=path, init_required=init_required)
    new_file = open(path, 'w+')
    new_file.write(content)
    new_file.close()
    return True
