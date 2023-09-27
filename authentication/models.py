import decimal
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

ADMIN_EMAIL = "AA@gmail.com"


# ADMIN_PASSWORD = 'AA'


class DepartmentNews(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="عنوان")
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name="توضیحات")
    image = models.ImageField(verbose_name="عکس", upload_to='profile_pics/news')
    date = models.CharField(max_length=10, verbose_name="تاریخ")
    link = models.CharField(max_length=1000, blank=True, null=True, verbose_name="لینک سایت")

    class Meta:
        verbose_name_plural = "اخبار وزارت ورزش"
        verbose_name = "خبر وزارت ورزش"

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'image': self.image.url,
            'date': self.date,
            'link': self.link,
        }


class UserProfile(models.Model):
    email = models.EmailField(verbose_name="آدرس ایمیل", primary_key=True, unique=True, null=False)
    phone_number = models.CharField(verbose_name="شماره موبایل", max_length=11, unique=True, null=True)
    username = models.CharField(verbose_name="نام کاربری", max_length=50, null=False, default='noName')
    password = models.CharField(max_length=16, null=False, editable=False)
    image_profile = models.ImageField(verbose_name="تصویر پروفایل", upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(verbose_name="بیوگرافی", max_length=1000, null=True, blank=True)
    login_token = models.UUIDField(default=uuid.uuid4, editable=False)
    accepted = models.BooleanField(verbose_name="تایید شده توسط ادمین", default=False)
    rejected = models.BooleanField(verbose_name="رد شده توسط ادمین", default=False)
    rate = models.DecimalField(
        verbose_name="امتیاز",
        default=0.0,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    num_ratings = models.PositiveIntegerField(default=0)
    total_rating = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)

    USER_ROLES = (
        ('simple_user', 'simple_user'),
        ('coach', 'coach'),
        ('gym_manager', 'gym_manager'),
        ('actor', 'actor'),
        ('office_admin', 'office_admin'),
        ('office_manager', 'office_manager'),
        ('office_expert', 'office_expert'),
        ('board_admin', 'board_admin'),
        ('board_authorities', 'board_authorities'),
    )

    role = models.CharField(
        verbose_name="نقش کاربر",
        max_length=20,
        choices=USER_ROLES,
        default='simple_user',
    )

    class Meta:
        verbose_name_plural = "پروفایل کاربران"
        verbose_name = "پروفابل کاربر"

    def __str__(self):
        return self.email

    def to_dict(self):
        return {
            'email': self.email,
            'phone_number': self.phone_number,
            'username': self.username,
            'image_profile': None if self.image_profile == '' else self.image_profile.url,
            'bio': self.bio,
            'role': self.role,
            'accepted': self.accepted,
            'rejected': self.rejected,
            'rate': self.rate,
        }

    def update_average_rating(self, new_rating):
        new_rating = decimal.Decimal(new_rating)
        self.total_rating += new_rating
        self.num_ratings += 1
        if self.num_ratings > 0:
            self.rate = self.total_rating / self.num_ratings
        else:
            self.rate = 0.0
        self.save()


class Coach(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    document_image = models.ImageField(verbose_name="تصویر کارت مربی‌گری", upload_to='profile_pics/lisense_pics',
                                       null=True, blank=True)
    education = models.CharField(verbose_name="تحصیلات", max_length=40)
    field = models.CharField(verbose_name="تخصص‌ها", max_length=1000, null=True, blank=True)
    gym = models.ForeignKey(verbose_name="باشگاه", to='GymManager', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "مربی‌ها"
        verbose_name = "مربی"

    def to_dict(self):
        return {
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'username': self.user.username,
            'image_profile': None if self.user.image_profile == '' else self.user.image_profile.url,
            'bio': self.user.bio,
            'role': self.user.role,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
            'document_image': None if self.document_image == '' else self.document_image.url,
            'rate': self.user.rate,
            'education': self.education,
            'field': self.field,
            'gym': self.gym.for_coach(),
        }


class GymManager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="نام باشگاه", max_length=50, unique=True)
    image = models.ImageField(verbose_name="تصویر باشگاه", upload_to='profile_pics/gym_place', null=True, blank=True)
    document_image = models.ImageField(verbose_name="تصویر پروانه", upload_to='profile_pics/lisense_pics', null=True,
                                       blank=True)
    possibilities = models.TextField(verbose_name="امکانات", max_length=2000, blank=True)
    location = models.CharField(verbose_name="آدرس", max_length=1000)
    location_link = models.CharField(verbose_name="لینک آدرس", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "سالن‌دارها"
        verbose_name = "سالن‌دار"

    def to_dict(self):
        return {
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'username': self.user.username,
            'image_profile': None if self.user.image_profile == '' else self.user.image_profile.url,
            'bio': self.user.bio,
            'role': self.user.role,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
            'name': self.name,
            'image': None if self.image == '' else self.image.url,
            'document_image': None if self.document_image == '' else self.document_image.url,
            'rate': self.user.rate,
            'possibilities': self.possibilities,
            'location': self.location,
            'location_link': self.location_link,
        }

    def for_coach(self):
        return {
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'username': self.user.username,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
            'name': self.name,
            'rate': self.user.rate,
        }


class Actor(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    document_image = models.ImageField(verbose_name="تصویر حکم قهرمانی", upload_to='profile_pics/lisense_pics',
                                       null=True, blank=True)
    field = models.CharField(verbose_name="رشته", max_length=30)

    class Meta:
        verbose_name_plural = "قهرمان‌ها"
        verbose_name = "قهرمان"

    def to_dict(self):
        return {
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'username': self.user.username,
            'image_profile': None if self.user.image_profile == '' else self.user.image_profile.url,
            'bio': self.user.bio,
            'role': self.user.role,
            'rate': self.user.rate,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
            'field': self.field,
            'document_image': None if self.document_image == '' else self.document_image.url,
        }


class OfficeAuthorities(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    office = models.ForeignKey(verbose_name="اداره", to='Office', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "کارمندان اداره‌ها"
        verbose_name = "کارمند اداره"

    def to_dict(self):
        return {
            'board': self.office.for_auth(),
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'username': self.user.username,
            'image_profile': None if self.user.image_profile == '' else self.user.image_profile.url,
            'bio': self.user.bio,
            'role': self.user.role,
            'rate': self.user.rate,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
        }


class Office(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, verbose_name='ادمین اداره')
    name = models.CharField(verbose_name='نام اداره', max_length=50, null=False)
    location = models.CharField(verbose_name='آدرس', null=False, max_length=1000)

    class Meta:
        verbose_name_plural = "اداره‌ها"
        verbose_name = "اداره"

    def for_auth(self):
        return {
            'name': self.name,
            'email': self.user.email,
        }

    def to_dict(self):
        return {
            'name': self.name,
            'location': self.location,
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'username': self.user.username,
            'image_profile': None if self.user.image_profile == '' else self.user.image_profile.url,
            'bio': self.user.bio,
            'role': self.user.role,
            'rate': self.user.rate,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
        }


class BoardAuthorities(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    board = models.ForeignKey(verbose_name="هیئت", to='Board', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "کارشناس‌های هیئت‌ها"
        verbose_name = "کارشناس اداره"

    def to_dict(self):
        return {
            'board': self.board.for_auth(),
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'username': self.user.username,
            'image_profile': None if self.user.image_profile == '' else self.user.image_profile.url,
            'bio': self.user.bio,
            'role': self.user.role,
            'rate': self.user.rate,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
        }


class Board(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, verbose_name='ادمین هیئت')
    name = models.CharField(verbose_name='نام هیئت', max_length=50, null=False)
    goal = models.CharField(verbose_name='اهداف', max_length=1500, null=True, blank=True)
    location = models.CharField(verbose_name='آدرس', null=False, max_length=1000)

    class Meta:
        verbose_name_plural = "هیئت‌ها"
        verbose_name = "هیئت"

    def for_auth(self):
        return {
            'name': self.name,
            'email': self.user.email,
        }

    def to_dict(self):
        return {
            'name': self.name,
            'goal': self.goal,
            'location': self.location,
            'email': self.user.email,
            'phone_number': self.user.phone_number,
            'username': self.user.username,
            'image_profile': None if self.user.image_profile == '' else self.user.image_profile.url,
            'bio': self.user.bio,
            'role': self.user.role,
            'rate': self.user.rate,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
        }


class Classroom(models.Model):
    name = models.CharField(verbose_name='نام کلاس', null=False, max_length=30)
    date = models.CharField(verbose_name='تاریخ برگزاری', null=False, max_length=10)
    time = models.CharField(verbose_name='زمان شروع کلاس', null=False, max_length=8)
    location = models.CharField(verbose_name='مکان برگزاری', null=False, max_length=100)
    link = models.CharField(verbose_name='لینک کلاس', null=False, max_length=1500)
    capacity = models.IntegerField(verbose_name='ظرفیت کلاس', null=False)
    board = models.ForeignKey(verbose_name="هیئت برگزارکننده", to='Board', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "کلاس‌ها"
        verbose_name = "کلاس"

    def to_dict(self):
        return {
            'name': self.name,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'link': self.link,
            'capacity': self.capacity,
            'board_email': self.board.user.email,
            'board_name': self.board.name,
            'users': JoinedClass.objects.filter(classroom=self, accepted=True).all().count()
        }


class JoinedClass(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(verbose_name='نام کاربر', null=True, max_length=30)
    national_code = models.CharField(verbose_name='کدملی', null=True, max_length=30)
    passport_number = models.CharField(verbose_name='شماره شناسنامه', null=True, max_length=30)
    father_name = models.CharField(verbose_name='نام پدر', null=True, max_length=30)
    phone_number = models.CharField(verbose_name='شماره موبایل', null=True, max_length=30)
    telephone_number = models.CharField(verbose_name='شماره ثابت', null=True, max_length=30)
    location = models.CharField(verbose_name='آدرس', null=True, max_length=30)
    location_code = models.CharField(verbose_name='کدپستی', null=True, max_length=30)
    accepted = models.BooleanField(verbose_name='تایید شده', default=False)
    rejected = models.BooleanField(verbose_name='رد شده', default=False)
    user = models.ForeignKey(verbose_name="آدرس ایمیل کاربر", to='UserProfile', on_delete=models.SET_NULL, null=True)
    classroom = models.ForeignKey(verbose_name="آدرس ایمیل هیئت کلاس", to='Classroom', on_delete=models.SET_NULL,
                                  null=True)

    class Meta:
        verbose_name_plural = "افراد و کلاس‌ها"
        verbose_name = "فرد و کلاس"

    def to_dict(self):
        return {
            'full_name': self.full_name,
            'national_code': self.national_code,
            'passport_number': self.passport_number,
            'father_name': self.father_name,
            'phone_number': self.phone_number,
            'telephone_number': self.telephone_number,
            'location': self.location,
            'location_code': self.location_code,
            'accepted': self.accepted,
            'rejected': self.rejected,
            'user_email': self.user.email,
            'board_email': self.classroom.board.user.email,
        }


class BoardGame(models.Model):
    name = models.CharField(verbose_name='نام بازی', null=False, max_length=30)
    image = models.ImageField(verbose_name="تصویر", upload_to='profile_pics', null=True, blank=True)
    date = models.CharField(verbose_name='تاریخ برگزاری', null=False, max_length=10)
    time = models.CharField(verbose_name='زمان شروع بازی', null=False, max_length=8)
    location = models.CharField(verbose_name='مکان برگزاری', null=False, max_length=100)
    board = models.ForeignKey(verbose_name="هیئت برگزارکننده", to='Board', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "مسابقه‌های هیئت‌ها"
        verbose_name = "مسابقه هیئت"

    def to_dict(self):
        return {
            'name': self.name,
            'image': None if self.image == '' else self.image.url,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'board_email': self.board.user.email,
            'board_name': self.board.name,
        }


class Message(models.Model):
    office_manager = models.ForeignKey(verbose_name="مدیر", to='OfficeAuthorities', on_delete=models.SET_NULL,
                                       null=True)
    message = models.TextField(verbose_name='متن پیام', null=False, max_length=3000)
    answered = models.BooleanField(verbose_name='پاسخ‌داده شده', default=False)

    class Meta:
        verbose_name_plural = "پیام‌ها"
        verbose_name = "پیام"

    def to_dict(self):
        return {
            'office_manager': self.office_manager.user.email,
            'message': self.message,
            'answered': self.answered
        }
