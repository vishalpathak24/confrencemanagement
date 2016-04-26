from django.contrib import admin
from confrence.models import Confrence, Reviewr, Topic, Author, Upload, Submission, PaperSubmission, PosterSubmission

# Register your models here.
admin.site.register(Confrence)
admin.site.register(Reviewr)
admin.site.register(Topic)
admin.site.register(Author)
admin.site.register(Upload)
admin.site.register(Submission)
admin.site.register(PaperSubmission)
admin.site.register(PosterSubmission)
