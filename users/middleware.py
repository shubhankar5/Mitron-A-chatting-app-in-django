from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from . import views as user_views
from django.core.cache import cache
from datetime import datetime
from django.contrib import auth
import time
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import redirect_to_login



EXEMPT_URLS = [reverse(settings.LOGIN_URL)]
if hasattr(settings, 'EXEMPT_URLS'):
	EXEMPT_URLS += [reverse(url) for url in settings.EXEMPT_URLS]

class LoginRequiredMiddleware:

	def __init__(self, get_ressponse):
		self.get_ressponse = get_ressponse

	def __call__(self,request):
		response = self.get_ressponse(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		
		assert hasattr(request,'user')
		path = request.path_info
		url_is_exempt = any(url == path for url in EXEMPT_URLS)

		if request.user.is_authenticated and url_is_exempt:
			return redirect('users-home')

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


SESSION_TIMEOUT_KEY = "_session_init_timestamp_"


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, "session") or request.session.is_empty():
        	return 

        init_time = request.session.setdefault(SESSION_TIMEOUT_KEY, time.time())

        expire_seconds = getattr(
            settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
        )

        session_is_expired = time.time() - init_time > expire_seconds

        if session_is_expired:
            logout(request)
            request.session.flush()
            messages.info(request, "You have been logged out due to inactivity")
            return redirect_to_login(next=request.path)

        expire_since_last_activity = getattr(
            settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY", True
        )
        grace_period = getattr(
            settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD", 1
        )

        if expire_since_last_activity and time.time() - init_time > grace_period:
            request.session[SESSION_TIMEOUT_KEY] = time.time()