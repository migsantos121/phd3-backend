def verify_relations_response(request_object, user, source):
    from ib_social.models.member_relation import MemberRelation
    response_objects = MemberRelation.verify_relations(request_object=request_object, source=source)
    return response_objects
