from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}",
        "tag": "abcde"
    } for i in range(200)
]
ANSWERS = [
    {
        "id": i,
        "text": f"This is answer number {i}",
    } for i in range(200)
]

TAGS = {
    "abcde" : [1, 3, 5, 8, 9, 45, 89],
}

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
    page_obj = paginate(QUESTIONS, request)
    return render(request, "index.html", {"questions": page_obj})

def hot(request):
    questions = QUESTIONS[5:]
    page_obj = paginate(questions, request)
    return render(request, "hot.html", {"questions": page_obj})
def question(request, question_id):
    item = QUESTIONS[question_id]
    answers = [ANSWERS[question_id]]
    page_obj = paginate(answers, request)
    return render(request, "question_detail.html", {"question": item, "answers": page_obj})
def tag(request, question_tag):
    questions = [QUESTIONS[i] for i in TAGS[question_tag]]
    page_obj = paginate(questions, request)
    return render(request, "tag.html", {"questions": page_obj})
def ask(request):
    return render(request, "ask.html")

def signup(request):
    return render(request, "signup.html")

def settings(request):
    return render(request, "settings.html")

def login(request):
    return render(request, "login.html")