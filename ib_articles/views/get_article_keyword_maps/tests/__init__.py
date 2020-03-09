# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "get_article_keyword_maps"
REQUEST_METHOD = "post"
URL_SUFFIX = "article/keyword_maps/"


from .test_case_01 import TestCase01GetArticleKeywordMapsAPITestCase

__all__ = [
    "TestCase01GetArticleKeywordMapsAPITestCase"
]


