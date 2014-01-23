import django
import datetime

from django.db import models
from tastypie.models import create_api_key

class AbstractBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class Member(django.contrib.auth.models.AbstractUser, AbstractBaseModel):
    def __unicode__(self):
        if len(self.first_name) + len(self.last_name) > 0:
            return u'{first} {last} ({username})'.format(
                first=self.first_name,
                last=self.last_name,
                username=self.username)
        return u"{username}".format(username=self.username)

    phone_number = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    legacy_id = models.IntegerField(null=True, blank=True)
    address = models.OneToOneField('dusken.Address', null=True, blank=True)
    place_of_study = models.ManyToManyField('dusken.PlaceOfStudy', null=True, blank=True)

    def owner(self):
        return self
    
    def has_valid_membership(self):
        # FIXME more than one membership?
        # FIXME membership_type?
        membership = self.membership_set.filter(end_date__gt=datetime.datetime.now())
        return len(membership) == 1 and membership[0].is_valid()

class Membership(AbstractBaseModel):
    def __unicode__(self):
        return u"{0}: {1} - {2}".format(
            self.member,
            self.start_date,
            self.end_date)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    membership_type = models.ForeignKey('dusken.MembershipType')
    payment = models.ForeignKey('dusken.Payment', unique=True, null=True, blank=True)
    member = models.ForeignKey('dusken.Member')

    def expires(self):
        return self.end_date

    def is_valid(self):
        return self.payment is not None

    def owner(self):
        return self.member

class MembershipType(AbstractBaseModel):
    def __unicode__(self):
        return u"{}".format(self.name)

    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    does_not_expire = models.BooleanField(default=False)

class PaymentType(models.Model):
    def __unicode__(self):
        return u"{}".format(self.name)

    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class Payment(AbstractBaseModel):
    def __unicode__(self):
        return "{},- via {}".format(self.value, self.payment_type.name)

    # Note: More like tokens?
    payment_type = models.ForeignKey('dusken.PaymentType')
    value = models.IntegerField()
    transaction_id = models.IntegerField(unique=True, null=True, blank=True)

class Address(AbstractBaseModel):
    class Meta:
        verbose_name_plural = "Addresses"

    def __unicode__(self):
        return u"{street}, {code} {city}, {country}".format(
            street=self.street_address,
            code=self.postal_code,
            city=self.city,
            country=self.country)

    street_address = models.CharField(max_length=255)
    street_address_two = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.ForeignKey('dusken.Country', null=True, blank=True)

    @property
    def full(self):
        return self.__unicode__()

class Country(AbstractBaseModel):
    class Meta:
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True) #ISO 3166-1 alpha 2


class PlaceOfStudy(AbstractBaseModel):
    def __unicode__(self):
        return u"{institution}, {year}".format(
            institution=self.institution,
            year=self.from_date.year)

    from_date = models.DateField()
    institution = models.ForeignKey('dusken.Institution')


class Institution(AbstractBaseModel):
    def __unicode__(self):
        return u'%s - %s' % (self.short_name, self.name)

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=16)

class MemberMeta(AbstractBaseModel):
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True)
    member = models.ForeignKey('dusken.Member')

class GroupProfile(AbstractBaseModel):
    """
    django.contrib.auth.model.Group extended with additional fields.
    """
    def __unicode__(self):
        return u"{}".format(self.posix_name)

    posix_name = models.CharField(max_length=255, unique=True)
    group = models.OneToOneField(django.contrib.auth.models.Group)

class Division(AbstractBaseModel):
    """
    Associations, comittee or similar
    """
    def __unicode__(self):
        return u"{}".format(self.name)

    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    members = models.ManyToManyField('dusken.Member', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    groups = models.ManyToManyField(django.contrib.auth.models.Group, null=True, blank=True) # permissions # TODO remove this?

class ServiceHook(AbstractBaseModel):
    """
    Events with callback_urls
    """
    def __unicode__(self):
        return u"{}".format(self.name)

    event = models.CharField(max_length=255)
    member = models.ForeignKey('dusken.Member')
    is_active = models.BooleanField(default=True)
    callback_url = models.TextField()


# SIGNALS #
###########
models.signals.post_save.connect(create_api_key, sender=Member)

