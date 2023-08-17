from django.db import models


class News(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    image = models.ImageField()
    date = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Cultural(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    image = models.ImageField()

    def __str__(self):
        return self.title


class Gallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return self.title


class Game(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField()
    SEX_CHOICES = (
        ("پسر", "Boy"),
        ("دختر", "Girl"),
    )
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, default='Boy')

    def __str__(self):
        return self.name


class Competition(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    file_title = models.CharField(max_length=1000, blank=True, null=True)
    file_link = models.FileField(blank=True, null=True)
    attention = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    # date = models.DateField()
    date = models.CharField(max_length=10)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    city = models.CharField(max_length=2000, default="")

    def __str__(self):
        return str(self.date)


class Result(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, blank=True, null=True)
    file_title = models.CharField(max_length=1000, blank=True, null=True)
    file_link = models.FileField(blank=True, null=True)
    attention = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=1000, default="")
    rate = models.CharField(max_length=100, blank=True, null=True, default=0)
    athlete_full_name = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.city


class Dormitories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    direction_link = models.CharField(max_length=1000, null=True)
    image = models.ImageField()

    def __str__(self):
        return self.name


class Gym(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    direction_link = models.CharField(max_length=1000, null=True)
    image = models.ImageField()

    def __str__(self):
        return self.name
