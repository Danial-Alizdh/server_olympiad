from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('get_department_news/', get_department_news, name='get_department_news'),
    path('get_department_office/', get_department_office, name='get_department_office'),
    path('get_department_game/', get_department_game, name='get_department_game'),
    path('get_department_classroom/', get_department_classroom, name='get_department_classroom'),
    path('get_department_board/', get_department_board, name='get_department_board'),
    path('add_element/', add_element, name='add_element'),
    path('add_to_class/', add_to_class, name='add_to_class'),
    path('get_all_class/', get_all_class, name='get_all_class'),
    path('accept_for_classroom/', accept_for_classroom, name='accept_for_classroom'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('main_page/', main_page, name='main_page'),
    path('update_profile/', update_profile, name='update_profile'),
    path('accept_role/', accept_role, name='accept_role'),
    path('get_users_by_role/', get_users_by_role, name='get_users_by_role'),
    path('user_information/', user_information, name='user_information'),
    path('add_coach_to_gym/', add_coach_to_gym, name='add_coach_to_gym'),
    path('change_rate/', change_rate, name='change_rate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL_APP2, document_root=settings.MEDIA_ROOT_APP2)