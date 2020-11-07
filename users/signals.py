from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Address, Friends, BlockedUsers
import os
import shutil


def file_to_dir(old_path):
    path = old_path
    path = path.split('/')[:-1]
    path = '/'.join(path)
    return path
        

@receiver(post_save,sender=User)
def create_profile_and_friends(sender,instance,created,**kwargs):
	if created:
		Profile.objects.create(user=instance)
		Address.objects.create(profile=instance.profile)
		Friends.objects.create(current_user=instance)
		BlockedUsers.objects.create(user=instance)


@receiver(post_delete, sender=Profile)
def delete_dp_folder_2(sender, instance, **kwargs):
    if instance.display_picture:
        path = file_to_dir(instance.display_picture.path)
        if  os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)