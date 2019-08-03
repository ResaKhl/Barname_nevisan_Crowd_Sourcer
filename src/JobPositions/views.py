import datetime
import json
from django import forms
from uuid import UUID
from Main_and_Users.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render_to_response
from BarnameNevisan import jalali
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, Http404


# Create your views here.
import math
from Main_and_Users.models import User, User_Info, JobPosition, Job_Position_Offer, JobPosition_Transaction, Skill, \
    Chosen_Offer, Category, myFiles


def normalize_query(query):
    temp = query.split('+')
    terms = []
    for term in temp:
        terms += term.split(' ')
    return terms


def process_query(q, cat, project, hire, team, skills):
    terms = normalize_query(q)
    query = 'SELECT * FROM Main_and_Users_jobposition WHERE ('
    if terms.__len__() > 0:
        query += 'is_confirmed = 1 '
        for term in terms:
            query += 'AND title LIKE \'%' + term + '%\' '
            pass
        query += ' AND ('
    if project == '0' and hire == '0' and team == '0':
        query += '1=1))'
    else:
        if project == '1':
            query += '(job_type=\'' + str(JobPosition.Job_types[0][1]) + '\') OR '
        if hire == '1':
            query += '(job_type=\'' + str(JobPosition.Job_types[1][1]) + '\') OR '
        if team == '1':
            query += '(job_type=\'' + str(JobPosition.Job_types[2][1]) + '\') OR '
        query += '(1 = 0)))'  # if none of the types are selected, it will make it return nothing!
    # query += ' LIMIT 10 OFFSET ' + str(int(p_no) * 10);
    print(query)
    results = JobPosition.objects.raw(query)
    skill_models = []

    print(skills.__len__())
    for skill in skills:
        print("skill str is " + str(skill))
        skill_models += list(Skill.objects.filter(name=skill))
        print("skill size is " + str(skill_models.__len__()))

    if cat is not '':
        category = Category.objects.filter(id=cat)
        print("category length is " + str(category.__len__()))
        if category.__len__() > 0:
            print(category.first().skill)
            print(list(category.first().skill.all()).__len__())
            skill_models += list(category.first().skill.all())
            print(skill_models.__len__())

    final_results = []
    flag = False
    if skill_models.__len__() == 0:
        final_results = results
    else:
        for result in results:
            for resultSkill in result.skills.all():
                for skill in skill_models:
                    print(skill.name)
                    if skill.name == resultSkill.name:
                        final_results.append(result)
                        flag = True
                        break
                if flag:
                    break

    return final_results


def search(request, p_no, q, cat, p, h, team):
    myskills = Skill.objects.all()
    allskills = [skill.name for skill in myskills]
    don_t_use_side = False
    if request.user.is_anonymous():
        don_t_use_side = True
    skills = request.GET.get('skills', '')
    skills = skills.split('/')
    current_page = 0
    if p_no is not None:
        p_no = int(p_no)
        current_page = p_no + 1
    print(q)
    if q is not None:
        results = process_query(q, cat, p, h, team, skills)
    else:
        results = JobPosition.objects.all().filter(is_confirmed=1)[:50]  # show first 50 results

    if p_no is None:
        p_no = 0

    start_index = p_no * 10
    page_count = math.ceil(len(list(results)) / 10)
    page_range = range(1, page_count + 1)
    print(page_count)
    results = results[start_index: start_index + 10]
    for result in results:
        result.offerCount = get_offer_count(result)
        result.link = "/position/" + str(result.id)
        datetime.timedelta()
        result.time_diff = datetime.datetime.now() - result.timestamp
    categories = Category.objects.all()
    if cat is not None and cat != '':
        cat_html = int(cat)
    else:
        cat_html = 0
    if q is not None:
        query = q
    else:
        query = ""
    return render(request, "search.html", {
        "results": results,
        "page_count": page_count,
        "page_range": page_range,
        "categories": categories,
        "current_page_no": current_page,
        "don_t_use_side": don_t_use_side,
        "query": query,
        "cat": cat_html,
        "is_project": (p == '1'),
        "is_hire": (h == '1'),
        "is_teamwork": (team == '1'),
        "skills": skills,
        'mylist':allskills,
    })
