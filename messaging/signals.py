from django.db.models.signals import pre_delete, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Messages, MessageFeatures
import os


@receiver(pre_delete, sender=User)
def handle_deleted_messages(sender, instance, **kwargs):
	deleted_user, created = User.objects.get_or_create(username='deleted')
	if created:
		deleted_user.profile.first_name = 'Deleted'
		deleted_user.profile.last_name = 'User'
	try:
		m1 = Messages.objects.get(sender=instance)
		m1.pk = None
		m1.sender = deleted_user
		m1.save()
	except:
		pass
	try:
		m2 = Messages.objects.get(receiver=instance)
		m2.pk = None
		m2.receiver = deleted_user
		m2.save()
	except:
		pass


@receiver(post_delete, sender=MessageFeatures)
def delete_image_messages(sender, instance, **kwargs):
    if instance.image:
    	if os.path.isfile(instance.image.path):
    		os.remove(instance.image.path) 