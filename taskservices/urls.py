from . import views
from django.urls import path ,include
from .views import mark_notification_as_read


urlpatterns=[path('services/filter/<int:service_id>/', views.taskfilter_view, name='filters'),
 path('book/<int:tasker_id>/<int:service_id>/', views.book_service, name='book_service'),
 # path('notifications/', views.notifications_view, name='notifications_view'),
 path('notifications/mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),


]

