from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('statement',views.statement,name='statement'),
    path('Income',views.Income,name="Income"),
    path('Expense',views.Expense,name="Expense"),
    path('howto',views.howto,name="howto"),
    path('report',views.report,name="report")
]