# p_no, q, cat, p, h, team):


def get_user_info(request):
    user = request.user
    user_info = User_Info.objects.filter(user=user).first()
    return user_info


@login_required(login_url='/login/')
def me_as_employer(request):
    user_info = get_user_info(request)
    firstname = user_info.user.first_name
    lastname = user_info.user.last_name
    photo = User_Info.objects.get(user=user_info.user).photo
    projects = JobPosition.objects.filter(user=user_info).order_by('-timestamp')
    # print("user:" + user_info.id)
    for project in projects:
        addProjectInfo(project)
        offers = Job_Position_Offer.objects.filter(job_position=project)
        project.offerCount = offers.__len__()

    return render(request, "me-as-employer.html", {
        "projects": projects,
        "firstname": firstname,
        "lastname": lastname,
        "photo": photo,
    })


@login_required(login_url='/login/')
def me_as_employee(request):
    user = request.user
    user_info = User_Info.objects.filter(user=user).first()
    firstname = user_info.user.first_name
    lastname = user_info.user.last_name
    photo = User_Info.objects.get(user=user_info.user).photo
    offers = Job_Position_Offer.objects.filter(user=user_info).order_by('-offer_submit_Date_time')
    for offer in offers:
        offer_project = JobPosition.objects.filter(id=offer.job_position_id).first()
        addProjectInfo(offer_project)
        offer_project.offerCount = offers.__len__()
        add_offer_info(offer)
        offer.position = offer_project

    return render(request, "me-as-employee.html", {
        "offers": offers,
        "firstname": firstname,
        "lastname": lastname,
        "photo": photo,
    })


def get_offer_count(position):
    offers = Job_Position_Offer.objects.filter(job_position=position)
    return offers.__len__()


def get_is_paid(position):
    transactions = JobPosition_Transaction.objects.filter(jobPosition=position)

    person_count = 0
    for transaction in transactions:
        person_count += transaction.number_of_persons
    return person_count


def format_price(price):
    temp = int(price)
    price = ''
    first_time = True
    while temp > 0:
        if first_time:
            price = str(temp % 1000)
            while price.__len__() < 3 and temp >= 1000:
                price = '0' + price
            first_time = False
        else:
            temp_price = str(temp % 1000)
            while temp_price.__len__() < 3 and temp >= 1000:
                temp_price = '0' + temp_price
            price = (temp_price + ',' + price)
        print("price: " + price)
        temp = int(temp / 1000)
    return price


def get_user_work_count(user):
    count = 0
    for offer in Job_Position_Offer.objects.filter(user=user):
        if Chosen_Offer.objects.filter(Job_Position_Offer=offer).first() is not None:
            count += 1
    return count


def get_user_score(user):
    score = 0
    count = 0
    for offer in Job_Position_Offer.objects.filter(user=user):
        chosen_offer = Chosen_Offer.objects.filter(Job_Position_Offer=offer).first()
        if chosen_offer is not None:
            if chosen_offer.commentScore is not None:
                score += (chosen_offer.commentScore.score_Employer_to_Employee * 20)
                count += 1
    if count == 0:
        return 0
    return int(score / count)


def get_user_age(birthday):
    return int((datetime.datetime.now() - birthday).days / 365)


