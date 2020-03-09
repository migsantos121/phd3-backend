def api_wrapper(*args, **kwargs):

    user = kwargs["user"]
    keywords_request_data = kwargs["request_data"]
    user.language = "ENGLISH" #todo: remove

    from ib_articles.models.keyword import Keyword
    response_object = Keyword.add_keywords(user=user, keywords_request_data=keywords_request_data)
    return response_object
