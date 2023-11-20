from django.contrib import admin
from .models import *




admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Remark)
admin.site.register(Certificate)