from rest_framework import serializers
from .models import Subscription,Package

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id','title','sku','description','avatar','price','duration')


class Subscriptionserailzer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ('package', 'created_time', 'expire_time')