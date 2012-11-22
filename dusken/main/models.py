# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class NorwegianAddress(models.Model):
    norwegian_addressid = models.IntegerField(primary_key=True)
    postalcode = models.CharField(max_length=10)
    placename = models.CharField(max_length=100)
    class Meta:
        db_table = u'norwegian_address'

class ExtendedMemberDetails(models.Model):
    membersid = models.ForeignKey(Member, primary_key=True, db_column='membersid')
    class Meta:
        db_table = u'extended_member_details'

class PaymentForMembership(models.Model):
    payment_for_membershipid = models.IntegerField(primary_key=True)
    sms_paymentid = models.IntegerField(unique=True, null=True, blank=True)
    webshop_paymentid = models.IntegerField(unique=True, null=True, blank=True)
    voucherid = models.IntegerField(unique=True, null=True, blank=True)
    class Meta:
        db_table = u'payment_for_membership'

class Membership(models.Model):
    membershipid = models.IntegerField(primary_key=True)
    startdate = models.DateField()
    membersid = models.ForeignKey(Member, db_column='membersid')
    membership_durationid = models.ForeignKey(MembershipDuration, db_column='membership_durationid')
    payment_for_membershipid = models.ForeignKey(PaymentForMembership, unique=True, null=True, db_column='payment_for_membershipid', blank=True)
    class Meta:
        db_table = u'membership'

class PaymentForGroupMembership(models.Model):
    group_membershipid = models.ForeignKey(GroupMembership, primary_key=True, db_column='group_membershipid')
    startdate = models.DateField(null=True, blank=True)
    amount = models.DecimalField(null=True, max_digits=19, decimal_places=4, blank=True)
    reference = models.CharField(max_length=100, blank=True)
    note = models.CharField(max_length=500, blank=True)
    class Meta:
        db_table = u'payment_for_group_membership'

class Expires(models.Model):
    expiresid = models.IntegerField(primary_key=True)
    monthofyear = models.IntegerField()
    dayofmonth = models.IntegerField()
    class Meta:
        db_table = u'expires'

class ExpiresformanytomanymembershipDuration(models.Model):
    expiresid = models.ForeignKey(Expires, db_column='expiresid')
    membership_durationid = models.ForeignKey(MembershipDuration, db_column='membership_durationid')
    class Meta:
        db_table = u'expiresformanytomanymembership_duration'

class MembershipDuration(models.Model):
    membership_durationid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    minimumduration = models.CharField(max_length=30)
    class Meta:
        db_table = u'membership_duration'

class Address(models.Model):
    addressid = models.IntegerField(primary_key=True)
    postalcode = models.CharField(max_length=10)
    addressline1 = models.CharField(max_length=255)
    placename = models.CharField(max_length=100)
    addressline2 = models.CharField(max_length=255)
    countryid = models.ForeignKey(Country, db_column='countryid')
    class Meta:
        db_table = u'address'

class Country(models.Model):
    countryid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        db_table = u'country'

class Legacy(models.Model):
    legacyid = models.IntegerField(primary_key=True)
    membersid = models.ForeignKey(Members, unique=True, null=True, db_column='membersid', blank=True)
    class Meta:
        db_table = u'legacy'

class Institution(models.Model):
    institutionname = models.CharField(max_length=255, primary_key=True)
    class Meta:
        db_table = u'institution'

class Groups(models.Model):
    groupsid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        db_table = u'groups'

class Subgroups(models.Model):
    subgroupsid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    groupsid = models.ForeignKey(Groups, db_column='groupsid')
    class Meta:
        db_table = u'subgroups'

class GroupMembership(models.Model):
    group_membershipid = models.IntegerField(primary_key=True)
    startdate = models.DateField()
    membersid = models.ForeignKey(Member, db_column='membersid')
    groupsid = models.ForeignKey(Groups, db_column='groupsid')
    membership_durationid = models.ForeignKey(MembershipDuration, db_column='membership_durationid')
    class Meta:
        db_table = u'group_membership'

class PositionInfo(models.Model):
    position_infoid = models.IntegerField(primary_key=True)
    positionsid = models.ForeignKey(Positions, db_column='positionsid')
    group_membershipid = models.ForeignKey(GroupMembership, null=True, db_column='group_membershipid', blank=True)
    email = models.CharField(max_length=150, blank=True)
    phonenumber = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'position_info'

class Positions(models.Model):
    positionsid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    subgroupsid = models.ForeignKey(Subgroups, db_column='subgroupsid')
    isstatic = models.BooleanField(null=True, blank=True)
    class Meta:
        db_table = u'positions'

class Member(models.Model):
    membersid = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=150, unique=True)
    username = models.CharField(max_length=40, unique=True)
    phonenumber = models.IntegerField(unique=True, null=True, blank=True)
    givenname = models.CharField(max_length=200, blank=True)
    dateofbirth = models.DateField(null=True, blank=True)
    surname = models.CharField(max_length=200, blank=True)
    addressid = models.ForeignKey(Address, null=True, db_column='addressid', blank=True)
    class Meta:
        db_table = u'members'

class MembershasplaceOfStudy(models.Model):
    membersid = models.ForeignKey(Member, db_column='membersid')
    place_of_studyid = models.ForeignKey(PlaceOfStudy, db_column='place_of_studyid')
    class Meta:
        db_table = u'membershasplace_of_study'

class PlaceOfStudy(models.Model):
    place_of_studyid = models.IntegerField(primary_key=True)
    fromdate = models.DateField()
    institutionname = models.ForeignKey(Institution, db_column='institutionname')
    class Meta:
        db_table = u'place_of_study'

class SchemaMigrations(models.Model):
    version = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = u'schema_migrations'

