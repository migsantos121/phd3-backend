__author__ = 'vedavidh'


class VernacularUtilitiesClass(object):

    def __init__(self):
        self.language_name, valid = self.validate_language()

        fields = self._meta.get_fields()
        fields = [field for field in fields if field.name.startswith('_')]
        for field in fields:
            field_name = field.name
            setattr(self, '_i' + field.name, getattr(self, field_name))

    @classmethod
    def get_language_variable_fields(cls):
        fields = cls._meta.get_fields()
        fields = [field for field in fields if field.name.startswith('_')]
        return fields

    @classmethod
    def validate_language(cls, language_name=None):
        from ib_common.constants.language_choices import LANGUAGES, DEFAULT_LANGUAGE
        valid = True
        if language_name is None or language_name not in LANGUAGES:
            if language_name is not None and language_name not in LANGUAGES:
                valid = False
            language_name = DEFAULT_LANGUAGE
        return language_name, valid

    def get_language_specific_details(self, language_name=None, attr_name='vernacular_details'):
        language_name, valid = self.validate_language(language_name=language_name)
        list_ = filter(lambda x: x.language_name == language_name, getattr(self, attr_name).all())
        if len(list_) > 1:
            pass
        return list_[0]

    def set_language_specific_attributes(self, **kwargs):
        l_name = kwargs.get('language_name', None)
        force_update = kwargs.get('force_update', False)

        language_name, valid = self.validate_language(language_name=l_name)

        if not ((self.language_name != language_name) or force_update):
            return

        fields = self._meta.get_fields()
        fields = [field for field in fields if field.name.startswith('_')]

        try:
            obj_details = self.get_language_specific_details(language_name=language_name)
        except IndexError:
            obj_details = None
        for field in fields:
            field_name = field.name
            if obj_details:
                setattr(self, '_i' + field_name, getattr(obj_details, 'v'+field_name))

        l_update_relations = kwargs.get('l_update_relations', False)

        if l_update_relations:
            f_var_names = kwargs.get('f_keys_list', [])
            for f_key in f_var_names:
                obj = getattr(self, f_key)
                if obj:
                    obj.set_language_specific_attributes(language_name=language_name)
                    setattr(self, f_key, obj)
        self.language_name = language_name
        return self

    @classmethod
    def set_language_specific_attributes_bulk(cls, objs, **kwargs):
        new_objs = []
        for obj in objs:
            obj.set_language_specific_attributes(**kwargs)
            new_objs.append(obj)
        return new_objs

    @classmethod
    def update_language_specific_details_bulk(cls, id_details_dict, rel_model, obj_name, language_name=None):
        """

        :param id_details_dict: {1: {'name': 'New name', 'description': 'New description'}}
        :param rel_model:
        :param obj_name:
        :param language_name:
        :return:
        """

        for item in id_details_dict.items():
            int(item[0])
            if not set(item[1].keys()).issubset(set(cls.get_language_variable_fields())):
                return

        kwargs = {obj_name+'_id__in': id_details_dict.keys()}

        language_name, valid = cls.validate_language(language_name=language_name)
        objs = rel_model.objects.filter(**kwargs).filter(language_name=language_name)

        unsaved_objs = []
        for obj in objs:
            dict_ = id_details_dict[getattr(obj, obj_name+'_id')]
            for item in dict_.items():
                setattr(obj, item[0], item[1])
            unsaved_objs.append(obj)

        from ib_common.db_utilities.bulk_update import bulk_update
        bulk_update(unsaved_objs)

    @classmethod
    def get_vernacular_query(cls, query_set):

        # handling select_related

        # handling values, values_list

        # handling prefetch_related

        # handling filter, exclude

        #

        pass
