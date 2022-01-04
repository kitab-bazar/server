import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from apps.user.models import User


class UserFactory(DjangoModelFactory):
    first_name = fuzzy.FuzzyText(length=15)
    last_name = fuzzy.FuzzyText(length=15)
    email = fuzzy.FuzzyText(length=15)
    password_text = fuzzy.FuzzyText(length=15)
    password = factory.PostGeneration(lambda user, *args, **kwargs: user.set_password(user.password_text))

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password_text = kwargs.pop('password_text')
        user = super()._create(model_class, *args, **kwargs)
        user.password_text = password_text
        return user
