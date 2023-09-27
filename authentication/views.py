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

    special_roles = ['office_admin', 'office_manager', 'office_expert', 'board_admin', 'board_authorities']

    flag = False
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)
    if auth_header:
        user = UserProfile.objects.get(login_token=auth_header)
        if user and (user.email == ADMIN_EMAIL or user.role in special_roles):
            flag = True

    if news.count() == 0:
        return JsonResponse({'message': 'خبری وجود ندارد', 'addNews': flag}, status=status.HTTP_200_OK)

    response_data = {'news': [n.to_dict() for n in news], 'addNews': flag}
    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_department_office(request):
    office = Office.objects.all()

    if office.count() == 0:
        return JsonResponse({'message': 'اداره‌ای وجود ندارد'}, status=status.HTTP_200_OK)

    response_data = {'office': [n.to_dict() for n in office]}
    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_department_game(request):
    game = BoardGame.objects.all()

    special_roles = ['board_admin', 'board_authorities']

    flag = False
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)
    if auth_header:
        user = UserProfile.objects.get(login_token=auth_header)
        if user and (user.email == ADMIN_EMAIL or user.role in special_roles):
            flag = True

    if game.count() == 0:
        return JsonResponse({'message': 'بازی‌ای وجود ندارد', 'addGame': flag}, status=status.HTTP_200_OK)

    response_data = {'game': [n.to_dict() for n in game], 'addGame': flag}
    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_department_classroom(request):
    classroom = Classroom.objects.all()

    special_roles = ['board_admin', 'board_authorities']

    flag = False
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)
    if auth_header:
        user = UserProfile.objects.get(login_token=auth_header)
        if user and (user.email == ADMIN_EMAIL or user.role in special_roles):
            flag = True

    if classroom.count() == 0:
        return JsonResponse({'message': 'کلاسی وجود ندارد', 'addClassroom': flag}, status=status.HTTP_200_OK)

    response_data = {'classroom': [n.to_dict() for n in classroom], 'addClassroom': flag}
    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_department_board(request):
    board = Board.objects.all()

    if board.count() == 0:
        return JsonResponse({'message': 'هیئتی وجود ندارد'}, status=status.HTTP_200_OK)

    response_data = {'board': [n.to_dict() for n in board]}
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
            try:
                data['coaches'] = [c.to_dict() for c in Coach.objects.filter(gym=GymManager.objects.get(user=UserProfile.objects.get(email=data['email'])))]
            except UserProfile.DoesNotExist:
                print('Nothing')
        elif user.role == 'actor':
            data = Actor.objects.filter(user=user).first().to_dict()
        elif user.role == 'office_admin':
            data = Office.objects.filter(user=user).first().to_dict()
            try:
                data['manager'] = [c.to_dict() for c in OfficeAuthorities.objects.filter(user=UserProfile.objects.get(role='office_manager'), office=Office.objects.get(user=UserProfile.objects.get(email=data['email'])))]
            except UserProfile.DoesNotExist:
                print('Nothin')
            try:
                data['expert'] = [c.to_dict() for c in OfficeAuthorities.objects.filter(user=UserProfile.objects.get(role='office_expert'), office=Office.objects.get(user=UserProfile.objects.get(email=data['email'])))]
            except UserProfile.DoesNotExist:
                print('Nothing')
        elif user.role == 'board_admin':
            data = Board.objects.filter(user=user).first().to_dict()
            try:
                data['auth'] = [c.to_dict() for c in BoardAuthorities.objects.filter(board=Board.objects.get(user=UserProfile.objects.get(email=data['email'])))]
            except UserProfile.DoesNotExist:
                print('Nothing')
            try:
                data['classroom'] = [c.to_dict() for c in JoinedClass.objects.filter(classroom=Classroom.objects.get(board=Board.objects.get(user=user))).all()]
            except UserProfile.DoesNotExist:
                print('Nothing')

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
        user.phone_number = request.data['phone_number']
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
        elif role == 'office_admin':
            office, created = Office.objects.get_or_create(user=user)
            if 'name' in request.data:
                office.name = request.data['name']
            if 'location' in request.data:
                office.location = request.data['location']
            office.save()
        elif role == 'office_manager' or role == 'office_expert':
            office_auth, created = OfficeAuthorities.objects.get_or_create(user=user)
            if 'office' in request.data:
                office_auth.office = Office.objects.filter(user=UserProfile.objects.filter(email=request.data['office']).first()).first()
            office_auth.save()
        elif role == 'board_admin':
            board, created = Board.objects.get_or_create(user=user)
            if 'name' in request.data:
                board.name = request.data['name']
            if 'goal' in request.data:
                board.goal = request.data['goal']
            if 'location' in request.data:
                board.location = request.data['location']
            board.save()
        elif role == 'board_authorities':
            board_auth, created = BoardAuthorities.objects.get_or_create(user=user)
            if 'board' in request.data:
                board_auth.board = Board.objects.filter(user=UserProfile.objects.filter(email=request.data['board']).first()).first()
            board_auth.save()

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

        if user.email != ADMIN_EMAIL and user.role != 'office_admin' and user.role != 'board_admin':
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
        elif role == 'office_admin':
            data = Office.objects.all()
        elif role == 'office_auth':
            data = OfficeAuthorities.objects.all()
        elif role == 'board_admin':
            data = Board.objects.all()
        elif role == 'board_auth':
            data = BoardAuthorities.objects.all()

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


