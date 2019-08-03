"""BarnameNevisan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', 'Main_and_Users.views.register'),
    url(r'^login/$', 'Main_and_Users.views.my_login'),
    url(r'^user_profile/$', 'Main_and_Users.views.user_profile'),
    url(r'^activation_mail_sent/$', 'Main_and_Users.views.activation_mail_sent'),
    url(r'register/activate_user/(?P<activation_field>.+)/$', 'Main_and_Users.views.activate_user'),
    url(r'set_new_password/(?P<forgot_password_field_hash>.+)/$', 'Main_and_Users.views.set_new_password'),
    url(r'forgot_password_getting_email/$', 'Main_and_Users.views.forgot_password_getting_email'),
    url(r'forgot_password_email_sent/$', 'Main_and_Users.views.forgot_password_email_sent'),
    url(r'^$', 'Main_and_Users.views.show_main'),
    url(r'^search/((?P<p_no>\d+)/(?P<q>\w*)/(?P<cat>\d*)/(?P<p>\d)/(?P<h>\d)/(?P<team>\d))*$','JobPositions.views.search'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^position/(?P<posId>.+)$', 'JobPositions.views.project'),
    url(r'^me-employer/$', 'JobPositions.views.me_as_employer'),
    url(r'^me-employee/$', 'JobPositions.views.me_as_employee'),
    url(r'^getUserData/(?P<offer_id>.+)$', 'JobPositions.views.get_user_data_for_offer'),
    url(r'^new_project/$', 'Main_and_Users.views.show_new_project'),
    url(r'^new_project_get_skills/$', 'Main_and_Users.views.new_project_get_skills'),
    url(r'^comment/(?P<job_position_id>.+)/$', 'Main_and_Users.views.show_comment'),
    url(r'^show_comment_employee_to_employer/(?P<job_position_id>.+)/$', 'Main_and_Users.views.show_comment_employee_to_employer'),
    url(r'^file_testing/$', 'Main_and_Users.views.file_testing'),
    url(r'^get_comment/(?P<chosen_offer_id>.+)/$','Main_and_Users.views.get_comment'),
    url(r'^change_password/$', 'Main_and_Users.views.change_password'),

    url(r'^offering/(?P<posId>.+)$','JobPositions.views.offering'),
    url(r'^position_pending/$','Main_and_Users.views.position_pending'),
    url(r'^position_pending1/$', 'JobPositions.views.position_pending1'),

    url(r'^user_info/$', 'Main_and_Users.views.user_info'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^profile_pic_setting/$', 'Main_and_Users.views.profile_pic_setting'),
    url(r'^profile_editing/$', 'Main_and_Users.views.profile_editing'),
    url(r'^show_my_skills/$', 'Main_and_Users.views.show_my_skills'),

    url(r'^edit-project/(?P<posId>.+)/$', 'Main_and_Users.views.edit_project'),













    url(r'^logout/$', 'Main_and_Users.views.logout_view'),
    url(r'^about/$', 'Main_and_Users.views.about'),
    url(r'^contact/$', 'Main_and_Users.views.contact'),
    url(r'^privacy/$', 'Main_and_Users.views.privacy'),
    url(r'^hire/$', 'Main_and_Users.views.hire'),
    url(r'^how-to/$', 'Main_and_Users.views.how_to'),
    url(r'^trust/$', 'Main_and_Users.views.trust'),
    url(r'^law/$', 'Main_and_Users.views.law'),
    url(r'^position-remove/(?P<posId>.+)$', 'JobPositions.views.remove_position'),
]
