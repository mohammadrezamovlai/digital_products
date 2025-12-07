# from rest_framework import serializers

# from .models import Category,File,Product


# class CategorySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id','title','description','avatar','url')


# class FileSerializer(serializers.HyperlinkedModelSerializer):
#     file_type = serializers.SerializerMethodField()
#     class Meta:
#         model = File
#         fields = ('id','title','file','file_type','url')
#     def get_file_type(self,obj):
#         return obj.get_file_type_display()


# class ProductSerializer(serializers.HyperlinkedModelSerializer):
#     categories = CategorySerializer(many=True)
#     files = FileSerializer(many=True)
#     extra = serializers.SerializerMethodField()
#     class Meta:
#         model = Product
#         fields = ('id','title','description','avatar','categories','files','extra','url')
#     def get_extra(self,obj):
#         return "im mohammadreza movali "
from rest_framework import serializers
from .models import Category, File, Product

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'avatar', 'url')
        extra_kwargs = {
            'url': {'view_name': 'products:category-detail'}
        }

class FileSerializer(serializers.HyperlinkedModelSerializer):
    file_type = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = ('id', 'title', 'file', 'file_type', 'url')
        extra_kwargs = {
            'url': {'view_name': 'products:file-detail'}
        }

    def get_file_type(self, obj):
        return obj.get_file_type_display()

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    extra = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'avatar', 'categories', 'files', 'extra', 'url')
        extra_kwargs = {
            'url': {'view_name': 'products:product-detail'}
        }

    def get_extra(self, obj):
        return "im mohammadreza movali"
