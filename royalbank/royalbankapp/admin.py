from django.contrib import admin
from .models import Bankusers,CardApplication,LoanRequest,HelpData
# Register your models here.
admin.site.register(Bankusers)
admin.site.register(CardApplication)
admin.site.register(LoanRequest)
admin.site.register(HelpData)