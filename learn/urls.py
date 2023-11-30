from django.urls import path,include
from . import views 
from .views import CustomLoginView


urlpatterns=[
    path('',views.index, name='index'),
    path('login/',CustomLoginView.as_view(), name='signin'),
    # path('dashboard/',views.dashboard, name='dashboard'),
    path('create_item/', views.create_item, name='create_item'),
    path('create_record/', views.create_record, name='create_record'),
    path('',include('django.contrib.auth.urls')),

    # path('register/', views.register, name='register'),
    # path('edit/', views.edit, name='edit'),
    
    # path('members/<name>/',views.memberProfile, name='detail'),
    # path('edit_member/<int:member_id>/', views.edit_member, name='update_member'),
    # path('remove_member/<int:member_id>/', views.remove_member, name='remove_member'),

    path('record/', views.records, name='record'),
    path('get_items_for_unit/', views.get_items_for_unit, name='get_items_for_unit'),
    path('list/', views.items_list, name='list'),
    path('report/', views.reports, name='report'),
    path('item_report/', views.item_report, name='item_report'),
    path('record_report/', views.record_report, name='record_report'),
    path('worth/', views.worth, name='worth'),

    path('item_pdf/', views.item_pdf, name='item_pdf'),

    path('record_pdf/', views.record_pdf, name='record_pdf'),

]
