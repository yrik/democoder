from django.contrib import admin

from core.models import (
    Article,
    User,
)


from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)

admin.site.register(Article)
admin.site.register(User)
