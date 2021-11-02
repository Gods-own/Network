from django.contrib import admin
from .models import User, Posts, Liked, Comments, Following, NoFollows

# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Liked)
admin.site.register(Comments)
admin.site.register(Following)
admin.site.register(NoFollows)