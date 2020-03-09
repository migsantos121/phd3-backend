
class CustomDBRouter(object):
    """
       A router to control all database operations on models in the
       auth application.
       """

    def app_labels_to_route(self):
        return ['ib_users', 'django_swagger_utils', 'auth', 'sessions', 'admin', 'contenttypes', 'oauth2_provider', 'rest_framework']

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in self.app_labels_to_route():
            return 'ib_user_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        # TODO: limit write permissions to limited models and the write access only to object creation
        if model._meta.app_label in self.app_labels_to_route():
            return 'ib_user_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label not in self.app_labels_to_route() and \
                        obj2._meta.app_label not in self.app_labels_to_route():
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in self.app_labels_to_route():
            return db == 'ib_user_db'
        else:
            return db == 'default'

