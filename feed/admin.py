from django.contrib import admin
from feed.models import *
# Register your models here.

admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(Comment)
admin.site.register(Reaction)