from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('ajax/load-projects/', views.load_projects, name='ajax_load_projects'),
    path('Propertyfilter/',views.filter_obj,name='filteroption'),
    path('Propertyfilter/ajax/load-projects/', views.load_projects, name='ajax_load_projects'),
    path('prop_view/<int:pid>', views.prop_view, name='prop_view'),
    path('contactus/', views.abt_us, name='contact_us'),
    path('moreimages/<int:pid>', views.more_img, name='more_img'),
    ]    
