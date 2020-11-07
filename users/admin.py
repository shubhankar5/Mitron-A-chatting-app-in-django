from django.contrib import admin
from .models import Profile, Address, Friends, BlockedUsers


admin.site.register([Profile, Address, Friends, BlockedUsers])