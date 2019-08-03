# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.forms import forms
from Main_and_Users.models import User_Info
from django.contrib.auth.models import *
from Main_and_Users.form_fields import *
from captcha.fields import CaptchaField
import re

__author__ = 'reza'

my_default_errors = {
    'required': '* لطفا این فیلد را پر نمایید.',
    'invalid': '* لطفا یک مقدار مناسب وارد نمایید.',
}
captcha_errors = {
    'required': '* لطفا کد امنیتی را وارد بفرمایید.',
    'invalid':'* لطفا کد امنیتی را عینا وارد بفرمایید.'
}
blank_error_massage = {
    'required' :'',
}
date_error = {
    'required': '* لطفا این فیلد را پر نمایید.',
    'invalid': '* لطفا با مقدار مناسب این فیلد را پر نمایید.'
}
educational_level_types = (
    ('0', 'مدرک تحصیلی'),
    ('دیپلم', 'دیپلم'),
    ('فوق دیپلم', 'فوق دیپلم'),
    ('کارشناسی', 'کارشناسی'),
    ('کارشناشی ارشد', 'کارشناشی ارشد'),
    ('دکتری', 'دکتری'),
)
city_types = (
    ('0', 'محل سکونت'),
    ('تهران', 'تهران'),
    ('اصفهان', 'اصفهان'),
    ('شیراز', 'شیراز'),
    ('یزد', 'یزد'),
    ('مشهد', 'مشهد'),
)
job_types =(
    ('0','نوع موقعیت'),
    ('پروژه','پروژه'),
    ('استخدام','استخدام'),
    ('هم‌تیمی','هم‌تیمی'),
)
scores_types = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)
class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=70, error_messages= my_default_errors, required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'پست الکترونیک' , 'style':"margin-top: 0px; direction: ltr;" , 'class':"form-control register-inputs", 'type':'email'}))
    password = Password(max_length=50, error_messages=my_default_errors, label='',widget=forms.PasswordInput(attrs={'placeholder': '(رمز عبور (حداقل ۶ کاراکتر' , 'style':"direction: ltr;"  , 'class':"form-control register-inputs", 'type':'password'}), required=True,)
    confirm_password = Password(max_length=50, error_messages=my_default_errors, label='',widget=forms.PasswordInput(attrs={'placeholder': ' تکرار رمز عبور' , 'style':"direction: ltr;"  , 'class':"form-control register-inputs", 'type':'password'}), required=True)
    first_name = forms.CharField(max_length=100, error_messages=my_default_errors, label='',required=True, widget=forms.TextInput(attrs={'placeholder': 'نام (فارسی)' , 'style':"direction: rtl;" , 'class':"form-control register-inputs" }))
    last_name = forms.CharField(max_length=100, error_messages=my_default_errors, label='',required=True, widget=forms.TextInput(attrs={'placeholder':  'نام خانوادگی (فارسی)' , 'style':"direction: rtl;"  , 'class':"form-control register-inputs" }))
    mobile_number = Mobile_Number(max_length=100, error_messages=my_default_errors, label='',required=True, widget=forms.TextInput(attrs={'placeholder': 'تلفن همراه (۱۱ رقم وارد کنید.)' , 'style':"direction: lrt;"  , 'class':"form-control register-inputs"}))
    last_educational_level = forms.ChoiceField(error_messages=my_default_errors, label='',
        widget=forms.Select(attrs={'class':"form-control register-inputs", 'style':"text-align-last:center;"}),
        choices=educational_level_types,
        required=True,
    )
    last_educational_University = forms.CharField(error_messages=my_default_errors, max_length=500, label='', widget=forms.TextInput(attrs={'placeholder':  'آخرین دانشگاه محل تحصیل (فارسی)'  , 'style':"direction: rtl;" , 'class':"form-control register-inputs"}))
    day = forms.CharField(required=False, max_length=2, label='تاریخ تولد:', error_messages='', widget=forms.TextInput(
        attrs={'placeholder': ' روز', 'style': "direction: ltr; width:60px; text-align-last:center; display:inline;",
               'class': "form-control register-inputs"}))
    month = forms.CharField(required=False, max_length=2, label='', error_messages='', widget=forms.TextInput(
        attrs={'placeholder': ' ماه', 'style': "direction: ltr; width:60px; text-align-last:center; display:inline;",
               'class': "form-control register-inputs"}))
    year = forms.CharField(required=False, max_length=4, label='', error_messages='', widget=forms.TextInput(
        attrs={'placeholder': ' (سال(چهار رقم', 'style': "direction: ltr; width:60px; text-align-last:center; display:inline;",
               'class': "form-control register-inputs"}))
    city = forms.ChoiceField(label='',
        widget=forms.Select(attrs={'class':"form-control register-inputs", 'style':"text-align-last:center;"}),
        choices=city_types,
        required=True,
    )
    captcha = CaptchaField(label='', required=True, error_messages=captcha_errors)
    sending_daily_email = forms.BooleanField(required=False,label='', widget=forms.CheckboxInput(attrs={'class':"form-control register-inputs", 'style':" position: relative;right: 26px !important; top: 14px !important;"}))
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        pw1 = cleaned_data.get("password")
        pw2 = cleaned_data.get("confirm_password")
        new_email = cleaned_data.get('email')
        previous_user = User.objects.filter(username=new_email)
        city = cleaned_data.get('city')
        year = cleaned_data.get('year')
        month = cleaned_data.get('month')
        day = cleaned_data.get('day')


        if previous_user.__len__() != 0:
            print(type(previous_user))
            raise ValidationError("* کاربر با ایمیل داده شده در سامانه موجود است.", code="password_confirmation_error")
        if pw1 != pw2:
            raise ValidationError("* رمز عبور و تکرار آن یکسان نمی‌باشد.", code="password_confirmation_error")
        if (str(year).__len__() != 4 or year=='' or int(year) < 1310):
            raise ValidationError("* لطفا سال را چهار رقمی  و معتبر وارد کنید.", code="password_confirmation_error")
        if str(month).__len__() > 2 or int(month) > 12 or int(month) <1:
            raise ValidationError("* لطفا ماه را حداکثر دو رقمی  و کمتر از ۱۲ وارد کنید.", code="password_confirmation_error")
        if str(day).__len__() > 2 or int(day) > 31 or int(day) <1 :
            raise ValidationError("* لطفا روز را حداکثر دو رقمی  و کمتر از ۳۲ وارد کنید.", code="password_confirmation_error")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=70, error_messages=my_default_errors,required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'پست الکترونیک' , 'style':"margin-top: 0px; direction: ltr;" , 'class':"form-control register-inputs", 'type':'email'}))
    password = Password(max_length=50, error_messages=my_default_errors, label='',widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور' , 'style':"direction: ltr;"  , 'class':"form-control register-inputs", 'type':'password'}), required=True)
    captcha = CaptchaField(label='', error_messages=captcha_errors, required=True)

class Forgot_password_getting_email(forms.Form):
    email = forms.EmailField(max_length=70, error_messages=my_default_errors,required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'پست الکترونیک' , 'style':"direction: ltr;" , 'class':"form-control register-inputs", 'type':'email'}))
    captcha = CaptchaField(label='', error_messages=captcha_errors, required=True)

