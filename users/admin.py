from django.contrib import admin

# Register your models here.
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import User  # <-- make sure this is 'User', not 'CustomUser'
from .models import User
from .models import MatrimonyProfile
from .models import CustomUser

admin.site.register(User, UserAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(MatrimonyProfile)
