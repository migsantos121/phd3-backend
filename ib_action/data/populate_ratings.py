"""
Created on 15/06/17

@author: revanth
"""


def populate_ratings(entity_ids, entity_type, source):
    import random
    user_ids = range(2, 32)
    from ib_action.models import Action
    actions_list = []
    for entity_id in entity_ids:
        user_ids_to_review = random.sample(user_ids, random.randint(20, 30))
        for user_id in user_ids_to_review:
            rating_value = random.randint(1, 5)
            actions_list.append(Action(user_id=user_id, entity_type=entity_type, entity_id=entity_id,
                                       action_type='RATE', action_value=str(rating_value), source=source))

    Action.objects.bulk_create(actions_list, batch_size=1000)


def populate_reviews(entity_ids, entity_type, source, content_list):
    import random
    from ib_action.models import Action
    from collections import defaultdict
    actions = Action.objects.filter(entity_id__in=entity_ids, entity_type=entity_type, source=source, action_type='RATE')
    entity_wise_users_dict = defaultdict(list)
    for action in actions:
        entity_wise_users_dict[action.entity_id].append(action.user_id)
    from ib_review.models import Review
    review_list = []
    for entity_id in entity_ids:
        random.shuffle(content_list)
        user_ids = entity_wise_users_dict[entity_id][:len(content_list)]
        for user_id, content in zip(user_ids, content_list):
            review_list.append(Review(entity_id=entity_id, entity_type=entity_type, user_id=user_id, source=source,
                                      content=content))

    Review.objects.bulk_create(review_list, batch_size=1000)


def populate_likes(entity_ids, entity_type, source):
    import random
    user_ids = range(2, 32)
    from ib_action.models import Action
    actions_list = []
    for entity_id in entity_ids:
        user_ids_to_review = random.sample(user_ids, random.randint(20, 30))
        for user_id in user_ids_to_review:
            actions_list.append(Action(user_id=user_id, entity_type=entity_type, entity_id=entity_id,
                                       action_type='LIKE', action_value='LIKE', source=source))

    Action.objects.bulk_create(actions_list, batch_size=1000)


def populate_shares(entity_ids, entity_type, source):
    import random
    user_ids = range(2, 32)
    from ib_action.models import Action
    actions_list = []
    for entity_id in entity_ids:
        user_ids_to_review = random.sample(user_ids, random.randint(20, 30))
        for user_id in user_ids_to_review:
            shares_count = random.randint(1, 5)
            actions_list.append(Action(user_id=user_id, entity_type=entity_type, entity_id=entity_id,
                                       action_type='SHARE', action_value=str(shares_count), source=source))

    Action.objects.bulk_create(actions_list, batch_size=1000)
