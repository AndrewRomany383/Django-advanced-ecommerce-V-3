from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Account, UserProfile

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email',
                    'first_name',
                    'last_name',
                    'username',
                    'data_joined',
                    'last_login',
                    'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('data_joined', 'last_login')
    ordering = ('-data_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px" />'.format(object.profile_picture.url))
    list_display = ('user', 'phone_number', 'city')
    list_filter = ('city',)


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
