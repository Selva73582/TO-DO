


from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home),
    path('login/',views.CustomLogin.as_view(),name="login"),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('TaskList',views.TaskList.as_view(),name="TaskList"),
    path('task/<int:pk>/',views.TaskDetail.as_view(),name="Task-View"),
    path('task-create/',views.TaskCreate.as_view(),name="Task-Create"),
    path('task-edit/<int:pk>/',views.TaskUpdate.as_view(),name="Task-Edit"),
    path('task-delete/<int:pk>/',views.TaskDelete.as_view(),name="Task-Delete"),

]