@api_view(['POST'])
def add_element(request):
    if request.method == 'POST':
        if request.data['type'] == 'news':
            serializer = DepartmentNewsSerializer(data=request.data)
            if serializer.is_valid():
                if 'image' not in request.data or request.data['image'] is None:
                    serializer.validated_data['image'] = None
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data['type'] == 'game':
            serializer = BoardGameSerializer(data=request.data)
            if serializer.is_valid():
                if 'image' not in request.data or request.data['image'] is None:
                    serializer.validated_data['image'] = None

                try:
                    user = UserProfile.objects.get(login_token=request.data['login_token'])
                    if user.role == 'board_admin':
                        serializer.validated_data['board'] = Board.objects.get(user=user)
                    elif user.role == 'board_authorities':
                        serializer.validated_data['board'] = Board.objects.get(user=UserProfile.objects.get(email=BoardAuthorities.objects.get(user=user).to_dict()['board']['email']))
                except UserProfile.DoesNotExist:
                    return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data['type'] == 'classroom':
            serializer = ClassroomSerializer(data=request.data)
            if serializer.is_valid():

                try:
                    user = UserProfile.objects.get(login_token=request.data['login_token'])
                    if user.role == 'board_admin':
                        serializer.validated_data['board'] = Board.objects.get(user=user)
                    elif user.role == 'board_authorities':
                        serializer.validated_data['board'] = Board.objects.get(user=UserProfile.objects.get(
                            email=BoardAuthorities.objects.get(user=user).to_dict()['board']['email']))
                except UserProfile.DoesNotExist:
                    return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)

                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_to_class(request):
    if request.method == 'POST':
        try:
            user = UserProfile.objects.get(login_token=request.data['login_token'])
            try:
                student, created = JoinedClass.objects.get_or_create(user=user, classroom=Classroom.objects.get(board=Board.objects.get(user=UserProfile.objects.get(email=request.data['board_email']))))
                student.full_name = request.data['full_name']
                student.national_code = request.data['national_code']
                student.passport_number = request.data['passport_number']
                student.father_name = request.data['father_name']
                student.phone_number = request.data['phone_number']
                student.telephone_number = request.data['telephone_number']
                student.location = request.data['location']
                student.location_code = request.data['location_code']
                student.save()
                return JsonResponse({'username': user.username}, safe=False, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_all_class(request):
    try:
        join_class = JoinedClass.objects.filter(user=UserProfile.objects.get(login_token=request.META.get('HTTP_AUTHORIZATION', None))).all()

        if join_class.count() == 0:
            return Response({'message': 'کلاسی وجود ندارد'}, status=status.HTTP_204_NO_CONTENT)

        response_data = {'data': [n.to_dict() for n in join_class]}
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def accept_for_classroom(request):
    if request.method == 'POST':
        try:
            user = UserProfile.objects.get(login_token=request.data['login_token'])
            if user.email == ADMIN_EMAIL or user.role == 'board_admin' or user.role == 'board_authorities':
                try:
                    student = JoinedClass.objects.get(user=UserProfile.objects.get(email=request.data['email']))
                except UserProfile.DoesNotExist:
                    return JsonResponse({'message': 'کاربری با این آدرس ایمیل یافت نشد.'},
                                        status=status.HTTP_404_NOT_FOUND)

                accepted = False if request.data['accepted'] == 'false' else True
                student.accepted = accepted
                student.rejected = not accepted
                student.save()

                return JsonResponse({'message': 'ثبت نام کاربر تایید گردید'}, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'message': 'توکن شما معتبر نیست.'}, status=status.HTTP_401_UNAUTHORIZED)
