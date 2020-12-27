from django.contrib import admin
from .models import Result, Movie, Recommendation
# Register your models here.

admin.site.register(Result)
admin.site.register(Movie)
admin.site.register(Recommendation)
