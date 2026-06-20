from django.urls import path 
from . import views 


urlpatterns = [  
    path("", views.task_list, name="tasks-list"), 
    path("create/", views.task_create, name="create-task"), 
    path("update/<int:id>/", views.task_update, name="update-task"),
    path("delete/<int:id>/", views.task_delete, name="task-delete"),
]