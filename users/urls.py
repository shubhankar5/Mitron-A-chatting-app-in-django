from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='users-home'),
    path('notifications/',views.notifications,name='users-notifications'),
    path('profile/',views.my_profile_view,name='users-profile'), 
    path('profile-update/',views.update_profile,name='users-profile-update'),
    path('profile/<int:id>/',views.others_profile_view,name='other-users-profile'), 
    path('search-results/',views.search_results_users,name='search-results-users'),
    path('search-results/keyword=<str:search_text>/',views.search_results_users,name='search-results-users'),
    path('friends/',views.view_all_friends,name='view-all-friends'),
    path('blocked-users-list/',views.blocked_users_list,name='users-blocked-list'),
    path('delete-user/',views.delete_user,name='delete-user'),
    path('ajax/unseen-notifications/',views.unseen_notifications,name='users-notifications-unseen'),  
    path('ajax/search-users/',views.search_users,name='search-users-ajax'),
    path('ajax/profile-picture-update/',views.update_profile_picture,name='users-profile-picture-update'),
    path('ajax/search-friends/',views.search_friends,name='search-friends-ajax'),
    path('ajax/change-friends/',views.change_friends,name='change-friends-ajax'),
    path('ajax/block-user/<int:id>/<str:action>/',views.block_users,name='block-users'),
]