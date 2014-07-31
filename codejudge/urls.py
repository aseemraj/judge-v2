from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'codejudge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^judgev2/', include('judgev2.urls', namespace="judgev2")),
    url(r'^admin/', include(admin.site.urls)),
)
