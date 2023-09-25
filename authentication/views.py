from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
import uuid
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth.hashers import check_password


@api_view(['GET'])
def get_department_news(request):
    news = DepartmentNews.objects.all()

    if news.count() == 0:
        return JsonResponse({'message': 'خبری وجود ندارد'}, status=status.HTTP_200_OK)

    special_roles = ['office_admin', 'office_manager', 'office_expert', 'board_admin', 'board_authorities']

    flag = False
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)
    if auth_header:
        user = UserProfile.objects.get(login_token=auth_header)
        if user and (user.email == ADMIN_EMAIL or user.role in special_roles):
            flag = True
    response_data = {'news': [n.to_dict() for n in news], 'addNews': flag}
    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)


def generate_login_token():
    return str(uuid.uuid4())


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            if 'image_profile' not in request.data or request.data['image_profile'] is None:
                serializer.validated_data['image_profile'] = None

            hashed_password = make_password(request.data.get('password'))
            serializer.validated_data['password'] = hashed_password

            login_token = generate_login_token()
            serializer.validated_data['login_token'] = login_token
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                'message': f'User {email} signed up successfully',
                'login_token': login_token
            }
            response = JsonResponse(data, safe=False, status=status.HTTP_201_CREATED)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return Response({'message': 'آدرس ایمیل وحود ندارد، لطفا ثبت نام کنید.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if check_password(password, user.password):
            user.login_token = generate_login_token()
            user.save()

            data = {
                'username': user.username,
                'login_token': user.login_token,
            }
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'آدرس ایمیل با گذرواژه هم‌خوانی ندارد.'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def logout(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token or token == 'null':
        return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = UserProfile.objects.get(login_token=token)
        user.login_token = None
        return Response({'message': 'از حساب خارج شدید'}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def profile(request):
    if request.method == "POST":
        token = request.data['login_token']
        if not token or token == 'null':
            return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(login_token=token)
        except UserProfile.DoesNotExist:
            return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = user.to_dict()
        if user.role == 'coach':
            data = Coach.objects.filter(user=user).first().to_dict()
        elif user.role == 'gym_manager':
            data = GymManager.objects.filter(user=user).first().to_dict()
            data['coaches'] = [c.to_dict() for c in Coach.objects.filter(gym=GymManager.objects.get(user=UserProfile.objects.get(email=data['email'])))]
        elif user.role == 'actor':
            data = Actor.objects.filter(user=user).first().to_dict()

        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def main_page(request):
    if request.method == "POST":
        token = request.data['login_token']
        if not token or token == 'null':
            return JsonResponse({'message': 'لطفا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(login_token=token)
            data = {
                'username': user.username,
                'admin': user.email == ADMIN_EMAIL,
            }
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return JsonResponse({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @api_view(['POST'])
# def update_profile(request):
#     if request.method == 'POST':
#         token = request.data['login_token']
#         if not token or token == 'null':
#             return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         try:
#             user = UserProfile.objects.get(login_token=token)
#         except UserProfile.DoesNotExist:
#             return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         # if 'image_profile' in request.data and request.data['image_profile'] is not None:
#         #     user.image_profile = request.data['image_profile']
#         #
#         # if 'image' in request.data and request.data['image'] is not None:
#         #     user.image = request.data['image']
#         #
#         # user.username = request.data['username']
#         user.save()
#         data = {
#             'username': user.username,
#         }
#         return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
#
#     return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_profile(request):
    if request.method == "POST":
        token = request.data['login_token']
        if not token or token == 'null':
            return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(login_token=token)
        except UserProfile.DoesNotExist:
            return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

        role = request.data['role']

        if 'image_profile' in request.data and request.data['image_profile'] is not None and request.data['image_profile'] != 'null':
            user.image_profile = request.data['image_profile']

        user.username = request.data['username']
        user.bio = request.data['bio']
        user.role = role

        if role == 'coach':
            coach, created = Coach.objects.get_or_create(user=user)
            if 'document_image' in request.data and request.data['document_image'] is not None:
                coach.document_image = request.data['document_image']
            if 'education' in request.data:
                coach.education = request.data['education']
            if 'fields' in request.data:
                coach.fields = request.data['fields']
            if 'gym' in request.data:
                coach.gym = GymManager.objects.filter(user=UserProfile.objects.filter(email=request.data['gym']).first()).first()
            coach.save()
        elif role == 'gym_manager':
            gym_manager, created = GymManager.objects.get_or_create(user=user)
            if 'name' in request.data:
                gym_manager.name = request.data['name']
            if 'document_image' in request.data and request.data['document_image'] is not None:
                gym_manager.document_image = request.data['document_image']
            if 'image' in request.data and request.data['image'] is not None:
                print('fffffffffff' + str(request.data['image']))
                gym_manager.image = request.data['image']
            if 'location' in request.data:
                gym_manager.location = request.data['location']
            if 'location_link' in request.data:
                gym_manager.location_link = request.data['location_link']
            if 'possibilities' in request.data:
                gym_manager.possibilities = request.data['possibilities']
            gym_manager.save()
        elif role == 'actor':
            actor, created = Actor.objects.get_or_create(user=user)
            if 'field' in request.data:
                actor.field = request.data['field']
            if 'document_image' in request.data and request.data['document_image'] is not None:
                actor.document_image = request.data['document_image']
            actor.save()

        user.save()
        return JsonResponse({'username': user.username}, status=status.HTTP_200_OK)

    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def accept_role(request):
    if request.method == "POST":
        token = request.data['login_token']
        if not token or token == 'null':
            return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(login_token=token)
        except UserProfile.DoesNotExist:
            return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.email != ADMIN_EMAIL:
            return JsonResponse({'message': 'تنها ادمین حق استفاده از این ویژگی را دارد.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = UserProfile.objects.get(email=request.data['user_email'])
        except UserProfile.DoesNotExist:
            return JsonResponse({'message': 'کاربری با این آدرس ایمیل یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the user's role
        accepted = False if request.data['accepted'] == 'false' else True
        user.accepted = accepted
        user.rejected = not accepted
        user.save()

        return JsonResponse({'message': 'نقش با موفقیت تغییر یافت.'}, status=status.HTTP_200_OK)

    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def get_users_by_role(request):
    if request.method == "POST":
        # token = request.data['login_token']
        # if not token or token == 'null':
        #     return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)
        #
        # try:
        #     user = UserProfile.objects.get(login_token=token)
        # except UserProfile.DoesNotExist:
        #     return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

        # if user.email != ADMIN_EMAIL:
        #     return JsonResponse({'message': 'تنها ادمین حق استفاده از این ویژگی را دارد.'}, status=status.HTTP_403_FORBIDDEN)

        role = request.data['role']

        if role not in dict(UserProfile.USER_ROLES).keys():
            return JsonResponse({'message': 'نقش شما یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)

        data = None
        if role == 'coach':
            data = Coach.objects.all()
        elif role == 'gym_manager':
            data = GymManager.objects.all()
        elif role == 'actor':
            data = Actor.objects.all()

        if data is None or data.count() == 0:
            return JsonResponse({}, safe=False, status=status.HTTP_204_NO_CONTENT)

        response_data = {'data': [d.to_dict() for d in data]}
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

        # users = UserProfile.objects.filter(role=role)
        # user_data = [{'username': user.username, 'email': user.email} for user in users]
        #
        # return JsonResponse({'users': user_data}, status=status.HTTP_200_OK)

    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def user_information(request):
    if request.method == "POST":
        token = request.data['login_token']
        if not token or token == 'null':
            return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(login_token=token)
        except UserProfile.DoesNotExist:
            return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(email=request.data['user_email'])
            data = user
            if user.role == 'coach':
                data = Coach.objects.filter(user=user).first()
            elif user.role == 'gym_manager':
                data = GymManager.objects.filter(user=user).first()
            elif user.role == 'actor':
                data = Actor.objects.filter(user=user).first()

            if data is None or data.count() == 0:
                return JsonResponse({}, safe=False, status=status.HTTP_204_NO_CONTENT)

            return JsonResponse(data.to_dict(), safe=False, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'message': 'چنین کاربری یافت نشد.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def add_coach_to_gym(request):
    if request.method == "POST":
        token = request.data['login_token']
        if not token or token == 'null':
            return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(login_token=token)
        except UserProfile.DoesNotExist:
            return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            coach = UserProfile.objects.get(email=request.data['coach_email'])
            if coach.role == 'coach':
                try:
                    gym_manager = GymManager.objects.get(name=request.data['gym_name'])
                    gym_manager.coaches.add(coach)
                    gym_manager.save()
                    return Response({'message': 'مربی به باشگاه اضافه شد.'}, status=status.HTTP_200_OK)
                except GymManager.DoesNotExist:
                    return Response({'message': 'باشگاهی با این نام یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'نقش شما مربی ورزشی نیست.'}, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return Response({'message': 'مربی‌ای با این آدرس ایمیل یافت نشد.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def change_rate(request):
    if request.method == "POST":
        token = request.data['login_token']
        if not token or token == 'null':
            return JsonResponse({'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(login_token=token)
        except UserProfile.DoesNotExist:
            return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserProfile.objects.get(email=request.data['user_email'])
            user.update_average_rating(request.data['rate'])

            return JsonResponse({'message': 'امتیاز با موفقیت ثبت شد.'}, safe=False, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'message': 'چنین کاربری یافت نشد.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'درخواست اشتباه'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
