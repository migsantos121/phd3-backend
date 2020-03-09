def get_article_from_medium(url):
    """

    :param article_id:
    :param url:
    :return:
    """
    import requests
    from lxml import html

    response = requests.get(url)
    tree = html.fromstring(response.content)
    author = tree.xpath("//a[@dir='auto']/text()")[0].encode('utf-8', 'ignore')
    story = tree.xpath("//div[@class='section-inner sectionLayout--insetColumn']//text()")
    story_name = tree.xpath("//h1/text()")[0].encode('utf-8', 'ignore')
    tags = tree.xpath("//a[@class='link u-baseColor--link']/text()")
    story_f = ""
    for s in story:
        story_f = story_f + s.encode('utf-8', 'ignore')
    tag = ",".join(tags)
    record = [story_name, story_f, author, url, tag]
    return record


def get_articles_from_medium(urls, user):
    """

    :param user: 
    :param urls:
    :return:
    """
    from ib_articles.models import Article
    for each_url in urls:
        each_article = get_article_from_medium(each_url)
        from datetime import datetime
        request_data = {
            "url": each_url,
            "title": each_article[0],
            "summary": each_article[1],
            "author_name": each_article[2],
            "tags": each_article[4],
            "user": user,
            "published_time": datetime.now()
        }

        Article.add_article(**request_data)


def scrape_medium():
    urls = [
        "https://blog.baremetrics.com/how-to-transition-from-customer-support-to-customer-success-d3b116c00835#.44501sf7n"
    ]

    user = get_admin_user()

    get_articles_from_medium(urls, user)


def get_admin_user():
    from django.contrib.auth import get_user_model
    user = get_user_model()
    users = user.objects.filter(is_staff=True)
    return users[0]


if __name__ == "__main__":
    scrape_medium()
