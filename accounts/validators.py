from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

def calculate_age(birth_date):
    today = timezone.now().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

@deconstructible
class MinAgeValidator(BaseValidator):
    message = _("Age must be at least %(limit_value)d.")
    code = 'min_age'

    def compare(self, birth_date, min_age):
        if birth_date is None:
            # Skip validation if birth_date is not provided
            return
        return calculate_age(birth_date) < min_age

@deconstructible
class UsernameValidator(BaseValidator):
    message = _("Username must be valid.")
    code = 'invalid_username'

    # override constructure to do ignore limit_value
    def __init__(self):
        pass

    def __call__(self, username):
        regex = "^[A-Za-z0-9_][A-Za-z0-9_.]{3,28}[A-Za-z0-9_]$"
        if not re.match(regex, username):
            raise ValidationError(self.message, code=self.code, params={"username": username})