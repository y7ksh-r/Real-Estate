from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home),
    path('ajax/load-projects/', views.load_projects, name='ajax_load_projects'),
    path('Propertyfilter/',views.filter_obj,name='filteroption'),
    path('Propertyfilter/ajax/load-projects/', views.load_projects, name='ajax_load_projects'),
    path('prop_view/<int:pid>', views.prop_view, name='prop_view'),
    path('contactus', views.abt_us, name='contact_us'),
    path('moreimages/<int:pid>', views.more_img, name='more_img'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('contact', views.contact, name='contact_us'),
    path('about', views.about, name='contact_us'),
    path('services', views.services, name='contact_us'),
    path('special_filter/<int:fid>', views.special_page_filter, name='special_page_filter'),
    path('otp/', views.otp_verification, name='otp_verification'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    ]    
