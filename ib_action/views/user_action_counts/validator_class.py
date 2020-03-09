from django_swagger_utils.drf_server.utils.decorator.interface_decorator import ValidatorAbstractClass

class ValidatorClass(ValidatorAbstractClass):

    def __init__(self,*args,**kwargs):
        self.request_data=kwargs['request_data']
        self.user=kwargs['user']
        # self.source=kwargs['source']
        # self.access_token=kwargs['access_token']

    def sample_validation(self):
        '''
        sample validations to be carried out here
        return True or False
        '''
        return True

    def validate(self):
        self.sample_validation()