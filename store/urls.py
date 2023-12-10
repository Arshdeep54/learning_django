from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter


routers = DefaultRouter()
routers.register("products", views.ProductViewSet)
routers.register("collections", views.CollectionViewSet)

urlpatterns = routers.urls

# u can print routers.urls to see it is same as below

# urlpatterns = [
#     path("products/", views.ProductList.as_view()),
#     path("products/<int:id>/", views.ProductDetails.as_view()),
#     path(
#         "collections/<int:pk>/",
#         views.CollectionDetails.as_view(),
#         name="collection_detail",
#     ),
#     path("collections/", views.CollectionList.as_view()),
# ]
