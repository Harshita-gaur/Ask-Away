
from django.contrib import admin
from .models import FAQ,CategoryFAQ,Feedback,TagFAQ
# Register your models here.
admin.site.register(FAQ)
admin.site.register(CategoryFAQ)
admin.site.register(Feedback)
admin.site.register(TagFAQ)