from .models import Notifications


def notify(request):
	if request.user.is_authenticated:
		notifications = Notifications.objects.filter(to_user=request.user).order_by('-id')
		notifications_count = notifications.filter(seen=False).count()
		if notifications_count:
			last = notifications.first().id
		else:
			last = 0
		print(notifications_count)

		return {
					'last' : last,
					'notifications' : notifications,
					'notifications_count' : notifications_count,
				}
	else:
		return {
					'last' : 0,
					'notifications' : None,
					'notifications_count' : 0,
				}