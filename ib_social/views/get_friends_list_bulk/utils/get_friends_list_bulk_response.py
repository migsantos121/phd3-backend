def get_friends_list_bulk_response(request_data, user, access_token, source):
    from ib_social.models import MemberRelation
    friends_list = MemberRelation.get_friends_list_bulk(request_data=request_data, user=user, source=source,
                                                        access_token=access_token)
    return friends_list
