"""
Created on 14/06/17

@author: revanth
"""
resource_types = ['ib_courses.KCourses', 'ib_videos.Video', 'ib_podcasts.Podcast', 'ib_books.Book', 'vi_articles.Article']


def populate_save_status_data(user_id, data_dict, source):
    from ib_action.models import Action
    actions_list = []
    for resource_type in resource_types:
        for resource in data_dict[resource_type]:
            actions_list.append(Action(entity_id=resource[0], entity_type=resource_type, user_id=user_id, source=source,
                                       action_type='SAVE_STATUS', action_value=resource[1]))
    print len(actions_list), 'actions added'
    Action.objects.bulk_create(actions_list)


actions_data = {
    'ib_courses.KCourses': [(11, 'SAVED'), (12, 'SAVED'), (13, 'SAVED'), (14, 'SAVED'), (15, 'SAVED'),
                            (16, 'COMPLETED'), (17, 'COMPLETED'), (18, 'COMPLETED'), (19, 'COMPLETED'), (20, 'COMPLETED')],
    'ib_videos.Video': [(11, 'SAVED'), (12, 'SAVED'), (13, 'SAVED'),
                        (16, 'COMPLETED'), (17, 'COMPLETED'), (18, 'COMPLETED')],
    'ib_podcasts.Podcast': [(11, 'SAVED'), (12, 'SAVED'), (13, 'SAVED'), (14, 'SAVED'),
                            (16, 'COMPLETED'), (17, 'COMPLETED'), (18, 'COMPLETED'), (19, 'COMPLETED')],
    'ib_books.Book': [(41, 'SAVED'), (46, 'COMPLETED')],
    'vi_articles.Article': [(11, 'SAVED'), (12, 'SAVED'), (17, 'COMPLETED'), (18, 'COMPLETED')],
}
