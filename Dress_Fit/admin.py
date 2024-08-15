from django.contrib import admin

# Register your models here.
from .models import admin_user
admin.site.register(admin_user)

from .models import Feedback
admin.site.register(Feedback)