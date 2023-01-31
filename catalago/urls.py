from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('sobre', views.sobre, name='sobre'),
  path('autores', views.AutorListView.as_view(), name='autores'),
  path('autor/<int:pk>', views.AutorDetailView.as_view(), name='autor_detail'),
  path('livros', views.LivroListView.as_view(), name='livro_list'),
  path('livros/<int:pk>', views.LivroDetailView.as_view(), name='livro_detail'),
  path('review/<int:pk>', views.ReviewDetailView.as_view(), name='review_detail'),
  path('review/create', views.ReviewCreateView.as_view(), name='review_create'),
  path('review/<int:pk>/avaliar/', views.review_avaliar, name='review_avaliar'),
  path('reviews', views.ReviewListView.as_view(), name='review_list'),
  path('review/<int:pk>/delete', views.ReviewDeleteView.as_view(), name='review_delete'),
  path('autor/<int:pk>/delete', views.AutorDeleteView.as_view(), name='autor_delete'),
]