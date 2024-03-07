from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path('login/', views.login_view, name='login_view'),
    path('user_profile/', views.view_employee, name='info'),
    path('todo/', views.todo, name='todo'),
    path('add_achievements/', views.add_achievements, name='achieve'),
    path('add_workhistory/', views.add_workhistory, name='history'),
    path('add_skills/', views.add_skills, name='skills'),
    path('project_login/', views.project_login, name='project_login'),
    path('collab/', views.collab, name='collab'),
    path('kanban/', views.kanban_board, name='kanban'),
    path('empdir/', views.employee_dir, name='dir'),
    path('sign/', views.register, name="signup"),
    path('note/view/', views.note_list, name='note_list'),
    path('note/create/', views.note_create, name='note_create'),
    path('note/view/delete/<str:notename>/', views.note_delete, name='note_delete'),
]