from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home_page_view, name='home'),
    path('reviews/', views.reviews_list),
    path('reviews/<int:id>/', views.review_detail),
]