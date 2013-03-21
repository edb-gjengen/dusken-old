import django
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Address(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.ForeignKey(Country)
    postal_code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Institution(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class PlaceOfStudy(models.Model):
    from_date = models.DateField()
    institution = models.ForeignKey(Institution)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Member(models.Model):
    # Auth:
    user = models.OneToOneField(django.contrib.auth.models.User)

    def username(self): return self.user.username
    def email(self): return self.user.email
    def first_name(self): return self.user.first_name
    def last_name(self): return self.user.last_name

    # Profile fields:
    phone_number = models.IntegerField(unique=True, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    legacy_id = models.IntegerField(unique=True, null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True)
    place_of_study = models.ManyToManyField(PlaceOfStudy, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class FacebookAuth(models.Model):
    token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    token_expires = models.DateTimeField(null=True, blank=True)
    member = models.OneToOneField(Member, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class GoogleAuth(models.Model):
    token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    token_expires = models.DateTimeField(null=True, blank=True)
    member = models.OneToOneField(Member, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class ExtendedMemberDetail(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pass

class PaymentForMembership(models.Model):
    # Note: More like tokens?
    sms_payment_id = models.IntegerField(unique=True, null=True, blank=True)
    webshop_payment_id = models.IntegerField(unique=True, null=True, blank=True)
    voucher_id = models.IntegerField(unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

'''
   TODO: should validate end_day_of_month and end_month (use datetime exceptions)
'''
class MembershipType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    duration_months = models.IntegerField(default=12)
    end_day_of_month = models.IntegerField(default=31)
    end_month = models.IntegerField(default=7)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def end_date(self):
        import datetime
        now = datetime.datetime.now()
        year = now.year + (now.month - 1 + self.duration_months) / 12
        month = (now.month - 1 + self.duration_months) % 12 + 1

        end1 = datetime.datetime(year, month, now.day, 0, 0, 0)
        end2 = None
        # closest date which fullfills the day, month and duration specified
        if now.month < self.end_month or (now.month == self.end_month and now.day < self.end_day_of_month):
            end2 = datetime.datetime(now.year, self.end_month, self.end_day_of_month)
        else:
            end2 = datetime.datetime(now.year+1, self.end_month, self.end_day_of_month)

        return min(end1, end2)

class Membership(models.Model):
    start_date = models.DateField()
    mtype = models.ForeignKey(MembershipType, db_column='type')
    payment = models.ForeignKey(PaymentForMembership, unique=True, null=True, blank=True)
    member = models.ForeignKey(Member)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def expires(self):
        return self.mtype.end_date()

class Group(django.contrib.auth.models.Group):
    posix_name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class GroupMembership(models.Model):
    start_date = models.DateField()
    member = models.ForeignKey(Member)
    group = models.ForeignKey(Group)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
