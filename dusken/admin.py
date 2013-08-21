from django.contrib import admin
from django.contrib.auth.models import User
from dusken.models import Member, Institution, Address, Country

class MemberAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Other User instances',
            {'fields' : ['legacy_id']}),
        ('User data',
            {'fields' : ['username', 'email', 'first_name', 'last_name']}),
        ('User data',
            {'fields' : ['phone_number', 'date_of_birth', 'address', 'place_of_study']}),
    ]

    readonly_fields = ( 'username', )

class InstitutionAdmin(admin.ModelAdmin):
	pass

admin.site.unregister(User)
admin.site.register(Member, MemberAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Address)
admin.site.register(Country)
