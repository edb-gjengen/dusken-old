from django.contrib import admin
from main.models import Member

class MemberAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Other User instances',    {'fields' : ['legacy_id']}),
        #('User data',               {'fields' : ['username', 'email', 'first_name', 'last_name']}),
        ('User data',               {'fields' : ['phone_number', 'date_of_birth', 'address', 'place_of_study']}),
    ]

admin.site.register(Member, MemberAdmin)
