from django.contrib import admin

# Register your models here.
from .models import Company,HistoryData,PredictData

admin.site.register(Company)
admin.site.register(HistoryData)
admin.site.register(PredictData)