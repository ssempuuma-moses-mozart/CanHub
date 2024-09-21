
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("n/index", views.index, name="index"),
    path("n/login", views.login_view, name="login"),
    path("n/my_donations/<int:item_id>/", views.my_donations_view, name="my_donations"),
    path("n/campaigns/<int:item_id>/", views.campaigns_view, name="campaigns"),
    path("n/dashboad/", views.dashboad_view, name="dashboad_no_item"),
    path("n/dashboad/<int:item_id>/", views.dashboad_view, name="dashboad"),
    path("n/logout", views.logout_view, name="logout"),
    path("n/user_logout", views.user_logout_view, name="user_logout"),
    path("n/register", views.register, name="register"),
    path('upload/', views.upload_post, name='upload_post'),
    path('user-profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle-like'),
    path('submit-comment/<int:post_id>/', views.submit_comment, name='submit_comment'),

    path('my-network/', views.my_network_view, name='my_network'),

    path('groups/', views.groups_view, name='groups'),
    path('groups/<int:id>/', views.group_detail_view, name='group_detail'),  # New URL pattern
    path('notifications/', views.notifications_view, name='notifications'),

    path('like_group/<int:post_id>/', views.toggle_like_group, name='toggle-like-group'),

    path('messaging/', views.messaging_view, name='messaging'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),

    path('group-comment/<int:post_id>/', views.group_comment, name='group_comment'),


    
    


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

