from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from ib_action.models import Action
    return Action.get_user_counts(**kwargs)
