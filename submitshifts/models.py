from django.db import models
from django.contrib.auth import get_user_model
from staff.models import Staff

# Create your models here.
class SubmitShift(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    fromtime = models.IntegerField(default = None, blank=True, null=True)
    totime = models.IntegerField(default = None, blank=True, null=True)
    absence_flg = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        title = (str(self.staff_id) + ' ' + str(self.year) + '-' + str(self.month) + '-' + str(self.day))
        return title

    class Meta:
        db_table = 'submitshifts'