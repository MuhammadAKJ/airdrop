import random
import string
from django.db import models

class AccessCode(models.Model):
    code = models.CharField(max_length=7, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
