from django.conf import settings
from rest_framework import serializers

from utilities import s3_storage
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

        if existing_user and not existing_user.is_active:
            raise serializers.ValidationError('User with this phone number is inactive.')

        return attrs

    def create(self, validated_data):
        validated_data['username'] = f"{validated_data['first_name']}_{validated_data['last_name']}"
        return User.objects.create_user(**validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'profile_image')


class UpdateUserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'uuid', 'username', 'first_name', 'last_name',
            'email', 'is_active', 'phone_number', 'phone_country_code',
            'created_at', 'updated_at',
            'profile_image',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile_image'] = s3_storage.get_file_url(instance.profile_image,
                                                                  settings.S3_USER_PROFILE_BUCKET)
        return representation


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        password = attrs['password']
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this phone number does not exist.')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password.')
        attrs['user'] = user
        return attrs
