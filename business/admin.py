from django.contrib import admin
from business import models
# Register your models here.


admin.site.register(models.Tag)
admin.site.register(models.Done)
admin.site.register(models.User)
admin.site.register(models.Task)