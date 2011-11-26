from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from programme.account.models import User_Profile

class UserProfileInline(admin.TabularInline):
    model = User_Profile
    fk_name = 'user'
    max_num = 1
    
class MyUserAdmin(UserAdmin):
    inlines = [
        UserProfileInline,
    ]
    


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
#admin.site.register(User_Profile, User_ProfileAdmin)

