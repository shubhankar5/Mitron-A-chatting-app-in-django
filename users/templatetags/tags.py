from django import template
from django.contrib.auth.models import User
from messaging.models import MessageFeatures
from messaging.crypto import decrypt


register = template.Library()


@register.filter
def get_tag(tags):
    return 'danger' if tags == 'error' else tags


@register.filter
def get_sender(q):
	return q.first().sender


@register.filter
def get_user(id):
	return User.objects.get(id=id)


@register.filter
def get_first_name(id):
	return User.objects.get(id=id).profile.first_name


@register.filter
def get_last_name(id):
	return User.objects.get(id=id).profile.last_name


@register.filter
def is_seen(id):
	return MessageFeatures.objects.get(id=id).seen


@register.filter
def length(text):
	if len(text)>30:
		return True
	else:
		return False


@register.filter
def dec(text):
	# print(decrypt(text))
	return decrypt(text)
