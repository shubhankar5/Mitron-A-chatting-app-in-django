from django.core.exceptions import ValidationError
from datetime import date
from django.utils.translation import gettext as _


def validate_dob(value):
	print(date.today().year-value.year)
	if date.today().year-value.year >= 5 :
		return value
	else:
		return ValidationError(_('Not an appropriate date of birth'), code='invalid')