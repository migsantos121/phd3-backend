def validate_users_credentials_and_get_users_details(users_credentials):
    user_names = [each_user['username'] for each_user in users_credentials]

    from ib_users.models.ib_user import IBUser
    ib_user_objs = IBUser.objects.filter(username__in=user_names)

    ib_user_objs_dict = convert_ib_user_objs_to_dict(ib_user_objs)
    valid_usernames = ib_user_objs_dict.keys()

    response_list = list()
    for each_user in users_credentials:
        if each_user['username'] in valid_usernames:
            ib_user_obj = ib_user_objs_dict[each_user['username']]
            if ib_user_obj.check_password(each_user['password']):
                response_list.append({'user_name': ib_user_obj.username, 'user_details': {
                    'id': ib_user_obj.id,
                    'username': ib_user_obj.username,
                    'pic': ib_user_obj.pic,
                    'pic_thumbnail': ib_user_obj.pic_thumbnail,
                    'name': ib_user_obj.name,
                    'dob': ib_user_obj.dob
                }})
            else:
                response_list.append({'username': ib_user_obj.username, 'user_details': None})
        else:
            response_list.append({'username': each_user['username'], 'user_details': None})
    return response_list


def convert_ib_user_objs_to_dict(ib_user_objs):
    ib_user_objs_dict = dict()
    for each_obj in ib_user_objs:
        ib_user_objs_dict[each_obj.username] = each_obj
    return ib_user_objs_dict
