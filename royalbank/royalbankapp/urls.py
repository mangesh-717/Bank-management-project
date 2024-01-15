from django.contrib import admin
from django.urls import path
from .views import *
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',login_form,name='loginform'),
    # path('operation/',login_required(operations),name='operations'),
    path('operations/',account,name='operations'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    
    path('loan/',loan_request_view,name='loan'),
    path('help/',help,name='help'),
    path('result/',result,name='results'),
    path('creadit_debit/',creadit_debit,name='creadit'),
    path('creadit_debit_form/',creadit_debit_form,name='creaditform'),
    path('About/',About,name='About'),
    path('carrier/',carrier,name='carrier')
]
