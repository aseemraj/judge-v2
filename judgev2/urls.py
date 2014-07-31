from django.conf.urls import patterns, url
from judgev2 import views

urlpatterns = patterns('',
	url(r'^users/$', views.users_index, name='index'),
	url(r'^admin_site/$', views.admin_index, name='index'),
	url(r'^register/$', views.register, name='index'),
	url(r'^problems/$', views.problems, name='index'),
	url(r'^login/$', views.user_login, name='index'),
	url(r'^$', views.index, name='index'),
	url(r'^logout/$', views.user_logout, name='index'),
	url(r'^leaderboard/$', views.leaderboard, name='index'),
	# url(r'^/$', views.user_logout, name='index'),
	url(r'^submission/$', views.submission, name='index'),
	url(r'^account/$', views.account, name='index'),
	url(r'^change_password/$', views.change_password, name='index'),
 	url(r'^change_email/$', views.change_email, name='index'),
	url(r'^problems/(?P<problem_id>\d+)/$', views.details, name='details'),
)