def addProjectInfo(position):
    close_date = jalali.Gregorian(position.closing_time.year, position.closing_time.month,
                                  position.closing_time.day)
    position.closing_time_year = close_date.persian_string("{0}")
    position.closing_time_month = close_date.persian_string("{1}")
    position.closing_time_day = close_date.persian_string("{2}")
    position.is_closed = datetime.datetime.now() > position.closing_time
    deadline = jalali.Gregorian(position.deadline.year, position.deadline.month, position.deadline.day)
    position.deadline_year = deadline.persian_string("{0}")
    position.deadline_month = deadline.persian_string("{1}")
    position.deadline_day = deadline.persian_string("{2}")
    timestamp = jalali.Gregorian(position.timestamp.year, position.timestamp.month,
                                  position.timestamp.day)
    position.timestamp_year = timestamp.persian_string("{0}")
    position.timestamp_month = timestamp.persian_string("{1}")
    position.timestamp_day = timestamp.persian_string("{2}")
    position.files = list(myFiles.objects.filter(job_position=position))


def add_offer_info(offer):
    chosen = Chosen_Offer.objects.filter(Job_Position_Offer=offer)
    if chosen.__len__() > 0:
        offer.is_chosen = True
        offer.user_photo = offer.user.photo
    else:
        offer.is_chosen = False
    # TODO
    start_date = jalali.Gregorian(offer.start_Date_time.year, offer.start_Date_time.month,
                                  offer.start_Date_time.day)
    offer.start_date_year = start_date.persian_string("{0}")
    offer.start_date_month = start_date.persian_string("{1}")
    offer.start_date_day = start_date.persian_string("{2}")
    offer.price = format_price(offer.price)
    submit_date = jalali.Gregorian(offer.offer_submit_Date_time.year, offer.offer_submit_Date_time.month,
                                   offer.offer_submit_Date_time.day)
    offer.offer_submit_Date_time_year = submit_date.persian_string("{0}")
    offer.offer_submit_Date_time_month = submit_date.persian_string("{1}")
    offer.offer_submit_Date_time_day = submit_date.persian_string("{2}")
    if str(offer.offer_submit_Date_time.minute).__len__() < 2:
        offer.offer_submit_Date_time_time = str(offer.offer_submit_Date_time.hour) + ":0" + str(
            offer.offer_submit_Date_time.minute)
    else:
        offer.offer_submit_Date_time_time = str(offer.offer_submit_Date_time.hour) + ":" + str(
            offer.offer_submit_Date_time.minute)
    offer.user_works = get_user_work_count(offer.user)
    offer.user_score = get_user_score(offer.user)
    offer.user.age = get_user_age(offer.user.birthday)


def normalizeUUID(posId):
    posId = posId.replace("/", "")
    return posId

def project(request, posId):
    user = request.user
    if user == None or user.is_anonymous():
        return offering(request, posId)
    user_id = request.user.id
    userid = str(user_id)
    user = User.objects.get(pk=userid)
    firstname = user.first_name
    lastname = user.last_name
    user_info = User_Info.objects.get(user=user)
    posId = normalizeUUID(posId)
    positions = JobPosition.objects.filter(id=posId)#.filter(is_confirmed=1)
    print(positions)
    if positions.__len__() > 0:
        position = positions[0]
        if position.user != user_info:
            return offering(request, posId)
        addProjectInfo(position)

        offers = Job_Position_Offer.objects.filter(job_position=position)
        position.accepted_offers = 0
        for offer in offers:
            add_offer_info(offer)
            if offer.is_chosen:
                position.has_chosen = True
                position.accepted_offers += 1
        position.offerCount = offers.__len__()
        position.personCount = get_is_paid(position)
        position.remain_persion_count = position.personCount - position.accepted_offers
        position.link = "/position/" + str(posId)
        user_info = get_user_info(request)
        firstname = user_info.user.first_name
        lastname = user_info.user.last_name
        photo = User_Info.objects.get(user=user_info.user).photo
        return render(request, "project-view.html", {
            "position": position,
            "offers": offers,
            "firstname": firstname,
            "lastname": lastname,
            "photo": photo,
        })
    raise Http404


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


# def date_handler(obj):
# if hasattr(obj, 'isoformat'):
# return obj.isoformat()
# else:
# raise TypeError(
# "Unserializable object {} of type {}".format(obj, type(obj))
# )


