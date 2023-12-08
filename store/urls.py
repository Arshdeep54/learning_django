from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list),
    path("products/<int:id>/", views.product_details),
    path("cllections/<int:pk>/", views.collection_details, name="collection_detail"),
]