class Set_new_password(forms.Form):
    password = Password(max_length=50, error_messages=my_default_errors, label='',widget=forms.PasswordInput(attrs={'placeholder': '(رمز عبور (حداقل ۶ کاراکتر' , 'style':"direction: ltr;"  , 'class':"form-control register-inputs", 'type':'password'}), required=True)
    confirm_password= Password(max_length=50, error_messages=my_default_errors, label='',widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور' , 'style':"direction: ltr;"  , 'class':"form-control register-inputs", 'type':'password'}), required=True)


    def clean(self):
        cleaned_data = super(Set_new_password, self).clean()
        pw1 = cleaned_data.get("password")
        pw2 = cleaned_data.get("confirm_password")
        if pw1 != pw2:
            raise ValidationError("* رمز عبور و تکرار آن یکسان نمی‌باشد.", code="password_confirmation_error");
        return cleaned_data

class File_handling(forms.Form):
    filename = forms.FileField(label='نام فایل',widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)

class New_Project_form_job_types_form(forms.Form):
    job_type = forms.ChoiceField(error_messages=my_default_errors, label='',
        widget=forms.Select(attrs={'class':"form-control register-inputs", 'style':"text-align-last:right; width: 150px"}),
        choices=job_types,
        required=True,
    )

class test_form(forms.Form):
    skills = forms.ChoiceField()


class My_Date_Form(forms.Form):
    day = Day(required=False, max_length=2, label='',error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' روز' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))
    month = Month(required=False, max_length=2, label='',error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' ماه' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))
    year = Year(required=False, max_length=4, label='',error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' سال' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))
            # class UserProfileRegisterForm(forms.ModelForm):
class New_Project_Date_form(forms.Form):
    day = forms.CharField(required=False, max_length=2, label='', error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' روز' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))
    month = forms.CharField(required=False, max_length=2, label='', error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' ماه' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))
    year = forms.CharField(required=False, max_length=4, label='', error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' سال' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))

class New_Project_Date_form1(forms.Form):
    day1 = forms.CharField(required=False, max_length=2, label='', error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' روز' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))
    month1 = forms.CharField(required=False, max_length=2, label='', error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' ماه' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))
    year1 = forms.CharField(required=False, max_length=4, label='', error_messages=date_error, widget=forms.TextInput(attrs={'placeholder': ' سال' , 'style':"direction: ltr; width:60px; text-align-last:center; display:inline;"  , 'class':"form-control register-inputs"}))


class Set_profile_pic(forms.Form):
    image = forms.ImageField(required=False, label='محل قرار دادن فایل')

