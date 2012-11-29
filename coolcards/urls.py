from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cards.views.vote', name='home' ),
    url(r'^leaderboard/', 'leaderboard.views.leaderboard', name='leaderboard'),
    url(r'^vote/$', 'cards.views.vote', name='vote'),
    url(r'^faq/$', 'django.views.generic.simple.direct_to_template', {'template':'faq.html'}, name='faq'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
