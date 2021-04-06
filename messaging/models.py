from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class MessageFeatures(models.Model):
	def create_temp_path(instance, filename):
	    extension = filename.split('.')[-1]
	    time_stamp = timezone.now()
	    time_stamp = time_stamp.strftime("%d-%m-%Y_%I-%M-%S%p")
	    path = 'image_messages/Mitron {time_stamp}.{extension}'.format(
	    	time_stamp = time_stamp, 
	    	extension = extension,
	    )
	    return path

	MESSAGE_TYPE_CHOICES = [
		('t','Text'),
		('i','Image')
	]

	message_type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES, default='t')
	time_stamp = models.DateTimeField(default=timezone.now)
	text = models.CharField(max_length=2200, blank=True, null=True)
	image=models.ImageField(upload_to=create_temp_path, blank=True, null=True)
	seen = models.BooleanField(default=False)
	liked = models.BooleanField(default=False)
		
	class Meta:
		verbose_name = 'Message Features'
		verbose_name_plural = 'Message Features'

	def __str__(self):
		time_stamp = self.time_stamp.strftime("%a-%b/%d/%Y-%I:%M:%S %p %Z")
		return f"{self.get_message_type_display()}: {self.id} on {time_stamp}"

	# def save(self,*args,**kwargs):
	# 	super(MessageFeatures,self).save(*args,**kwargs)
	# 	if self.image:
	# 		img=Image.open(self.image.path)
	# 		if img.height>350 or img.width>350: #Image size is adjusted here
	# 			output_size=(350,350)
	# 			img.thumbnail(output_size)
	# 			img.save(self.image.path)


class Messages(models.Model):
	sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, related_name='to_users', null=True, on_delete=models.CASCADE)
	messages = models.ManyToManyField(MessageFeatures, related_name='whos', blank=True)

	class Meta:
		verbose_name = 'Messages'
		verbose_name_plural = 'Messages'
		UniqueConstraint( 	name='unique_pair',
    						fields=['sender', 'receiver'],
    					)

	def __str__(self):
		return f"{self.sender}'s messages to {self.receiver}"

	@classmethod
	def add_message(cls, sender, receiver, message_type='t', text=None, image=None):
		message_system = cls.objects.filter(sender=sender, receiver=receiver).first()
		if not message_system:
			message_system = cls.objects.create(sender=sender, receiver=receiver)
		message = MessageFeatures.objects.create(	message_type=message_type,
													text=text,
													image=image,
											)
		message_system.messages.add(message)
