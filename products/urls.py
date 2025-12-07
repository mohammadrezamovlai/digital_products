# from .views import ProductListView,CategoryListView,FileListView
# from django.urls import path
# app_name = 'products'
# urlpatterns = [
#     path('products/',ProductListView.as_view({'get':'list','post':'create'}),name='product-list'),
#     path('products/<int:pk>',ProductListView.as_view({'get':'retrieve','put': 'update','patch': 'partial_update', 'delete': 'destroy' }),name='product-detail'),
#     path('categories/',CategoryListView.as_view({'get':'list','post':'create'}),name='category-list'),
#     path('categories/<int:pk>',CategoryListView.as_view({'get':'retrieve','put': 'update','patch': 'partial_update', 'delete': 'destroy'}),name='category-detail'),
#     path('products/<int:product_id>/files/',FileListView.as_view({'get':'list','post':'create'}),name='file-list'),
#     path('files/<int:pk>',FileListView.as_view({'get':'retrieve','put': 'update','patch': 'partial_update', 'delete': 'destroy', }),name='file-detail'),
# ]
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, FileViewSet
from django.urls import path, include

app_name = 'products'

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
]
