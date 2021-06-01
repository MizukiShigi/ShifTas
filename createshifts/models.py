from django.db import models
from submitshifts.models import SubmitShift

# Create your models here.
class ModifyShift(models.Model):
    submit_id = models.ForeignKey(SubmitShift, null=True, on_delete=models.CASCADE)
    position = models.CharField(max_length=10)
    modify_fromtime = models.IntegerField()
    modify_totime = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CounterShift(models.Model):
    am_1 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_am1')
    am_2 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_am2')
    am_3 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_am3')
    am_4 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_am4')
    am_5 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_am5')
    pm_1 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_pm1')
    pm_2 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_pm2')
    pm_3 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_pm3')
    pm_4 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_pm4')
    pm_5 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_pm5')
    pm_6 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='counter_pm6')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FlyerShift(models.Model):
    am_1 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='flyer_am1')
    am_2 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='flyer_am2')
    pm_1 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='flyer_pm1')
    pm_2 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='flyer_pm2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class KitchenShift(models.Model):
    am_1 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='kitchen_am1')
    am_2 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='kitchen_am2')
    pm_1 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='kitchen_pm1')
    pm_2 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='kitchen_pm2')
    pm_3 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='kitchen_pm3')
    pm_4 = models.ForeignKey(ModifyShift, null=True, on_delete=models.CASCADE, related_name='kitchen_pm4')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CompleteShift(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    is_holiday = models.BooleanField()
    counter_shift = models.ForeignKey(CounterShift, on_delete=models.CASCADE)
    flyer_shift = models.ForeignKey(FlyerShift, on_delete=models.CASCADE)
    kitchen_shift = models.ForeignKey(KitchenShift, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    