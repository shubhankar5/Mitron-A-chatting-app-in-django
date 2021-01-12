from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileCreateForm, ProfileUpdateForm, AddressForm, ProfilePictureForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Friends, BlockedUsers, Notifications
from messaging.models import Messages
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_safe, require_http_methods
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator


@require_http_methods(["GET", "POST"])
def init(request):
	if request.method=='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request,user)
				messages.success(request,f'Your account has been created. Complete your profile and enjoy chatting!')
				return redirect('users-home')
			else:
				raise Http404()
	else:
		form = UserRegisterForm()
	return render(request,'users/init.html',{'form':form})


@require_http_methods(["GET", "POST"])
def login_view(request):
	if request.method=='POST':
		form = AuthenticationForm(request,request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request,user)
				return redirect('users-home')
			else:
				raise Http404()
	else:
		form = AuthenticationForm()
	return render(request,'users/login.html',{'form':form})


@require_safe
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out!")
    return redirect('login')


@require_http_methods(["GET", "POST"])
@login_required
def my_profile_view(request):
	if not request.user.profile.first_name:
		if request.method=='POST':
			profile_form = ProfileCreateForm(request.POST, instance=request.user.profile)
			address_form = AddressForm(request.POST, instance=request.user.profile.address)
			if profile_form.is_valid() and address_form.is_valid():
				profile_form.save()
				address_form.save()
				messages.success(request,f'Your profile has been created!')
				return redirect('users-home')
		else:
			profile_form = ProfileCreateForm(instance=request.user.profile)
			address_form = AddressForm(instance=request.user.profile.address)
		return render(request,'users/new_profile.html',{	'profile_form':profile_form,
															'address_form':address_form
														})
	else:
		if request.method=='POST':
			dp_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
			if dp_form.is_valid():
				dp_form.save()
				messages.success(request,f'Your profile picture has been updated!')
				return redirect('users-profile')
		else:
			dp_form = ProfilePictureForm()
		return render(request,'users/profile.html', {	'person' : request.user,
														'dp_form' : dp_form })


@require_http_methods(["GET", "POST"])
@login_required
def update_profile(request):
	if request.method=='POST':
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
		add_form = AddressForm(request.POST,instance=request.user.profile.address)
		if u_form.is_valid() and p_form.is_valid() and add_form.is_valid():
			u_form.save()
			p_form.save()
			add_form.save()
			messages.success(request,f'Your profile has been updated!')
			return redirect('users-profile')
				
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		add_form = AddressForm(instance=request.user.profile.address)
	return render(request,'users/update_profile.html',	{	'u_form':u_form,
															'p_form':p_form,
															'add_form':add_form
														})


@require_http_methods(["GET", "POST"])
@login_required
def update_profile_picture(request):
	if request.is_ajax():
		mode = request.GET.get('mode')
		if mode == 'remove-picture':
			request.user.profile.display_picture = 'profile_pics/default.jpg'
			request.user.profile.save()
			messages.success(request,'Profile picture has been successfully removed')
			message = 'removed'
		return JsonResponse({ 'message' : message })


@require_safe
@login_required
def others_profile_view(request, id):
	if id == request.user.id or id == User.objects.get(username='deleted').id:
		raise Http404()
	else:
		try:
			person = User.objects.get(id = id)
		except:
			raise Http404()

		sent = received = is_friend =  True
		is_blocked = False 
		try:
			request.user.pending_sent_list.get(current_user=person)
		except:
			sent = False
		try:
			request.user.pending_received_list.get(current_user=person)
		except:
			received = False
		try:
			request.user.friends.get(current_user=person)
		except:
			is_friend = False
		if person.is_blocked_by.filter(user=request.user).exists():
			is_blocked = True
		return render(request,'users/profile.html', {	'person' : person,
														'sent' : sent,
														'received' : received,
														'is_friend': is_friend,
														'is_blocked' : is_blocked
													})


def queryset_users(request, search_text):
	if len(search_text):
		blocked_users_id = request.user.is_blocked_by.all().values('user__id')
		try:
			users_all = User.objects.filter(
						Q(username__istartswith = search_text) |
						Q(first_name__istartswith = search_text) |
						Q(last_name__istartswith = search_text)
					).order_by(
						Lower('profile__first_name'),
						Lower('profile__last_name')
					).exclude(
						Q(id = request.user.id) |
						Q(id = User.objects.get(username='deleted').id) |
						Q(id__in = blocked_users_id)
					)
					
			size = len(users_all)
		except:
			users_all = None
			size = 0
	else:
		users_all = None
		size = -1
	return users_all, size


@require_safe
@login_required
def search_users(request):
	if request.is_ajax():
		search_text = request.GET.get('search_text')
		users_all, size = queryset_users(request, search_text)
		max_results = 6
		if size >= max_results:
			users_some = users_all[:max_results]
			size = max_results
		else :
			users_some = users_all
		return render(request, 'users/search_results.html', {	'users' : users_some,
																'mode' : 'users', 
																'size' : size,
																'max_results' : max_results
															})


