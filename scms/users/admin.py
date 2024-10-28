from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import *


class UserModel(UserAdmin):
    list_display=['username','user_type']
# Register your models here.
admin.site.register(CustomUser, UserModel)
admin.site.register(Course)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subjects)
admin.site.register(Holidays)
admin.site.register(Timetable)
admin.site.register(Room)
admin.site.register(Registration)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Results)
admin.site.register(Note)
admin.site.register(Fess)
admin.site.register(Event)