from django.contrib import admin
from .models import CustomUser, Ibadat, Scale, IbadatItem

admin.site.register(CustomUser)
admin.site.register(Ibadat)
admin.site.register(Scale)
admin.site.register(IbadatItem)