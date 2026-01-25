from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path("", views.DishListView.as_view(), name="dish_list"),
    path("<int:pk>/", views.DishDetailView.as_view(), name="dish_detail"),
]