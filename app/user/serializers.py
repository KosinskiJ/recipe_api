from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password' : {'write_only' : True, 'min_length' : 5}}

    def create(self, validate_data) :
        """create new user with encrypted password"""
        return get_user_model().objects.create_user(**validate_data)


class AuthTokenSerializer(serializers.Serializer) :
    """Serializer user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type' : 'password'},
        trim_whitespace = False
    )

    def validate(self, attrs) :
        """Validate and auth the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )
        if not user :
            msg = _('Unable to authenticate')
            raise serializers.ValidationError(msg, code = 'authentication')
        attrs['user'] = user
        return attrs
