# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.name)


class User_Info(models.Model):
    educational_level_types = (
        ('0', 'مدرک تحصیلی'),
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('کارشناسی', 'کارشناسی'),
        ('کارشناشی ارشد', 'کارشناشی ارشد'),
        ('دکتری', 'دکتری'),
    )
    city_types = (
        ('تهران', 'تهران'),
        ('اصفهان', 'اصفهان'),
        ('شیراز', 'شیراز'),
        ('یزد', 'یزد'),
        ('مشهد', 'مشهد'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)
    is_mobile_number_confirmed = models.BooleanField(default=False)
    mobile_number_confirmation_code = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=500, choices=city_types)
    last_educational_University = models.CharField(max_length=500, null=True)
    last_educational_level = models.CharField(max_length=500, choices=educational_level_types, null=True)
    sending_daily_email = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill)
    birthday = models.DateTimeField()
    activation_field = models.UUIDField(unique=True, default=None, editable=True, null=True)
    forgot_password_field_hash = models.UUIDField(unique=True, default=None, editable=True, null=True)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True,
                              default="photos/avatar_720-vflYJnzBZ.png")

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', blank=True, null=True)
    skill = models.ManyToManyField(Skill)

    def __str__(self):
        return str(self.name) + '(' + str(self.parent) + ')'


class Configuration(models.Model):
    key = models.CharField(primary_key=True, max_length=100)
    value = models.CharField(max_length=100)


class JobPosition(models.Model):
    Job_types = (
        ('پروژه', 'پروژه'),
        ('استخدام', 'استخدام'),
        ('هم‌تیمی', 'هم‌تیمی'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User_Info)
    title = models.CharField(max_length=500)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, max_length=100)
    closing_time = models.DateTimeField(null=True)
    job_type = models.CharField(max_length=500, choices=Job_types)
    is_special = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    can_be_done_remotely = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill)
    timestamp = models.DateTimeField(null=True)
    def __str__(self):
        return str(self.id) + '(' + str(self.title) + ')'


class myFiles(models.Model):
    title = models.CharField(max_length=500, null=True)
    filename = models.FileField(upload_to="", null=True, blank=True)
    job_position = models.ForeignKey(JobPosition)

    def __str__(self):
        return str(self.id) + '(' + str(self.job_position.id) + ')'

class Job_Position_Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_position = models.ForeignKey(JobPosition)
    user = models.ForeignKey(User_Info)
    price = models.FloatField()
    start_Date_time = models.DateTimeField(max_length=100)
    offer_submit_Date_time = models.DateTimeField(default=datetime.datetime.now)
    time_needed = models.IntegerField()

    def __str__(self):
        return str(self.id) + '(' + str(self.job_position.title) + ')'

class CommentScore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cooperation_status = models.CharField(max_length=30)
    score_Employer_to_Employee = models.IntegerField(null=True)
    comment_Employer_to_Employee = models.TextField(null=True)
    cooperation_desc_Employer_to_Employee = models.TextField(null=True)
    score_Employee_to_Employer = models.IntegerField(null=True)
    comment_Employee_to_Employer = models.TextField(null=True)
    cooperation_desc_Employee_to_Employer = models.TextField(null=True)


class Chosen_Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    JobPosition = models.ForeignKey(JobPosition)
    Job_Position_Offer = models.OneToOneField(Job_Position_Offer)
    commentScore = models.OneToOneField(CommentScore, null=True)

    def __str__(self):
        return str(self.id)

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    bank_account = models.CharField(max_length=20)
    date = models.DateTimeField(default=datetime.datetime.now)


class JobPosition_Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jobPosition = models.ForeignKey(JobPosition)
    transaction = models.OneToOneField(Transaction)
    number_of_persons = models.IntegerField()


# class Activation_mail_sent(models.Model):