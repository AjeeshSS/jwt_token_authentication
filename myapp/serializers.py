from rest_framework import serializers
import re
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    
class RegistrationUserSerializer(serializers.ModelSerializer):
    """Serializer for registration."""
    
    confirm_password = serializers.CharField(max_length=20, write_only=True)
    avatar = serializers.ImageField(max_length=None, allow_empty_file=
                                    False, use_url=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'email','first_name', 'last_name', 'mobile', 'date_of_birth', 'avatar', 'password', 'confirm_password']
        read_only_fields = ['id']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        validation_error = {}

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$', attrs.get('password')):
            validation_error['password'] = 'Enter a valid value for password'

        # if attrs.get('password') != attrs.get('confirm_password'):
        #     validation_error['confirm_password'] = 'Passwords do not match'

        if not re.match(r"^[a-zA-Z]{1}[a-zA-Z0-9\s]+$", attrs.get('first_name')):
            validation_error['first_name'] = 'Enter a valid value for username'

        if len(str(attrs.get('mobile'))) != 10:
            validation_error['mobile'] = 'Enter a valid mobile. This value may contain 10 length.'

        if not re.match("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})$", attrs.get('email')):
            validation_error['email'] = 'Enter a valid email.'

        if validation_error:
            raise serializers.ValidationError(validation_error)

        return attrs

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        if validated_data['password'] != confirm_password:
            raise serializers.ValidationError('Passwords do not match')
        
        customer = User.objects.create_user(**validated_data)
        customer.save()
        return customer
    