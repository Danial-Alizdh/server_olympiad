from django.db import models


class News(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="عنوان")
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name="توضیحات")
    image = models.ImageField(verbose_name="عکس")
    date = models.CharField(max_length=10, verbose_name="تاریخ")

    class Meta:
        verbose_name_plural = "اخبار"
        verbose_name = "خبر"

    def __str__(self):
        return self.title


class Cultural(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="عنوان")
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name="توضیحات")
    image = models.ImageField(verbose_name="عکس")

    class Meta:
        verbose_name_plural = "فرهنگی‌ها"
        verbose_name = "فرهنگی"

    def __str__(self):
        return self.title


class Gallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="عنوان")
    image = models.ImageField(verbose_name="عکس")

    class Meta:
        verbose_name_plural = "گالری"
        verbose_name = "گالری"

    def __str__(self):
        return self.title


class Game(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="نام بازی")
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name="توضیحات")
    image = models.ImageField(verbose_name="عکس")

    class Meta:
        verbose_name_plural = "بازی‌ها"
        verbose_name = "بازی"

    def __str__(self):
        return self.name


class Competition(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE, verbose_name="نام بازی")
    file_title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="عنوان فایل")
    file_link = models.FileField(blank=True, null=True, verbose_name="فایل")
    attention = models.CharField(max_length=1000, blank=True, null=True, verbose_name="متن توجه (نوشته قرمز رنگ)")
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name="توضیحات")
    date = models.CharField(max_length=10, verbose_name="تاریخ")
    start_time = models.TimeField(blank=True, null=True, verbose_name="زمان شروع")
    end_time = models.TimeField(blank=True, null=True, verbose_name="زمان پایان")
    city = models.CharField(max_length=2000, default="", verbose_name="استان")

    class Meta:
        verbose_name_plural = "مسابقه‌ها"
        verbose_name = "مسابقه"

    def __str__(self):
        return str(self.date)


class Result(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE, verbose_name="نام بازی")
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="عنوان")
    file_title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="عنوان فایل")
    file_link = models.FileField(blank=True, null=True, verbose_name="فایل")
    attention = models.CharField(max_length=1000, blank=True, null=True, verbose_name="متن توجه (نوشته قرمز رنگ)")
    city = models.CharField(max_length=1000, default="", verbose_name="استان")
    rate = models.CharField(max_length=100, default="0", verbose_name="امتیاز")
    athlete_full_name = models.CharField(max_length=500, blank=True, null=True, verbose_name="نام بازیکن")

    class Meta:
        verbose_name_plural = "نتیجه‌ها"
        verbose_name = "نتیجه"

    def __str__(self):
        return self.city


class Dormitories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="نام خوابگاه")
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name="توضیحات")
    direction_link = models.CharField(max_length=1000, blank=True, null=True, verbose_name="لینک گوگل مپ یا بلد")
    image = models.ImageField(verbose_name="عکس")

    class Meta:
        verbose_name_plural = "خوابگاه‌ها"
        verbose_name = "خوابگاه"

    def __str__(self):
        return self.name


class Gym(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="نام سالن")
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name="توضیحات")
    direction_link = models.CharField(max_length=1000, blank=True, null=True, verbose_name="لینک گوگل مپ یا بلد")
    image = models.ImageField(verbose_name="عکس")

    class Meta:
        verbose_name_plural = "سالن‌های مسابقه‌"
        verbose_name = "سالن"

    def __str__(self):
        return self.name


class Survey(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    context = models.TextField(verbose_name="متن")

    class Meta:
        verbose_name_plural = "نظرها"
        verbose_name = "نظرسنجی"

    def __str__(self):
        return self.email
