import re
from django import forms
from django.core.exceptions import ValidationError

__author__ = 'saeed'


class MyDateField(forms.Field):
    def to_python(self, value):
        match_date = re.match('^(\d{2})/(\d{2})/(\d{4})$', value)
        if match_date:
            s = value.split("/")
            return s[2] + '-' + s[1] + '-' + s[0]

    def validate(self, value):
        super(MyDateField, self).validate(value)

        match_date = re.match('^(\d{2})/(\d{2})/(\d{4})$', value)
        if not match_date:
            raise ValidationError('Date should be in DD/MM/YYYY format.', code='invalid_date')


class Password(forms.CharField):
    def validate(self, value):
        super(Password, self).validate(value)
        if len(value) < 6:
            raise ValidationError('* رمز عبور بایستی حداقل ۶ رقم باشد.', code='invalid')

class Mobile_Number(forms.CharField):
    def validate(self, value):
        super(Mobile_Number, self).validate(value)
        if len(value) != 11:
            raise ValidationError('* تلفن همراه باید ۱۱ رقمی باشد.', code='invalid')
    pass

class Year(forms.CharField):
    def validate(self, value):
        super(Year, self).validate(value, )
        if (len(value) != 4 or int(value) < 1310):
            raise ValidationError('* سال را ۴ رقمی و معتبر وارد کنید.', code='invalid')

class Month(forms.CharField):
    def validate(self, value):
        super(Month, self).validate(value)
        if (len(value) != 2 or int(value) > 12):
            raise ValidationError('* ماه را دو رقمی و کمتر از ۱۲ وارد کنید.', code='invalid')

class Day(forms.CharField):
    def validate(self, value):
        super(Day, self).validate(value)
        if (len(value) != 4 or int(value) > 32):
            raise ValidationError('* روز را چهار رقمی  و معتبر وارد کنید.', code='invalid')


class UpdatePassword(forms.CharField):
    def validate(self, value):
        super(UpdatePassword, self).validate(value)
        if len(value) < 6 and len(value) != 0:
            raise ValidationError('Password must be at least 6 characters long.', code='invalid')