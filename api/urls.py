from django.urls import path
from .views import Tasks, Delete, Update, CompletedTasks, InCompletedTasks, Users

urlpatterns = [
    path('tasks/<int:id>', Tasks.as_view()),
    path('tasks/', Tasks.as_view()),
    path('delete/<int:pk>', Delete.as_view()),
    path('update/<int:pk>', Update.as_view()),
    path('completed', CompletedTasks.as_view()),
    path('incompleted', InCompletedTasks.as_view()),
    path('users', Users.as_view())
]