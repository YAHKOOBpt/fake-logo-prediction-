from django.urls import path
from . import views
urlpatterns = [
    
    # path('predict_logo', views.predict_logo, name='predict_logo'),

    path('register', views.register, name='register'),
    path('', views.login, name='login'),
    path('predict_logo', views.predict_logo, name='predict_logo'),
    path('logoutpage', views.logoutpage, name='logoutpage'),
    path('logout', views.logout, name='logout'),
    path('view_user', views.view_user, name='view_user'),
    path('view_product/<int:pk>/', views.view_product, name='view_product'),
    path('category', views.category, name='category'),
    path('view_prediction', views.view_prediction, name='view_prediction'),
]
