__author__ = 'vedavidh'


def get_user_supported_languages_api_wrapper(*args, **kwargs):
    from ib_common.constants.language_choices import LANGUAGES
    return {
        'languages': LANGUAGES
    }

