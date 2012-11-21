from django.contrib import admin
from cards.models import Card, Oracle
from activity.models import Vote

admin.site.register(Card)
admin.site.register(Oracle)
admin.site.register(Vote)
