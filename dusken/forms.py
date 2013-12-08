from django import forms

from models import Member

class MemberCreateForm(forms.ModelForm):
    # TODO 
    # custom validation of:
    #  - phonenumber (phonenumbers package, unique)
    #  - email (+unique)
    #  - legacy_id (unique)
    # 
    # clean:
    #  - phonenumber
    #  - username
    #  - password

    class Meta:
        model = Member
