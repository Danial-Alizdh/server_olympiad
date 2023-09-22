from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from reviews import views
from reviews.views import *

router = routers.DefaultRouter()
router.register(r'news_items', views.NewsViewSet)
router.register(r'results_items', views.ResultViewSet)
router.register(r'games_items', views.GameViewSet)
router.register(r'dormitories_items', views.DormitoriesViewSet)
router.register(r'gyms_items', views.GymViewSet)
router.register(r'timing_competitions_items', views.CompetitionViewSet)
router.register(r'top_results', views.TopResultsViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('add-survey/', views.surveyListView),

    path('gallery_items/', GalleryList.as_view(), name='gallery-list'),

    path('cultural_items/', CulturalList.as_view(), name='cultural-list'),

    path('championship_items/', ChampionshipList.as_view(), name='championship-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL_APP1, document_root=settings.MEDIA_ROOT_APP1)