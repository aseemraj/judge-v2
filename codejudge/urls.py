from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'codejudge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^codejudge_django/', include('codejudge_django.urls', namespace="codejudge_django")),
    url(r'^admin/', include(admin.site.urls)),
)
