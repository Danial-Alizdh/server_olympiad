import decimal

from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

ADMIN_EMAIL = "AA@gmail.com"


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
    )

    role = models.CharField(
        verbose_name="نقش کاربر",
        max_length=15,
        choices=USER_ROLES,
        default='simple_user',
    )

    class Meta:
        verbose_name_plural = "پروفایل کاربران"
        verbose_name = "پروفابل کاربر"

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     if self.image_profile and self.image_profile != 'null':
    #         img = Image.open(self.image_profile.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.image_profile.path)

    def to_dict(self):
        return {
            'email': self.email,
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
        # Calculate the new total rating by adding the new rating to the current total
        self.total_rating += new_rating
        # Increment the number of ratings
        self.num_ratings += 1
        # Calculate the new average rating
        if self.num_ratings > 0:
            self.rate = self.total_rating / self.num_ratings
        else:
            self.rate = 0.0
        # Save the updated object
        self.save()


class Coach(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    document_image = models.ImageField(verbose_name="تصویر کارت مربی‌گری", upload_to='profile_pics/lisense_pics', null=True, blank=True)
    education = models.CharField(verbose_name="تحصیلات", max_length=40)
    field = models.CharField(verbose_name="تخصص‌ها", max_length=1000, null=True, blank=True)
    gym = models.ForeignKey(verbose_name="باشگاه", to='GymManager', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "مربی‌ها"
        verbose_name = "مربی"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     if self.document_image:
    #         img = Image.open(self.document_image.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.document_image.path)

    def to_dict(self):
        return {
            'email': self.user.email,
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

    # def for_gym(self):
    #     return {
    #         'email': self.user.email,
    #         'username': self.user.username,
    #         'image_profile': self.user.image_profile.url,
    #         'accepted': self.user.accepted,
    #         'rejected': self.user.rejected,
    #     }

class GymManager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="نام باشگاه", max_length=50, unique=True)
    image = models.ImageField(verbose_name="تصویر باشگاه", upload_to='profile_pics/gym_place', null=True, blank=True)
    document_image = models.ImageField(verbose_name="تصویر پروانه", upload_to='profile_pics/lisense_pics', null=True, blank=True)
    possibilities = models.TextField(verbose_name="امکانات", max_length=2000, blank=True)
    location = models.CharField(verbose_name="آدرس", max_length=1000)
    location_link = models.CharField(verbose_name="لینک آدرس", max_length=50, null=True, blank=True)
    # coaches = models.ManyToManyField(verbose_name="مربی‌ها", to='Coach', related_name='gyms_managed', blank=True)

    class Meta:
        verbose_name_plural = "سالن‌دارها"
        verbose_name = "سالن‌دار"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     if self.image:
    #         img = Image.open(self.image.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)
    #
    #     if self.document_image:
    #         img = Image.open(self.document_image.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.document_image.path)

    def to_dict(self):
        return {
            'email': self.user.email,
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
            'username': self.user.username,
            'accepted': self.user.accepted,
            'rejected': self.user.rejected,
            'name': self.name,
            'rate': self.user.rate,
        }


class Actor(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    document_image = models.ImageField(verbose_name="تصویر حکم قهرمانی", upload_to='profile_pics/lisense_pics', null=True, blank=True)
    field = models.CharField(verbose_name="رشته", max_length=30)

    class Meta:
        verbose_name_plural = "قهرمان‌ها"
        verbose_name = "قهرمان"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     if self.document_image:
    #         img = Image.open(self.document_image.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.document_image.path)

    def to_dict(self):
        return {
            'email': self.user.email,
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
