def get_application_id(client_id, client_secret):
    from oauth2_provider.models import Application
    try:
        application = Application.objects.get(client_id=client_id,
                                              client_secret=client_secret)
        return application.id
    except Application.DoesNotExist:
        from django.utils.translation import ugettext_lazy as _
        from django_swagger_utils.drf_server.exceptions.not_found import \
            NotFound
        raise NotFound(str(_('Application not found')), res_status='')
