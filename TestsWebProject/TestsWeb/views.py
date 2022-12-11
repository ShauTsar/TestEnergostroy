from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import createuserform, addQuestionform
from .models import Tests, QuesModel
from .models import Answer, Quiz
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    tests = Tests.objects.all()
    return render(request, 'HtmlViews/home.html', {'tests': tests})
# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'HtmlViews/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError: return render(request, 'HtmlViews/signupuser.html', {'form': UserCreationForm(),'error': 'Сотрудник уже зарегистрирован /n ' })
        else:
            return render(request, 'HtmlViews/signupuser.html', {'form': UserCreationForm(),'error': 'Пароли не совпадают' })

def testBelbina(request):
    quiz = Quiz.objects.all()
    return render(request, 'HtmlViews/testBelbina.html')


def addQuestion(request):
    if request.user.is_staff:
        form = addQuestionform()
        if (request.method == 'POST'):
            form = addQuestionform(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('/')
        context = {'form': form}
        return render(request, 'HtmlViews/addQuestion.html', context)
    else:
        return redirect('home')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('login')
        context = {
            'form': form,
        }
        return render(request, 'HtmlViews/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'HtmlViews/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('/')
def test(request):
    if request.method == 'POST':
        print(request.POST)
        questions=QuesModel.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'HtmlViews/result.html',context)
    else:
        questions=QuesModel.objects.all()
        context = {
            'questions':questions
        }
        return render(request,'HtmlViews/test.html',context)
