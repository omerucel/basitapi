import factory

from django.contrib.auth.models import User

class UserFactory(factory.Factory):
    FACTORY_FOR = User

    id = factory.Sequence(lambda a: int(a)+1)
    username = factory.Sequence(lambda a: 'username%d' %(int(a)+1))
    password = factory.Sequence(lambda a: 'password%d' %(int(a)+1))

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)

        if password:
            user.set_password(password)
            if create:
                user.save()

        return user
