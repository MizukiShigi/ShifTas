from django.contrib import admin
from staff.models import Staff
from submitshifts.models import SubmitShift
from createshifts.models import ModifyShift, CounterShift, FlyerShift, KitchenShift, CompleteShift

# Register your models here.
admin.site.register(Staff)
admin.site.register(SubmitShift)
admin.site.register(ModifyShift)
admin.site.register(CounterShift)
admin.site.register(FlyerShift)
admin.site.register(KitchenShift)
admin.site.register(CompleteShift)