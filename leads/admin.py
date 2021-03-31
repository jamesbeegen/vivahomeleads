from django.contrib import admin

from .models import Lead, QualTable

#REGISTER MODELS
admin.site.register(Lead)
admin.site.register(QualTable)
