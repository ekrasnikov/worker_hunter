from django.contrib import admin

from .models import City, Vacancy, Speciality, Site, Url

admin.site.register(City)
admin.site.register(Vacancy)
admin.site.register(Speciality)
admin.site.register(Site)
admin.site.register(Url)
