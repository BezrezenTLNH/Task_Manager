from django.contrib.auth.models import User


# Create your models here.
class Person(User):

    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name()