@require_safe
@login_required
def search_results_users(request, search_text=None): 
	if search_text:
		users_all, size = queryset_users(request, search_text)
		paginator = Paginator(users_all, 10)
		page_number = request.GET.get('page')
		page_users = paginator.get_page(page_number)
		return render(request, 'users/search_results_view_all.html', {	'search_text' : search_text,
																		'page_users' : page_users,
																	})	
	else:
		raise Http404('First search something!')


@require_http_methods(["POST"])
@login_required
def change_friends(request):
	if request.is_ajax():
		choice = request.POST['choice']
		friend = User.objects.get(id = request.POST['user_id'])

		CHANGE_FRIENDS_MESSAGES = {
			'add' : f'Friend request sent to {friend.username} :)',
			'remove' : f'{friend.username} is not your friend anymore!',
			'cancel_request' : 'Friend request deleted!',
			'accept' : f'{friend.username} and you are friends now :)',
			'decline' : 'Friend request declined!'
		}

		if choice == 'add':
			Friends.add_friend(request.user, friend)
			Notifications.add_notification(friend, 'sent', request.user)
		elif choice == 'remove':
			Friends.remove_friend(request.user, friend)
		elif choice == 'accept' or choice == 'decline':
			Friends.handle_received_request(request.user, friend, choice)
			if choice == 'accept':
				Notifications.add_notification(friend, 'accepted', request.user)
		elif choice == 'cancel_request':
			Friends.cancel_sent_request(request.user, friend)
			Notifications.delete_notification(friend, 'sent', request.user)
		data = {
			'message' : CHANGE_FRIENDS_MESSAGES[choice]
		}
		messages.info(request, data['message'])
		return JsonResponse(data)


@require_safe
@login_required
def search_friends(request):
	if request.is_ajax():
		search_text = request.GET.get('search_text','')
		mode = request.GET.get('mode')
		friends_object = Friends.objects.get(current_user = request.user)
		try:
			friends = friends_object.friends.filter(
						Q(username__istartswith = search_text) |
						Q(first_name__istartswith = search_text) |
						Q(last_name__istartswith = search_text)
					).exclude(
						username = 'deleted'
					).order_by(
						Lower('profile__first_name'),
						Lower('profile__last_name')
					)
			size = len(friends)
		except:
			friends = None
			size = 0
		if mode == 'friends':
			paginator = Paginator(friends, 7)
			page_number = request.GET.get('page')
			page_friends = paginator.get_page(page_number)
			return render(request, 'users/search_results.html', {	'users' : friends,
																	'mode' : mode, 
																	'size' : size,
																	'page_friends' : page_friends,
																})

		return render(request, 'users/search_results.html', {	'users' : friends,
																'mode' : mode, 
																'size' : size
															})


@require_safe
@login_required
def view_all_friends(request):
	if request.user.friends.count() > 0:
		has_friends = True
	else:
		has_friends = False
	return render(request, 'users/view_all_friends.html', { 'has_friends' : has_friends })


@require_safe
@login_required
def notifications(request):
	if request.is_ajax():
		mode = request.GET.get('mode')
		return render(request, 'users/notifications_ajax.html', { 'mode': mode })


@require_safe
@login_required
def unseen_notifications(request):
	if request.is_ajax():
		last = request.GET.get('last')
		if last:
			unseen_notifications = Notifications.objects.filter(to_user=request.user, 
																id__lte=last,
																)
			for n in unseen_notifications:
				if not n.seen:
					n.seen = True
					n.save()
			response = 'success'

		else:
			response = 'failed'
		return JsonResponse({'response' : response })


@require_safe
@login_required
def block_users(request, id, action):
	if request.is_ajax():
		try:
			person = User.objects.get(id=id)
			response = 'success'
		except:
			response = 'failure'
		if action == 'block':
			if person.is_blocked_by.filter(user=request.user).exists():
				messages.warning(request, f'Sorry! @{person.username} is already in Blocked Users')
			else:
				BlockedUsers.block_user(request.user, person)
				messages.info(request, f'@{person.username} has been added to Blocked Users')
		elif action == 'unblock':
			if person.is_blocked_by.filter(user=request.user).exists():
				BlockedUsers.unblock_user(request.user, person)
				messages.info(request, f'@{person.username} has been removed from Blocked Users')
			else:
				messages.warning(request, f'Sorry! @{person.username} is not in Blocked Users')
		return JsonResponse({ 'response' : response })


@require_safe
@login_required
def blocked_users_list(request):
	blocked_users = BlockedUsers.objects.get(user=request.user)
	blocked_users = blocked_users.blocked_list.all()
	return render(request,'users/blocked_users.html', { 'blocked_users' : blocked_users })


@require_safe
@login_required
def delete_user(request):
	request.user.delete()
	messages.success(request, 'Your account has been deleted successfully')
	return redirect('init')


@require_http_methods(["GET", "POST"])
@login_required
def home(request):
	if request.user.profile.first_name:
		if Messages.objects.filter(	Q(sender=request.user)|
									Q(receiver=request.user)
							).exists():
			has_messages = True
		else:
			has_messages = False
		return render(request,'users/home.html', { 'has_messages' : has_messages})
	else:
		return redirect('users-profile')
