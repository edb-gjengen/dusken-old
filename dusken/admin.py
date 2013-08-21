from django.contrib import admin
from django.contrib.auth.models import User
from dusken.models import Member, Institution, Address, Country

class MemberAdmin(admin.ModelAdmin):
    exclude = ( 'password', 'last_login', )

admin.site.unregister(User)
admin.site.register(Member, MemberAdmin)
admin.site.register(Institution)
admin.site.register(Address)
admin.site.register(Country)
