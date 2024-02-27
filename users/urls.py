from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static


app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginview, name='loginview'),
    path('login/process', views.process, name='process'),
    path('logout', views.processlogout, name='processlogout'),
    path('add', views.add, name='add'),
    path('search', views.search, name='search'),
    path('processadd', views.processadd, name='processadd'),
    path('<int:profile_id>/detail/', views.detail, name='detail'),
    path('<int:profile_id>/delete/', views.delete, name='delete'),
    path('<int:profile_id>/edit/', views.edit, name='edit'),
    path('<int:profile_id>/processedit/', views.processedit, name='processedit'),
    path('addcomment', views.addcomment, name='addcomment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.
STATIC_URL, document_root=settings.STATIC_ROOT)
