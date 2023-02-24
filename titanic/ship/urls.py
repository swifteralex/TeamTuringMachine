from django.urls import path

from . import views

app_name = 'ship'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('<int:userid>/manifest/', views.manifest, name='manifest'),
    path('<int:userid>/upload/', views.upload, name='upload'),
    path('<int:userid>/<int:shipid>/transaction/', views.transaction, name='transaction'),
    path('<int:userid>/<int:shipid>/load/', views.load, name='load'),
    path('<int:userid>/<int:shipid>/unload/', views.unload, name='unload'),
    path('<int:userid>/<int:shipid>/balance/', views.balance, name='balance'),
]