@login_required(login_url='/login/')
def get_user_data_for_offer(request, offer_id):
    offer_id = normalizeUUID(offer_id)
    user = get_user_info(request)
    count = 0
    offer = Job_Position_Offer.objects.filter(id=offer_id).first()
    print(offer)
    jobPosition = offer.job_position
    print(jobPosition.user.id)
    print(user.id)
    print(jobPosition.user.id != user.id)
    if jobPosition.user.id != user.id:
        return HttpResponse(json.dumps(None, default=date_handler), content_type="application/json")
    transactions = JobPosition_Transaction.objects.filter(jobPosition=jobPosition)
    for transaction in transactions:
        count += transaction.number_of_persons
    if Chosen_Offer.objects.filter(JobPosition=jobPosition).__len__() < count:
        result = {}
        result["mobile_no"] = user.mobile_number
        result["phone_no"] = user.phone_number
        result["email"] = user.user.email
        result["first"] = user.user.first_name
        result["last"] = user.user.last_name
        result["img"] = "/static/img/user-img.png"
        chosen = Chosen_Offer(Job_Position_Offer=offer, JobPosition=jobPosition)
        chosen.save()
        return HttpResponse(json.dumps(result, default=date_handler), content_type="application/json")
    return HttpResponse(json.dumps(None, default=date_handler), content_type="application/json")