class Edit_registrtaion(forms.Form):
    first_name = forms.CharField(max_length=100, error_messages=my_default_errors, label='', required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'نام (فارسی)', 'style': "direction: rtl;",
                                                               'class': "form-control register-inputs"}))
    last_name = forms.CharField(max_length=100, error_messages=my_default_errors, label='', required=False,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'نام خانوادگی (فارسی)', 'style': "direction: rtl;",
                                           'class': "form-control register-inputs"}))
    mobile_number = Mobile_Number(max_length=100, error_messages=my_default_errors, label='', required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'تلفن همراه ،۱۱ رقم وارد کنید.',
                                                                'style': "direction: ltr;",
                                                                'class': "form-control register-inputs"}))
    last_educational_level = forms.ChoiceField(error_messages=my_default_errors, label='',
                                               widget=forms.Select(attrs={'class': "form-control register-inputs",
                                                                          'style': "text-align-last:center;"}),
                                               choices=educational_level_types,
                                               required=False,
                                               )
    last_educational_University = forms.CharField(error_messages=my_default_errors, max_length=500, label='',
                                                  widget=forms.TextInput(
                                                      attrs={'placeholder': 'آخرین دانشگاه محل تحصیل (فارسی)',
                                                             'style': "direction: rtl;",
                                                             'class': "form-control register-inputs"}), required=False)
    day = forms.CharField(required=False, max_length=2, label='تاریخ تولد:', error_messages='', widget=forms.TextInput(
        attrs={'placeholder': ' روز', 'style': "direction: ltr; width:60px; text-align-last:center; display:inline;",
               'class': "form-control register-inputs"}))
    month = forms.CharField(required=False, max_length=2, label='', error_messages='', widget=forms.TextInput(
        attrs={'placeholder': ' ماه', 'style': "direction: ltr; width:60px; text-align-last:center; display:inline;",
               'class': "form-control register-inputs"}))
    year = forms.CharField(required=False, max_length=4, label='', error_messages='', widget=forms.TextInput(
        attrs={'placeholder': ' (سال(دو رقم',
               'style': "direction: ltr; width:60px; text-align-last:center; display:inline;",
               'class': "form-control register-inputs"}))
    city = forms.ChoiceField(label='',
                             widget=forms.Select(
                                 attrs={'class': "form-control register-inputs", 'style': "text-align-last:center;"}),
                             choices=city_types,
                             required=False,
                             )
    # image = forms.ImageField(required=False, label='محل قرار دادن فایل')
    sending_daily_email = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(
        attrs={'class': "",
               'style': " position: relative; right: 50px !important; top: 9px !important;"}))

    def clean(self):
        cleaned_data = super(Edit_registrtaion, self).clean()
        pw1 = cleaned_data.get("password")
        pw2 = cleaned_data.get("confirm_password")
        new_email = cleaned_data.get('email')
        year = cleaned_data.get('year')
        month = cleaned_data.get('month')
        day = cleaned_data.get('day')

        if pw1 != pw2:
            raise ValidationError("* رمز عبور و تکرار آن یکسان نمی‌باشد.", code="password_confirmation_error")
        if (str(year).__len__() != 4 or year == '' or int(year) < 1310):
            raise ValidationError("* لطفا سال را چهار رقمی و معتبر وارد کنید.", code="password_confirmation_error")
        if (month!='' and (str(month).__len__() > 2 or int(month) > 12 or int(month) < 1)):
            raise ValidationError("* لطفا ماه را حداکثر دو رقمی  و کمتر از ۱۲ وارد کنید.",
                                  code="password_confirmation_error")
        if (day!='' and (str(day).__len__() > 2 or int(day) > 31 or int(day) < 1)):
            raise ValidationError("* لطفا روز را حداکثر دو رقمی  و کمتر از ۳۲ وارد کنید.",
                                  code="password_confirmation_error")
        return cleaned_data


class scoress(forms.Form):
    scores = forms.ChoiceField(error_messages=my_default_errors, label='',
                                              widget=forms.Select(attrs={'class': "form-control register-inputs",
                                                                         'style': "text-align-last:center;"}),
                                              choices=scores_types,
                                              required=False,
                                              )
class Change_Password(forms.Form):
    old_password = Password(max_length=50, error_messages=my_default_errors, label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'رمز عبور قبلی', 'style': "direction: ltr;",
               'class': "form-control register-inputs", 'type': 'password'}), required=True, )
    password = Password(max_length=50, error_messages=my_default_errors, label='', widget=forms.PasswordInput(
        attrs={'placeholder': '(رمز عبور (حداقل ۶ کاراکتر', 'style': "direction: ltr;",
               'class': "form-control register-inputs", 'type': 'password'}), required=True, )
    confirm_password = Password(max_length=50, error_messages=my_default_errors, label='', widget=forms.PasswordInput(
        attrs={'placeholder': ' تکرار رمز عبور', 'style': "direction: ltr;", 'class': "form-control register-inputs",
               'type': 'password'}), required=True)

    def clean(self):
        cleaned_data = super(Change_Password, self).clean()
        pw1 = cleaned_data.get("password")
        pw2 = cleaned_data.get("confirm_password")
        if pw1 != pw2:
            raise ValidationError("* رمز عبور و تکرار آن یکسان نمی‌باشد.", code="password_confirmation_error")