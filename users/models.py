from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"{self.pk}:{self.fullname} ({self.email})"
