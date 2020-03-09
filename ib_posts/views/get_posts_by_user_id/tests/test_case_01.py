from mock import mock

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "search_q": "", 
     "offset":0,
    "filters": {
        "sorts": {
            "posted_date":"asc"
        },
        "include_article_info": true
    },
    "limit":10
}
"""

response_body = """
[
    {
        "creation_datetime": "2017-07-18 20:15:23.711321", 
        "post_id": 1, 
        "content": "This is a test content.", 
        "multimedia_url": null, 
        "article_info": {
            "published_time": "2012-08-12 12:21:00", 
            "title": "title", 
            "url": "url", 
            "image": null, 
            "tags": null, 
            "author_name": "tanmay", 
            "summary": "summary"
        }, 
        "user_id": 1, 
        "multimedia_type": null, 
        "article_id": 1
    }
]
"""

test_case = {
    "request": {
        "path_params": {"user_id": "1"},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}

def now():
    import datetime
    return datetime.datetime(2017, 7, 18, 20, 15, 23, 711321)


class TestCase01GetPostsByUserIdAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetPostsByUserIdAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    @mock.patch('django.utils.timezone.now', now)
    def test_case(self):

        from ib_articles.models.article import Article
        a = Article.objects.create(_title="title", _summary="summary", _url="url",
                                   _published_time="2012-08-12 12:21:00",
                                   _author_name='tanmay')

        from ib_posts.models.post import Post
        post = Post.objects.create(_contents='This is a test content.', article_id=1, user_id=1)
        response = super(TestCase01GetPostsByUserIdAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01GetPostsByUserIdAPITestCase, self).setupUser(username, password)

        self.foo_user.first_name = "user"
        self.foo_user.save()


