def api_wrapper(request_data, user, source):

    from ib_social.models import MemberRelation
    return MemberRelation.get_relation_stats(request_data,source)

