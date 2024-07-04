from django.contrib import admin
from django.urls import path, include, re_path
from alkitaab import views
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello, World!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.api.urls')),
    path('', hello_world, name='main'),
    re_path('api/signup/', views.signup, name='signup'),
    re_path('api/login/', views.login, name='login'),
    path('api/update_user/', views.update_user, name='update_user'),
    path('api/delete_user/', views.delete_user, name='delete_user'),
    path('api/create_ibadat/', views.create_ibadat, name='create_ibadat'),
    path('api/get_ibadaat/', views.get_ibadaat, name='get_ibadaat'),
    path('api/update_ibadat/<int:id>/', views.update_ibadat, name='update_ibadat'),
    path('api/delete_ibadat/<int:id>/', views.delete_ibadat, name='delete_ibadat'),
    path('api/get_scale/<int:id>/', views.get_scale, name='get_scale'),
    path('api/create_scale/<int:id>/', views.create_scale, name='create_scale'),
    path('api/update_scale/<int:id>/', views.update_scale, name='update_scale'),
    path('api/delete_scale/<int:id>/', views.delete_scale, name='delete_scale'),
    path('api/get_ibadat_item/<int:id>/', views.get_ibadat_item, name='get_ibadat_item'),
    path('api/create_ibadat_item/<int:id>/', views.create_ibadat_item, name='create_ibadat_item'),
    path('api/update_ibadat_item/<int:id>/', views.update_ibadat_item, name='update_ibadat_item'),
    path('api/delete_ibadat_item/<int:id>/', views.delete_ibadat_item, name='delete_ibadat_item'),
]