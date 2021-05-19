from django.contrib import admin
from staff.models import Staff
from submitshifts.models import SubmitShift

# Register your models here.
admin.site.register(Staff)
admin.site.register(SubmitShift)