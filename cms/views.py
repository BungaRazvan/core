from .base import CMSView


class Login(CMSView):

    @staticmethod
    def execute(self):
        return {'hey': 'var'}
