from django.contrib import admin
from account.models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'username')
    ordering = ('-date_added',)
    search_fields = ('name',)
    exclude=('date_added',)
admin.site.register(Profile,ProfileAdmin)