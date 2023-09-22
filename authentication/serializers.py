from rest_framework import serializers
from .models import *


class DepartmentNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentNews
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CoachSerializer(serializers.ModelSerializer):
    user = UserProfile()
    gym = serializers.PrimaryKeyRelatedField(queryset=GymManager.objects.all(), required=False)

    class Meta:
        model = Coach
        fields = '__all__'


class GymManagerSerializer(serializers.ModelSerializer):
    user = UserProfile()
    coaches = serializers.PrimaryKeyRelatedField(queryset=Coach.objects.all(), many=True)

    class Meta:
        model = GymManager
        fields = '__all__'
