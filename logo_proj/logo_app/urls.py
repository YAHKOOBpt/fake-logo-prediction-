from django.urls import path
from . import views
urlpatterns = [
    
    path('predict', views.predict_logo, name='predict_logo'),

    path('register', views.register, name='register'),
    path('', views.login, name='login'),
    path('logo', views.logo, name='logo'),
    path('logoutpage', views.logoutpage, name='logoutpage'),
]
