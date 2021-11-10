from django.urls import path
from main import views

urlpatterns = [
    path("", views.index_page, name="index_page"),
    path("content_create/", views.content_creation, name="content_create"),
    path("content_update/<int:pk>/", views.content_update, name="content_update"),
    path("details/<int:id>/", views.content_detail, name="content_detail"),
    path("delete/<int:number>/", views.content_delete, name="content_delete"),

    path("user/login/", views.login_user),
    path("user/logout/", views.logout_user, ),

]
