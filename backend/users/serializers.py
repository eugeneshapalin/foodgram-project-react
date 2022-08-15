from djoser.serializers import UserSerializer
from rest_framework import serializers

from api.models import Subscription
from users.models import User


class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',
                  'username',
                  'first_name',
                  'last_name',
                  'password'
                  )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CurrentCustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()
