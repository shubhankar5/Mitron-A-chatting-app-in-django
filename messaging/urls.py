from django.urls import path
from . import views

urlpatterns = [
    path('ajax/message-logs/',views.view_message_logs,name='message-logs'),
    path('ajax/handle-unseen-messages/',views.handle_unseen_messages,name='handle-unseen-messages'),
    path('ajax/handle-message-liking/',views.handle_message_liking,name='handle-message-liking'),
    path('ajax/view-messages/',views.view_messages,name='view-messages'),
    path('ajax/view-typing-box/',views.view_typing_box,name='view-typing-box'),
    path('ajax/send-message/<int:id>/',views.send_message,name='send-message'),
	path('ajax/send-image-message/<int:id>/',views.handle_image_messages,name='send-image'),   
]