# from rest_framework import serializers
# from .models import User


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=6)

#     class Meta:
#         model = User
#         fields = ['username','full_name', 'phone', 'email', 'password', 'gender', 'birth_date']

#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username'],
#             full_name=validated_data['full_name'],
#             phone=validated_data['phone'],
#             email=validated_data.get('email'),
#             gender=validated_data.get('gender'),
#             birth_date=validated_data.get('birth_date')
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
from rest_framework import serializers
from .models import User
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'password',  'date_joined']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email'),
            # فرض کردیم gender و date_joined هم میخوای
        )
        user.set_password(validated_data['password'])
        user.save()
        return user