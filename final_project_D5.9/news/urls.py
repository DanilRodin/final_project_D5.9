from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView

urlpatterns = [
   path('news/', NewsListView.as_view(template_name="news.html"), name='news'),
   path('<int:pk>', NewDetailView.as_view(), name='new'),
   path('search/', SearchNewsListView.as_view(template_name="search.html"), name='search'),
   path('add/', NewAddCreateView.as_view(), name='new_add'),
   path('edit/<int:pk>', NewUpdateView.as_view(), name='new_edit'),
   path('delete/<int:pk>', NewDeleteView.as_view(), name='new_delete'),
   path('article/create/', NewAddCreateView.as_view(), name='article_create'),
   path('article/<int:pk>/edit', NewUpdateView.as_view(), name='article_edit'),
   path('article/<int:pk>/delete', NewDeleteView.as_view(), name='article_delete'),
   path('login/', LoginView.as_view(template_name="login.html"), name='login'),
   path('user_page/', IndexView.as_view(template_name="user_page.html"), name='user_page'),
   path('logout/user', logout_user, name='logout_user'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subdcribe, name='subscribe'),

]