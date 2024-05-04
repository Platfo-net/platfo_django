from rest_framework import serializers

from utilities.validators import validate_password
from .models import User


class UserRegisterByPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'phone_number', 'phone_country_code')

    def validate(self, attrs):
        existing_user = User.objects.existing(
            phone_number=attrs['phone_number'],
            phone_country_code=attrs['phone_country_code'],
        ).first()

        if not validate_password(attrs['password']):
            raise serializers.ValidationError('Your password is not acceptable')

        if existing_user and existing_user.is_active:
            raise serializers.ValidationError('User with this phone number already exists.')

        if existing_user and not existing_user.is_active:
            raise serializers.ValidationError('User with this phone number is inactive.')

        return attrs
