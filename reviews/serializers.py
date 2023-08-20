from rest_framework_json_api import serializers
from .models import *


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'image', 'date', 'link')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)


class CulturalSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Cultural
        fields = ('id', 'title', 'images')


class GallerySerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Gallery
        fields = ('id', 'title', 'images')


class ChampionshipSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Championship
        fields = ('id', 'title', 'images')


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'game_id', 'title', 'file_title', 'file_link', 'attention', 'city', 'rate', 'athlete_full_name')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'image')


class DormitoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dormitories
        fields = ('id', 'name', 'description', 'direction_link', 'image')


class GymSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gym
        fields = ('id', 'name', 'description', 'direction_link', 'image')


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'game_id', 'file_title', 'file_link', 'attention', 'description', 'date', 'start_time', 'end_time', 'city')


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'name', 'email', 'context')