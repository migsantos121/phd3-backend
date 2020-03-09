__author__ = 'kapeed2091'


def get_url_decoded_content(content):
    import urllib
    content = str(urllib.unquote(content).decode('utf8'))
    return content
