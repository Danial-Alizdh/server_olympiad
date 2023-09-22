from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('get_department_news/', get_department_news, name='get_department_news'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('main_page/', main_page, name='main_page'),
    path('update_profile/', update_profile, name='update_profile'),
    # path('change_user_role/', change_user_role, name='change_user_role'),
    path('accept_role/', accept_role, name='accept_role'),
    path('get_users_by_role/', get_users_by_role, name='get_users_by_role'),
    path('user_information/', user_information, name='user_information'),
    path('add_coach_to_gym/', add_coach_to_gym, name='add_coach_to_gym'),
    path('change_rate/', change_rate, name='change_rate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL_APP2, document_root=settings.MEDIA_ROOT_APP2)