from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
from .models import Product,File,Category
# from import_export.admin import ImportMixin
# from import_export import resources


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent','title','is_enable','created_time']
    list_filter = ['is_enable','parent']
    search_fields = ['title']


class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ['title','file','is_enable','file_type']
    extra  = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','is_enable','created_time']
    list_filter = ['is_enable']
    search_fields = ['title']
    filter_horizontal = ['categories']
    inlines = [FileInlineAdmin]


# class ProductResource(resources.ModelResource):
#     class Meta:
#         model = Product
#         fields = ('id', 'title', 'is_enable', 'created_time')
#         export_order = ('id', 'title', 'is_enable', 'created_time')


# @admin.register(Product)
# class ProductAdmin(ImportMixin, admin.ModelAdmin):
#     resource_class = ProductResource

#     list_display = ['title','is_enable','created_time']
#     list_filter = ['is_enable']
#     search_fields = ['title']
#     filter_horizontal = ['categories']
#     inlines = [FileInlineAdmin]



