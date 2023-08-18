from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from reviews import views

router = routers.DefaultRouter()
router.register(r'news_items', views.NewsViewSet)
router.register(r'cultural_items', views.CulturalViewSet)
router.register(r'gallery_items', views.GalleryViewSet)
router.register(r'results_items', views.ResultViewSet)
router.register(r'games_items', views.GameViewSet)
router.register(r'dormitories_items', views.DormitoriesViewSet)
router.register(r'gyms_items', views.GymViewSet)
router.register(r'timing_competitions_items', views.CompetitionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    path('', include(router.urls)),

    path('add-survey/', views.surveyListView),
]
