from django.contrib import admin
from accounts.models import Profile, ChangeUsername
from django.utils.html import format_html

class ProfileAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" style="aspect-ratio: 1;object-fit: cover;border-radius: 50%;" />'.format(obj.profile_img.url))

    image_tag.short_description = 'Profile Image'

    list_display = ('image_tag', 'full_name', 'username', 'email',)
    list_display_links = ('image_tag', 'full_name',)
    ordering  = ('username',)
    
# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ChangeUsername)