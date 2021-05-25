from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Staff(models.Model):
    staff = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    staff_name = models.CharField(max_length=255)
    age = models.IntegerField()
    staff_no = models.IntegerField(default=0, unique=True, blank=False)
    houry_wage = models.IntegerField(default=1000)
    counter_flg = models.BooleanField()
    flyer_flg = models.BooleanField()
    kitchen_flg = models.BooleanField()
    responsible_flg = models.BooleanField()
    opener_flg = models.BooleanField()
    rookie_flg = models.BooleanField()
    shift_creater_flg = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_name
