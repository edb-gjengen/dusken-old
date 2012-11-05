# FIXME
# - Reduce the database more?
#   - ExpiresformanytomanymembershipDuration
#   - Institution
#   - Member has place of study?
#   - Subgroups
#   - Positions
# - Only one type of adress? YES
# - ExtendedMemberdetail?
# - Legacy_id as extended member detail?

# TODO
# - autofields created, updated

from django.db import models

class Country(models.Model):
    country_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        db_table = u'country'

class Address(models.Model):
    address_id = models.IntegerField(primary_key=True)
    postalcode = models.CharField(max_length=10)
    addressline1 = models.CharField(max_length=255)
    placename = models.CharField(max_length=100)
    addressline2 = models.CharField(max_length=255)
    country_id = models.ForeignKey(Country, db_column='country_id')
    class Meta:
        db_table = u'address'

class Member(models.Model):
    member_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=150, unique=True)
    username = models.CharField(max_length=40, unique=True)
    phonenumber = models.IntegerField(unique=True, null=True, blank=True)
    givenname = models.CharField(max_length=200, blank=True)
    dateofbirth = models.DateField(null=True, blank=True)
    surname = models.CharField(max_length=200, blank=True)
    address_id = models.ForeignKey(Address, null=True, db_column='address_id', blank=True)
    class Meta:
        db_table = u'member'

class NorwegianAddress(models.Model):
    norwegian_address_id = models.IntegerField(primary_key=True)
    postal_code = models.CharField(max_length=10)
    place_name = models.CharField(max_length=100)
    class Meta:
        db_table = u'norwegian_address'

class ExtendedMemberDetail(models.Model):
    member_id = models.ForeignKey(Member, primary_key=True, db_column='member_id')
    class Meta:
        db_table = u'extended_member_details'

class PaymentForMembership(models.Model):
    payment_for_membership_id = models.IntegerField(primary_key=True)
    sms_payment_id = models.IntegerField(unique=True, null=True, blank=True)
    webshop_payment_id = models.IntegerField(unique=True, null=True, blank=True)
    voucher_id = models.IntegerField(unique=True, null=True, blank=True)
    class Meta:
        db_table = u'payment_for_membership'

class MembershipDuration(models.Model):
    membership_duration_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    minimum_duration = models.CharField(max_length=30)
    class Meta:
        db_table = u'membership_duration'

class Membership(models.Model):
    membership_id = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    member_id = models.ForeignKey(Member, db_column='member_id')
    membership_duration_id = models.ForeignKey(MembershipDuration, db_column='membership_duration_id')
    payment_for_membership_id = models.ForeignKey(PaymentForMembership, unique=True, null=True, db_column='payment_for_membership_id', blank=True)
    class Meta:
        db_table = u'membership'

class Group(models.Model):
    group_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        db_table = u'group'

# TODO Remove his and related.
class GroupMembership(models.Model):
    group_membership_id = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    member_id = models.ForeignKey(Member, db_column='member_id')
    group_id = models.ForeignKey(Group, db_column='group_id')
    membership_duration_id = models.ForeignKey(MembershipDuration, db_column='membership_duration_id')
    class Meta:
        db_table = u'group_membership'


class PaymentForGroupMembership(models.Model):
    group_membership_id = models.ForeignKey(GroupMembership, primary_key=True, db_column='group_membership_id')
    start_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(null=True, max_digits=19, decimal_places=4, blank=True)
    reference = models.CharField(max_length=100, blank=True)
    note = models.CharField(max_length=500, blank=True)
    class Meta:
        db_table = u'payment_for_group_membership'

class Expires(models.Model):
    expires_id = models.IntegerField(primary_key=True)
    monthofyear = models.IntegerField()
    dayofmonth = models.IntegerField()
    class Meta:
        db_table = u'expires'

class ExpiresformanytomanymembershipDuration(models.Model):
    expires_id = models.ForeignKey(Expires, db_column='expires_id')
    membership_duration_id = models.ForeignKey(MembershipDuration, db_column='membership_duration_id')
    class Meta:
        db_table = u'expiresformanytomanymembership_duration'

class Legacy(models.Model):
    legacy_id = models.IntegerField(primary_key=True)
    member_id = models.ForeignKey(Member, unique=True, null=True, db_column='member_id', blank=True)
    class Meta:
        db_table = u'legacy'

class Institution(models.Model):
    institutionname = models.CharField(max_length=255, primary_key=True)
    class Meta:
        db_table = u'institution'

class Subgroup(models.Model):
    subgroup_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    group_id = models.ForeignKey(Group, db_column='group_id')
    class Meta:
        db_table = u'subgroup'

class Position(models.Model):
    position_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    subgroup_id = models.ForeignKey(Subgroup, db_column='subgroup_id')
    is_static = models.NullBooleanField(null=True, blank=True)
    class Meta:
        db_table = u'position'

class PositionInfo(models.Model):
    position_info_id = models.IntegerField(primary_key=True)
    position_id = models.ForeignKey(Position, db_column='position_id')
    group_membership_id = models.ForeignKey(GroupMembership, null=True, db_column='group_membership_id', blank=True)
    email = models.CharField(max_length=150, blank=True)
    phonenumber = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'position_info'

class PlaceOfStudy(models.Model):
    place_of_study_id = models.IntegerField(primary_key=True)
    fromdate = models.DateField()
    institutionname = models.ForeignKey(Institution, db_column='institutionname')
    class Meta:
        db_table = u'place_of_study'

class MemberhasplaceOfStudy(models.Model):
    member_id = models.ForeignKey(Member, db_column='member_id')
    place_of_study_id = models.ForeignKey(PlaceOfStudy, db_column='place_of_study_id')
    class Meta:
        db_table = u'membershasplace_of_study'
