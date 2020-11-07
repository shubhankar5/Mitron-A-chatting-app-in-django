from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from datetime import date
from .validators import validate_dob
from django.core.cache import cache 
import datetime
from chat_app import settings
from uuid import uuid4


class Profile(models.Model):
	def dp_rename_and_path(instance, filename):
	    extension = filename.split('.')[-1]
	    time_stamp = timezone.now()
	    time_stamp = time_stamp.strftime("%d-%m-%Y_%I-%M-%S%p")
	    path = 'profile_pics/{username}/{time_stamp}_{randomstring}.{extension}'.format(
	    	username = instance.user.username, 
	    	time_stamp = time_stamp, 
	    	randomstring = uuid4().hex, 
	    	extension = extension,
	    )
	    print(path)
	    return path

	SEX_CHOICES = [
		('m','Male'),
		('f','Female'),
		('o','Others'),
	]

	dob_default = date.today()
	dob_default = dob_default.replace(year = dob_default.year-5)
	user=models.OneToOneField(User,on_delete = models.CASCADE)
	display_picture=models.ImageField(default = 'profile_pics/default.jpg', upload_to = dp_rename_and_path)
	first_name=models.CharField(max_length = 20)
	last_name=models.CharField(max_length = 20)
	sex = models.CharField(max_length = 1, choices = SEX_CHOICES, default = 'm')
	dob=models.DateField(default=dob_default, validators = [validate_dob], verbose_name='Date of Birth')
	bio=models.TextField(max_length = 100, default = "Hi there! Let's be friends")

	def __str__(self):
		return f"{self.user.username}'s Profile"
		
	def save(self,*args,**kwargs):
		super(Profile,self).save(*args,**kwargs)

		img=Image.open(self.display_picture.path)
		print('andar hu bsdk')
		if img.height>300 or img.width>300:
			output_size=(300,300)
			img.thumbnail(output_size)
			img.save(self.display_picture.path)


class Address(models.Model):
    profile=models.OneToOneField(Profile,on_delete=models.CASCADE)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=50)

    class Meta:
    	verbose_name = 'Address'
    	verbose_name_plural = 'Address'

    def __str__(self):
    	return f"{self.profile.user.username}'s Address"


class Friends(models.Model):
	current_user = models.OneToOneField(User, related_name='owner', on_delete=models.CASCADE)
	friends = models.ManyToManyField(User, related_name='friends', blank=True)
	pending_sent_list = models.ManyToManyField(User, related_name='pending_sent_list', blank=True)
	pending_received_list = models.ManyToManyField(User, related_name='pending_received_list', blank=True)
	
	class Meta:
		verbose_name = 'Friends'
		verbose_name_plural = 'Friends'

	def __str__(self):
		return f"{self.current_user}'s friends"

	@classmethod
	def add_friend(cls, to_user, from_user):
		from_user_friendlist = cls.objects.get(current_user = from_user)
		to_user_friendlist = cls.objects.get(current_user = to_user)
		from_user_friendlist.pending_sent_list.add(to_user)
		to_user_friendlist.pending_received_list.add(from_user)

	@classmethod
	def remove_friend(cls, friend_user, from_user):
		from_user_friendlist = cls.objects.get(current_user = from_user)
		friend_user_friendlist = cls.objects.get(current_user = friend_user)
		from_user_friendlist.friends.remove(friend_user)
		friend_user_friendlist.friends.remove(from_user)

	@classmethod
	def cancel_sent_request(cls, to_user, from_user):
		from_user_friendlist = cls.objects.get(current_user = from_user)
		to_user_friendlist = cls.objects.get(current_user = to_user)
		from_user_friendlist.pending_sent_list.remove(to_user)
		to_user_friendlist.pending_received_list.remove(from_user)

	@classmethod
	def handle_received_request(cls, to_user, from_user, choice):
		from_user_friendlist = cls.objects.get(current_user = from_user)
		to_user_friendlist = cls.objects.get(current_user = to_user)
		if choice == 'accept':
			from_user_friendlist.friends.add(to_user)
			to_user_friendlist.friends.add(from_user)
			from_user_friendlist.pending_received_list.remove(to_user)
			to_user_friendlist.pending_sent_list.remove(from_user)

		elif choice == 'decline':
			from_user_friendlist.pending_received_list.remove(to_user)
			to_user_friendlist.pending_sent_list.remove(from_user)

 
class BlockedUsers(models.Model):
	user = models.OneToOneField(User, related_name='me', on_delete=models.CASCADE)
	blocked_list = models.ManyToManyField(User, related_name='is_blocked_by', blank=True)

	class Meta:
		verbose_name = 'Blocked Users'
		verbose_name_plural = 'Blocked Users'

	def __str__(self):
		return f"{self.user}'s blocked list"

	@classmethod
	def block_user(cls, user, user_to_be_blocked):
		f1 = Friends.objects.get(current_user=user)
		f2 = Friends.objects.get(current_user=user_to_be_blocked)
		f1.pending_sent_list.remove(user_to_be_blocked)
		f1.pending_received_list.remove(user_to_be_blocked)
		f1.friends.remove(user_to_be_blocked)
		f2.pending_sent_list.remove(user)
		f2.pending_received_list.remove(user)
		f2.friends.remove(user)
		obj = cls.objects.get(user=user)
		obj.blocked_list.add(user_to_be_blocked)

	@classmethod
	def unblock_user(cls, user, blocked_user):
		obj = cls.objects.get(user=user)
		obj.blocked_list.remove(blocked_user)


class Notifications(models.Model):
	TYPE_CHOICES = [
		('sent', 'sent you a friend request'),
		('accepted', 'accepted your friend request'),
	]

	to_user = models.ForeignKey(User, related_name='my_notifications', on_delete=models.CASCADE)
	type = models.CharField(max_length = 10, choices = TYPE_CHOICES, default = 'sent')
	seen = models.BooleanField(default = False)
	time_stamp = models.DateTimeField(default=timezone.now)
	from_user = models.ForeignKey(User, related_name='about_whom', on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Notifications'
		verbose_name_plural = 'Notifications'

	def __str__(self):
		time_stamp = self.time_stamp.strftime("%a-%b/%d/%Y-%I:%M:%S %p %Z")
		return f"ID: {self.id} | {self.to_user}'s notification at {time_stamp}"	

	@classmethod
	def add_notification(cls, to_user, type, from_user):
		n = cls.objects.filter( to_user=to_user,
								from_user = from_user
								)
		print(n.count())
		if n.count()>20:
			n.first().delete()
		n = cls.objects.create(	to_user=to_user,
								type = type,
								from_user = from_user
								)
		n.save()

	@classmethod
	def delete_notification(cls, to_user, type, from_user):
		try:
			n = cls.objects.get(to_user=to_user,
								type = type,
								from_user = from_user
								)
		except:
			n = cls.objects.none()
		n.delete()
