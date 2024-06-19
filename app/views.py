from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from app.models import Question, Answer, Tag, Profile, User
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from app.forms import LoginForm, RegisterForm, SettingsForm, QuestionForm, AnswerForm
from django.contrib import messages
# Create your views here.


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

def index(request):
    #page_obj = paginate(Question.objects.get_new(), request)
    listTag = []
    for item in Question.objects.get_new():
        tags = item.tag.all()
        print(tags)
        listTag.append((item, tags))
    page_obj = paginate(listTag, request)
    return render(request, "index.html",{"user": request.user, "questions": page_obj, "tags": Tag.objects.get_best(), "users": Profile.objects.get_best()})

def hot(request):
    listTag = []
    for item in Question.objects.get_hot():
        tags = item.tag.all()
        print(tags)
        listTag.append((item, tags))
    page_obj = paginate(listTag, request)
    return render(request, "hot.html", {"questions": page_obj, "tags": Tag.objects.get_best(), "users": Profile.objects.get_best()})

def question(request, question_id):
    if request.method == 'GET':
        answer_form = AnswerForm()
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            f = answer_form.save(commit=False)
            f.author = request.user
            f.question = Question.objects.get(id=question_id)
            f.save()
            if f:
                return redirect(reverse('question', args=(question_id,)))
            else:
                answer_form.add_error(field=None, error="Bad answer!")
    page_obj = paginate(Answer.objects.get_new(question_id), request)
    question = Question.objects.get(id=question_id)
    tags = question.tag.all()
    return render(request, "question_detail.html", {"answer_form": answer_form, "question": Question.objects.get(id=question_id), "tagsOfQuestion": tags, "answers": page_obj, "tags": Tag.objects.get_best(), "users": Profile.objects.get_best()})

def tag(request, question_tag):
    page_obj = paginate(Question.objects.get_by_tag(question_tag), request)
    return render(request, "tag.html", {"question_tag": question_tag, "questions": page_obj, "tags": Tag.objects.get_best(), "users": Profile.objects.get_best()})
def ask(request):
    if request.method == 'GET':
        question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            q = question_form.save(commit=False)
            q.author = request.user
            q.save()
            if q:
                return redirect(reverse('question', args=(q.id,)))
            else:
                question_form.add_error(field=None, error="Bad question!")

    return render(request, "ask.html", {"item": request.user, "form": question_form, "tags": Tag.objects.get_best(), "users": Profile.objects.get_best()})

@login_required
def settings(request):
    user = request.user
    if request.method == 'GET':
        data = {"username": user.username, "first_name": user.first_name, "last_name": user.last_name, "email": user.email}
        settings_form = SettingsForm(user, initial=data)
    if request.method == 'POST':
        settings_form = SettingsForm(data=request.POST, user=request.user, files=request.FILES)
        if settings_form.is_valid():
            user = settings_form.save()
            if user:
                return redirect(reverse('settings'))
            else:
                settings_form.add_error(field=None, error="Registration error!")

    return render(request, "settings.html", {"user": request.user, "form": settings_form, "tags": Tag.objects.get_best(), "users": Profile.objects.get_best()})
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))
def signup(request):
    if request.method == 'GET':
        user_form = RegisterForm()
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="Registration error!")
    return render(request, "signup.html", {'form': user_form, "tags": Tag.objects.get_best(), "users": Profile.objects.get_best()})
@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        print(7)
        if login_form.is_valid():
            print(6)
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                messages.error(request, 'username or password not correct')
        else:
            print(9)
    return render(request, "login.html", context={"form": login_form, "tags": Tag.objects.get_best(), "users": Profile.objects.get_best()})
