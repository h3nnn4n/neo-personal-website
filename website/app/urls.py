from django.urls import path

from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("games/", views.GamesView.as_view(), name="games"),
    path("posts/", views.PostView.as_view(), name="posts_index"),
    path("posts/<slug:slug>/", views.PostView.as_view(), name="posts_view"),
    path("tags/", views.TagView.as_view(), name="tags_index"),
    path("tags/<slug:tag>/", views.TagView.as_view(), name="tags_view"),
    path("projects/", views.ProjectsView.as_view(), name="projects_index"),
]
