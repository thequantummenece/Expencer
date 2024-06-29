from django.shortcuts import render, HttpResponse, redirect
from .models import IncomeM, ExpenseM
from django.contrib import messages
from django.db import models
import datetime
from datetime import datetime as dt
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User


def home(request):
    allcatI = IncomeM.objects.values('category').distinct()
    allcatE = ExpenseM.objects.values('category').distinct()
    cats = {'allcatI': allcatI, 'allcatE': allcatE}

    return render(request, 'core/home.html', cats)

def dashboard(request):
        return render(request,"core/dashboard.html")


def report(request):
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')

    if startdate and enddate:
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d').date()
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d').date()

        # Aggregating income by month
        dataI = IncomeM.objects.filter(date__range=[startdate, enddate]).extra(
            select={'month': "strftime('%%Y-%%m', date)"}).values('month').annotate(
            total_income=Sum('amount')).order_by('month')

        # Aggregating Expense by month
        dataE = ExpenseM.objects.filter(date__range=[startdate, enddate]).extra(
            select={'month': "strftime('%%Y-%%m', date)"}).values('month').annotate(
            total_expense=Sum('amount')).order_by('month')

        # Aggregating Expense by category
        dataEC = ExpenseM.objects.filter(date__range=[startdate, enddate]).values('category').annotate(
            total_expense=Sum('amount'))

        # Aggregating income by Category
        dataIC = IncomeM.objects.filter(date__range=[startdate, enddate]).values('category').annotate(
            total_income=Sum('amount'))

        # Preparing data for the charts
        data_pointsI = [{'label': item['month'], 'y': item['total_income']} for item in dataI]
        data_pointsE = [{'label': item['month'], 'y': item['total_expense']} for item in dataE]
        data_pointsCE = [{'label': item['category'], 'y': item['total_expense']} for item in dataEC]
        data_pointsCI = [{'label': item['category'], 'y': item['total_income']} for item in dataIC]

        context = {
            'data_pointsI': data_pointsI,
            'data_pointsE': data_pointsE,
            'data_pointsCE': data_pointsCE,
            'data_pointsCI': data_pointsCI,
        }

        return render(request, "core/report.html", context)


def get_combined_data(start_date, end_date):
    # Ensure dates are in datetime format
    start_date = dt.strptime(start_date, '%Y-%m-%d').date()
    end_date = dt.strptime(end_date, '%Y-%m-%d').date()

    # Retrieve expenses within date range and annotate with type 'expense'
    expenses = ExpenseM.objects.filter(date__range=(start_date, end_date)).annotate(
        type=V('EXPENSE', output_field=CharField())
    ).values('category', 'name', 'amount', 'date', 'type')

    # Retrieve incomes within date range and annotate with type 'income'
    incomes = IncomeM.objects.filter(date__range=(start_date, end_date)).annotate(
        type=V('INCOME', output_field=CharField())
    ).values('category', 'name', 'amount', 'date', 'type')

    # Combine both querysets
    combined_data = expenses.union(incomes).order_by('date')

    return combined_data


def statement(request):
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')

    if not start_date or not end_date:
        messages.add_message(request, messages.WARNING, 'Enter Your Dates!!')
        return render(request,'core/statement.html')

    combined_data = get_combined_data(start_date, end_date)
    return render(request, 'core/statement.html', {'combined_data': combined_data})


def Income(request):
    if request.method == 'GET':
        incomecat = request.GET.get('IncomeCategoryInput').strip().upper()
        incomename = request.GET.get('IncomeNameInput').strip().capitalize()
        incomeamount = request.GET.get('IncomeAmountInput')
        incomedate = request.GET.get('IncomeDateInput')

        if (len(incomecat) <= 2 or int(incomeamount) <= 0 or len(incomename) <= 2):
            messages.add_message(request, messages.WARNING, 'Please Enter Valid Values!!')
            return redirect('home')
        elif (str(datetime.date.today()) < incomedate):
            messages.add_message(request, messages.WARNING, 'Please Enter Valid Date!!')
            return redirect('home')

        Income1 = IncomeM.objects.create(category = incomecat, name = incomename,amount = incomeamount,date = incomedate)
        Income1.save()
        messages.add_message(request, messages.SUCCESS, 'Your Income Has been Added')
        return redirect('home')


def Expense(request):
    if request.method == 'GET':
        expensecat = request.GET.get('ExpenseCategoryInput').strip().upper()
        expensename = request.GET.get('ExpenseNameInput').strip().capitalize()
        expenseamount = request.GET.get('ExpenseAmountInput')
        expensedate = request.GET.get('ExpenseDateInput')

        if (len(expensecat)<=2 or int(expenseamount) <= 0 or len(expensename) <= 2):
            messages.add_message(request, messages.WARNING, 'Please Enter Valid Values!!')
            return redirect('home')
        elif(str(datetime.date.today())<expensedate):
            messages.add_message(request, messages.WARNING, 'Please Enter Valid Date!!')
            return redirect('home')

        Expense1 = ExpenseM.objects.create(category=expensecat, name=expensename, amount=expenseamount, date=expensedate)
        Expense1.save()
        messages.add_message(request, messages.SUCCESS, 'Your Expense Has been Added')
        return redirect('home')


def howto(request):
    return HttpResponse("How to Page Coming Soon")

def blogin(request):
    if request.method =="POST":
        #parameters for post
        loginusername = request.POST["lusername"]
        loginpassword = request.POST["Password"]

        user = authenticate(username = loginusername,password = loginpassword)
        if user is None:
            messages.error(request,"Invalid Credentials")
            return redirect('home')
        else:
            login(request, user)
            messages.success(request,"Successfully logged in ")
            return redirect('home')
    else:return HttpResponse("Lawda")

def blogout(request):
    if request.method == "GET":
        logout(request)
        messages.warning(request, "You have been logged out")
        return redirect('home')

def signin(request):
    if request.method == "POST":
        # parameters
        fname = request.POST['inputfname']
        lname = request.POST['inputlname']
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['inputemail']

        if(password2 == password):
            #creating user
            myuser = User.objects.create_user(username,email,password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.add_message(request, messages.SUCCESS, 'your account has been created')
            return redirect('home')

        else:
            messages.add_message(request, messages.ERROR, 'Error Signing in')
            return redirect('home')