from django.urls import path

from . import views

app_name = 'ship'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('<int:shipid>/logout/', views.logout, name='logout'),
    path('<int:shipid>/logoutAnimate/', views.logoutAnimate, name='logoutAnimate'),
    path('<int:shipid>/finalize/', views.finalize, name='finalize'),
    path('<int:userid>/manifest/', views.manifest, name='manifest'),
    path('<int:userid>/upload/', views.upload, name='upload'),
    path('<int:userid>/<int:shipid>/transaction/', views.transaction, name='transaction'),
    path('<int:userid>/<int:shipid>/load/', views.load, name='load'),
    path('<int:userid>/<int:shipid>/animate/', views.animate, name='animate'),
    path('<int:userid>/log-entry/', views.log, name='log'),
]