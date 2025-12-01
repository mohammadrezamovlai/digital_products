from rest_framework import serializers

from .models import Gateway

class GetawaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('id','title','description','avatar')