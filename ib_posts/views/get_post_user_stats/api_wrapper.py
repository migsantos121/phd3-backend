from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    from ib_posts.models import Post
    total, posts_media_type = Post.get_post_user_stats(user.id)

    response = {
        "total": total,
        "posts_media_type": posts_media_type
    }
    return response
