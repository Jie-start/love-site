from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('places/', views.place_list, name='place_list'),
    path('places/create/', views.place_create, name='place_create'),
    path('places/<int:pk>/', views.place_detail, name='place_detail'),
    path('activities/', views.activity_list, name='activity_list'),
    path('wishes/', views.wish_list, name='wish_list'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('relationship/request/', views.relationship_request_create, name='relationship_request_create'),
    path('relationship/requests/', views.relationship_requests, name='relationship_requests'),
    path('relationship/request/<int:request_id>/', views.relationship_request_handle, name='relationship_request_handle'),
    path('activities/create/', views.activity_create, name='activity_create'),
    path('activities/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('wishes/create/', views.wish_create, name='wish_create'),
    path('wishes/<int:pk>/toggle/', views.wish_toggle_status, name='wish_toggle_status'),
] 