from django.contrib import admin

from myapp.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'avatar']
    
admin.site.register(User,UserAdmin)
