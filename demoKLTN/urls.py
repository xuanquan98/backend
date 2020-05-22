from django.urls import path
from . import views

urlpatterns = [
   path('', views.index),
   path('/getCv',views.listCv),
   path('/login', views.login),
   path('/logout', views.logout),
   path('/deleteCv', views.deleteCv),
   path('/updateCv', views.updateCv)
]