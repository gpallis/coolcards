from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template':'home.html'} ),
    url(r'^leaderboard/', 'leaderboard.views.leaderboard'),
    url(r'^vote/$', 'cards.views.vote'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)