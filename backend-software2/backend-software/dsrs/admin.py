from django.contrib import admin
from .models import Currency, DSR, Resource, Territory, File_dir
# Register your models here.


admin.site.register(DSR)

admin.site.register(Resource)

admin.site.register(Territory)

admin.site.register(Currency)

admin.site.register(File_dir)