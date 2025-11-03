from .views import ProductListView,CategoryListView,FileListView
from django.urls import path

urlpatterns = [
    path('products/',ProductListView.as_view({'get':'list','post':'create'}),name='product-list'),
    path('products/<int:pk>',ProductListView.as_view({'get':'retrieve','put': 'update','patch': 'partial_update', 'delete': 'destroy' }),name='product-detail'),
    path('categories/',CategoryListView.as_view({'get':'list','post':'create'}),name='category-list'),
    path('categories/<int:pk>',CategoryListView.as_view({'get':'retrieve','put': 'update','patch': 'partial_update', 'delete': 'destroy'}),name='category-detail'),
    path('products/<int:product_id>/files/',FileListView.as_view({'get':'list','post':'create'}),name='file-list'),
    path('files/<int:pk>',FileListView.as_view({'get':'retrieve','put': 'update','patch': 'partial_update', 'delete': 'destroy', }),name='file-detail'),
]