@login_required(login_url='/login/')
def offering(request, posId):
    user = request.user
    user_anonymous = False
    try:
        UUID(posId)
    except ValueError:
        raise Http404
    try:
        position = JobPosition.objects.get(id=posId)
    except ObjectDoesNotExist:
        raise Http404
    addProjectInfo(position)
    this_position_files = myFiles.objects.filter(job_position=position)
    # print(this_position_files[0].filename.url)
    # print(this_position_files[0].filename.path)
    # print(this_position_files[0].filename.name)
    # print(this_position_files[0].title)
    start_date_form = New_Project_Date_form()
    user_score = get_user_score(position.user)
    user_works = get_user_work_count(position.user)
    offers_count = Job_Position_Offer.objects.filter(job_position=position).count()
    if user == None or user.is_anonymous():
        user_anonymous = True
        return render(request, "ProjectPage-freelancer.html", {
            'user_anonymous':user_anonymous,
            "position": position,
            'this_position_files': this_position_files,
            'user_score': user_score,
            'user_works': user_works,
            'offers_count': offers_count,
        })
        # REZAAAAAA: don't show offer form in this condition!
    user_info = User_Info.objects.get(user=user)
    if(position.is_confirmed is not True):
        raise Http404
    # if(user_info==position.user):
    #     return project(request, posId)
    firstname = user.first_name
    lastname = user.last_name
    photo = User_Info.objects.get(user=user).photo

    offered_done = False
    is_chosen = False
    job_position_offer1 = False
    position_pending1 = False


    offer = None
    this_job_position_offers = Job_Position_Offer.objects.filter(job_position=position , user=user_info)

    if(this_job_position_offers.__len__()!=0):
        chosen_offer = Chosen_Offer.objects.filter(Job_Position_Offer = this_job_position_offers[0])
        add_offer_info(this_job_position_offers[0])
        if(chosen_offer.__len__()!=0):
            is_chosen = True
            offered_done = True
            offer = this_job_position_offers[0]
        else:
            offered_done = True
            return render(request, 'ProjectPage-freelancer.html', {
                'user_score':user_score,
                'user_works':user_works,
                'offers_count':offers_count,
                'offer':this_job_position_offers[0],
                'offered_done':offered_done,
                'is_chosen':is_chosen,
                'firstname':firstname,
                'lastname':lastname,
                'photo':photo,
                'this_position_files':this_position_files,
                'position':position,
            })

    # this_user_prevoious_offers_forthisposition =
    position.link = "/position/" + str(posId)
    if (request.method == "POST" and not is_chosen and not offered_done):
        bad_year = False
        bad_month = False
        bad_day = False
        date_none = False
        form = New_Project_Date_form(request.POST)
        time_for_doing_is_none = False
        offered_price_is_none = False
        offered_price = request.POST['offered_price']
        time_for_doing = request.POST['time_for_doing']
        if(time_for_doing==''):
            time_for_doing_is_none = True
        if(offered_price==''):
            offered_price_is_none = True
        if (form.is_valid()):
            if (form.cleaned_data['year'] == '' or form.cleaned_data['month'] == '' or form.cleaned_data[
                'day'] == ''):
                date_none = True

            if (str(form.cleaned_data['year']).__len__() != 4 or int(form.cleaned_data['year'])<1390):
                bad_year = True
            if ((str(form.cleaned_data['month']).__len__() != 2 and str(
                    form.cleaned_data['month']).__len__() != 1) or int(form.cleaned_data['month']) > 12
                    or int(form.cleaned_data['month']) < 1):
                bad_month = True
            if ((str(form.cleaned_data['day']).__len__() != 2 and str(form.cleaned_data['day']).__len__() != 1) or int(form.cleaned_data['day']) > 32 or int(form.cleaned_data['day']) < 1):
                bad_day = True

            if (not time_for_doing_is_none and not offered_price_is_none and not date_none  and not bad_year and not bad_month and not bad_day):

                close_date = jalali.Persian(form.cleaned_data['year'], form.cleaned_data['month'],
                                            form.cleaned_data['day'])
                year = close_date.gregorian_string("{0}")
                month = close_date.gregorian_string("{1}")
                day = close_date.gregorian_string("{2}")
                a = datetime.datetime(int(year), int(month), int(day))
                first_time_for_starting = a

                job_position_offer = Job_Position_Offer(user=user_info, job_position=position, price=offered_price,
                                                        start_Date_time=first_time_for_starting, time_needed=time_for_doing)
                job_position_offer.save()
                return HttpResponseRedirect('/position_pending1/')

            else:
                return render(request, "ProjectPage-freelancer.html", {
                    'time_for_doing_is_none':time_for_doing_is_none,
                    'offered_price_is_none':offered_price_is_none,
                    'date_none':date_none,
                    'bad_year':bad_year,
                    'bad_month':bad_month,
                    'bad_day':bad_day,
                    'form': start_date_form,
                    "position": position,
                    'job_position_offer1': job_position_offer1,
                    'is_chosen': is_chosen,
                    'offered_done': offered_done,
                    'offer': offer,
                    'this_position_files': this_position_files,
                    'firstname': firstname,
                    'lastname': lastname,
                    'photo': photo,
                    'user_score': user_score,
                    'user_works': user_works,
                    'offers_count': offers_count,
                })
    return render(request, "ProjectPage-freelancer.html", {
        'form': start_date_form,
        "position": position,
        'job_position_offer1': job_position_offer1,
        'is_chosen':is_chosen,
        'offered_done':offered_done,
        'offer':offer,
        'this_position_files':this_position_files,
        'firstname': firstname,
        'lastname': lastname,
        'photo': photo,
        'user_score': user_score,
        'user_works': user_works,
        'offers_count': offers_count,
    })

@login_required(login_url='/login/')
def position_pending1(request):
    job_position_offer1 = 'true'
    position_pending1 = 'false'
    return render(request, 'activation-mail-sent.html', {
        'job_position_offer1': job_position_offer1,
        'position_pending1': position_pending1,
    })
    pass


@login_required(login_url='/login/')
def remove_position(request, posId):
    posId = normalizeUUID(posId)
    user_info = get_user_info(request)
    position = JobPosition.objects.get(id=posId, user=user_info)
    if position is not None:
        position.delete()
    else:
        raise Http404
    return me_as_employer(request)