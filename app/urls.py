from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('rooms/', views.room_list, name='rooms'),
    path('delete-room/<int:id>/', views.delete_room, name='delete_room'),
    path('students/', views.student_list, name='student_list'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('my-room/', views.my_room, name='my_room'),
    path('rent-status/', views.rent_status, name='rent_status'),
    path('rent/', views.rent_list, name='rent'),
    path('complaints/', views.student_complaints, name='student_complaints'),
    path('admin-complaints/', views.admin_complaints, name='admin_complaints'),

]