from rest_framework import serializers
from .models import AppUser

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = [
            'username','public_id', 'full_name', 'phone', 'email', 'role',
            'gender', 'birth_date', 'avatar', 'bio', 'about',
            'is_active', 'is_verified', 'last_seen', 'created_at'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = AppUser
        fields = ['username','full_name', 'phone', 'email', 'password', 'gender', 'birth_date']

    def create(self, validated_data):
        user = AppUser(
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            email=validated_data.get('email'),
            gender=validated_data.get('gender'),
            birth_date=validated_data.get('birth_date')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
