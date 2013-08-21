from django.contrib import admin
from django.contrib.auth.models import User
from dusken.models import *

class MemberAdmin(admin.ModelAdmin):
    exclude = ( 'password', 'last_login', )
    fieldsets = (
        (None, {
            'fields' : ('username', 'first_name', 'last_name', 'date_of_birth'),
        }),
        ('Contact info', {
            'fields' : ('email', 'phone_number', 'address', 'place_of_study'),
        }),
        ('Permissions', {
            'fields' : ('is_superuser', 'is_staff', 'groups', 'user_permissions'),
        }),
        ('Legacy', {
            'fields' : ('legacy_id', ),
        }),
        ('Creation time', {
            'fields' : ('date_joined', ),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ('username', )
        return self.readonly_fields


class InstitutionAdmin(admin.ModelAdmin):
	pass

admin.site.unregister(django.contrib.auth.models.Group)
admin.site.unregister(User)
admin.site.register(Address)
admin.site.register(Country)
admin.site.register(Group)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipType)
admin.site.register(Membership)
admin.site.register(PlaceOfStudy)
