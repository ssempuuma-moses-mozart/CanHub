from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(FollowersCount)
admin.site.register(Like)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(GroupPost)
admin.site.register(GroupComment)