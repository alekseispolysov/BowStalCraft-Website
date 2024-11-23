from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.urls import path
from . import views
from django.urls import path, include

app_name = 'forum'

# All urls routes for forum application
# We can see forum page, create post, update post, delete post, view details of post, search for post, comment, edit delete comment, ajax for post reputation

urlpatterns = [
	path('', views.ForumIndexPage.as_view(), name="forum-index-page"),
	path('create/', views.CreateForumPost.as_view(), name="forum-create-post"),
	path('update/<str:pk>/', views.UpdateForumPost.as_view(), name="forum-update-post"),
	path('delete/<str:pk>/', views.DeleteForumPost.as_view(), name="forum-delete-post"),
	path('post/<str:pk>/', views.DetailForumPage.as_view(), name='forum-detail-page'),
	path('search/', views.fullSearch.as_view(), name='forum-search'),
	path('comment/edit/<str:pk>/', views.EditCommentToPost.as_view(), name='forum-edit-comment-post'),
	path('comment/delete/<str:pk>/', views.DeleteCommentToPost.as_view(), name='forum-delete-comment-post'),
	path('post/<str:pk>/ajax/', views.DetailForumPostPageAjax.as_view()),
]


