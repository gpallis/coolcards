from django.contrib import admin
from cards.models import Card, Oracle
from activity.models import Vote
from django.utils.safestring import mark_safe
from django.core import urlresolvers

admin.site.register(Vote)

class CardAdmin(admin.ModelAdmin):
    def oracle_link(self,instance):
        link = urlresolvers.reverse('admin:cards_oracle_change', args=([instance.get_oracle_data().id]))
        return mark_safe("<a href='"+link+"'>"+instance.name+"</a>")
    readonly_fields = ('oracle_link',)
    search_fields = ['name']
    
class OracleAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
admin.site.register(Card,CardAdmin)
admin.site.register(Oracle,OracleAdmin)