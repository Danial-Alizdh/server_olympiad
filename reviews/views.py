from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


# Create your views here.
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CulturalList(generics.ListAPIView):
    queryset = Cultural.objects.all()
    serializer_class = CulturalSerializer


class GalleryList(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class ChampionshipList(generics.ListAPIView):
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class DormitoriesViewSet(viewsets.ModelViewSet):
    queryset = Dormitories.objects.all()
    serializer_class = DormitoriesSerializer


class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class TopResultsViewSet(viewsets.ModelViewSet):
    queryset = TopResults.objects.all()
    serializer_class = TopResultsSerializer


@api_view(['POST'])
def surveyListView(request):
    print(request.data)
    if request.method == 'POST':
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
