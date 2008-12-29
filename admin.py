from django.contrib import admin
from blogiix.models import Post, Comment, ShortUrl

class ShortUrlAdmin(admin.ModelAdmin):
	list_display = ('short_url', 'url')


# Tell admin which classes to look at		
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ShortUrl, ShortUrlAdmin)