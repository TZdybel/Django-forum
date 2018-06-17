from django.urls import path
from django.contrib.auth import views as authviews
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', authviews.login, {'template_name': 'forum/login.html'}, name='login'),
    path('logout/', authviews.logout, {'template_name': 'forum/logout.html'}, name='logout'),
    path('addthread/', views.add_thread, name='add_thread'),
    path('profile/<str:username>/', views.see_profile, name='see_profile'),
    path('profile/<str:username>/userdelete', views.user_delete, name='user_delete'),
    path('profile/<str:username>/profileupdate/', views.profile_update, name='profile_update'),
    path('profile/<str:username>/passwdchange/', views.password_change, name='password_change'),
    path('<str:category>/', views.threadlist, name='threadlist'),
    path('<str:category>/<int:threadID>/', views.thread_details, name='thread_details'),
    path('<str:category>/<int:threadID>/answer', views.answer, name='answer'),
    path('<str:category>/<int:threadID>/deletethread', views.thread_delete, name='thread_delete'),
    path('<str:category>/<int:threadID>/<int:postID>/deletepost', views.post_delete, name='delete_post')
]
