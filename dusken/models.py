import django
from django.db import models
from tastypie.models import create_api_key

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Member(django.contrib.auth.models.User):
    def __unicode__(self):
        if len(self.first_name) + len(self.last_name) > 0:
            return u'{first} {last} ({username})'.format(
                first=self.first_name,
                last=self.last_name,
                username=self.username)
        return u"{username}".format(username=self.username)

    phone_number = models.IntegerField(unique=True, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    legacy_id = models.IntegerField(unique=True, null=True, blank=True)
    address = models.ForeignKey('dusken.Address', null=True, blank=True)
    place_of_study = models.ManyToManyField('dusken.PlaceOfStudy', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Membership(BaseModel):
    def __unicode__(self):
        return u"{member}: {fromdate}".format(member=self.member, fromdate=self.start_date)

    start_date = models.DateField()
    mtype = models.ForeignKey('dusken.MembershipType', db_column='type')
    payment = models.ForeignKey('dusken.Payment', unique=True, null=True, blank=True)
    member = models.ForeignKey('dusken.Member')

    def expires(self):
        return self.mtype.end_date()

'''
   TODO: should validate end_day_of_month and end_month (use datetime exceptions)
'''
class MembershipType(BaseModel):
    def __unicode__(self):
        return u"{}".format(self.name)

    name = models.CharField(max_length=50, unique=True)
    duration_months = models.IntegerField(default=12)
    end_day_of_month = models.IntegerField(default=31)
    end_month = models.IntegerField(default=7)
    is_active = models.BooleanField(default=True)

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

class PaymentType(models.Model):
    def __unicode__(self):
        return u"{}".format(self.name)

    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

class Payment(BaseModel):
    def __unicode__(self):
        return self.payment_type #TODO

    # Note: More like tokens?
    payment_type = models.ForeignKey('dusken.PaymentType')
    value = models.IntegerField()
    transaction_id = models.IntegerField(unique=True, null=True, blank=True)


class FacebookAuth(BaseModel):
    def __unicode__(self):
        return u"{}".format(self.token)

    token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    token_expires = models.DateTimeField(null=True, blank=True)
    member = models.OneToOneField('dusken.Member', null=True, blank=True)
    
class GoogleAuth(BaseModel):
    def __unicode__(self):
        return u"{}".format(self.token)

    token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    token_expires = models.DateTimeField(null=True, blank=True)
    member = models.OneToOneField('dusken.Member', null=True, blank=True)


class Address(BaseModel):
    class Meta:
        verbose_name_plural = "Addresses"

    def __unicode__(self):
        return u"{street}, {code} {city}, {country}".format(
            street=self.street_address,
            code=self.postal_code,
            city=self.city,
            country=self.country)

    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.ForeignKey('dusken.Country', null=True, blank=True)


class Country(BaseModel):
    class Meta:
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True) #ISO 3166-1 alpha 2


class PlaceOfStudy(BaseModel):
    def __unicode__(self):
        return u"{institution}, {year}".format(
            institution=self.institution,
            year=self.from_date.year)

    from_date = models.DateField()
    institution = models.ForeignKey('dusken.Institution')


class Institution(BaseModel):
    def __unicode__(self):
        return u'%s - %s' % (self.short_name, self.name)

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=16)


class ExtendedMemberDetail(BaseModel):
    pass


class Group(django.contrib.auth.models.Group):
    def __unicode__(self):
        return u"{} ({})".format(self.name, self.posix_name)

    posix_name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

###########
# SIGNALS #
###########
models.signals.post_save.connect(create_api_key, sender=Member)

