from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from judgev2.models import Users, Problems, Solve
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import json

# Create your views here.
def index(request):
	try:
		if request.session['username']:
			return render(request, 'users/index.html')
		else:
			return render(request, 'users/login.html')
	except KeyError:
		return render(request, 'users/login.html')

def users_index(request):
	try:
		if request.session['username']:
			return HttpResponseRedirect("/judgev2")
		else:
			return render(request, 'users/login.html')
	except KeyError:
		return render(request, 'users/login.html')

def admin_index(request):
	try:
		if request.session['username']:
			if request.session['username']=='admin':
				return HttpResponseRedirect("newprob/")
			else:
				del request.session['username']
				del request.session['password']
				logout(request)
				return render(request, 'admin_site/index.html', {'error': 2})
		else:
			return render(request, 'admin_site/index.html', {'error': 2})
	except KeyError:
		context = RequestContext(request)
		error = 1
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			if username=='admin' and password=='pclub2014dhpc':
				request.session['username']  = username
				request.session['password']  = password
				return HttpResponseRedirect("/judgev2/admin_site/newprob/")
			else:
				error = 1
		else:
			error = 2
		return render(request, 'admin_site/index.html', {'error': error})

def newprob(request):
	try:
		if request.session['username']:
			if request.session['username']=='admin':
				return render(request, 'admin_site/newprob.html')
			else:
				return HttpResponseRedirect("/judgev2/admin_site/")
		else:
			return HttpResponseRedirect("/judgev2/admin_site/")
	except KeyError:
		return HttpResponseRedirect("/judgev2/admin_site/")

def adminlogout(request):
	try:
		if request.session['username']:
			del request.session['username']
		return HttpResponseRedirect("/judgev2/admin_site/")
	except KeyError:
		return HttpResponseRedirect("/judgev2/admin_site/")

def adminsubmit(request):
	try:
		if request.session['username']:
			if request.session['username']=='admin':
				context = RequestContext(request)
				if request.method == 'POST':
					probname = request.POST['probname']
					probstat = request.POST['probstat']
					testin = request.POST['testin']
					testout = request.POST['testout']
					points = request.POST['points']
					timelimit = request.POST['timelimit']
					query = Problems.objects.filter(problem_name=probname)
					if query:
						return render(request, 'admin_site/newprob.html', {'error': 1})
					else:
						problem = Problems.objects.create(problem_name=probname, problem_statement=probstat, input=testin, solvedby=0, output=testout, points=points, time=timelimit)
						problem.save()
					return render(request, 'admin_site/newprob.html', {'error': 2})
				else:
					return render(request, 'admin_site/newprob.html', {'error': 3})
			else:
				return HttpResponseRedirect("/judgev2/admin_site/logout/")
		else:
			return HttpResponseRedirect("/judgev2/admin_site/")
	except KeyError:
		return HttpResponseRedirect("/judgev2/admin_site/")
			

def register(request):
	context = RequestContext(request)
	errors = False
	if request.method == 'POST' and request.is_ajax():
		username = request.POST['user_name']
		password = request.POST['pass_word']
		email = request.POST['email']
		query = User.objects.filter(username=username)
		if query:
			errors = True
		else:
			user = User.objects.create_user(username, email, password)
			user.save()
			query = Users.objects.create(username = username)
			query.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			request.session['username']  = username
			request.session['password']  = password
			print request.session['username']
			
		return HttpResponse(json.dumps({'errors': errors}),content_type='application/json')
	else:
		raise Http404


def user_login(request):
	try:
		if request.session['username']:
			return HttpResponseRedirect("/judgev2")
	except KeyError:
		context = RequestContext(request)
		error = False
		if request.method == 'POST' and request.is_ajax():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user != None:
				if user.is_authenticated():
					login(request, user)
					request.session['username']  = username
					request.session['password']  = password
					return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
				else:
					error = True
					return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
			else:
				error = True
				return HttpResponse(json.dumps({'errors': error}),content_type='application/json')

		return render(request, 'users/login.html')

@login_required
def change_password(request):
	error = 0
	if request.method == "POST":
		old_password = request.POST['old_password']
		new_password = request.POST['new_password']
		user = authenticate(username=request.session['username'], password=old_password)
		if user is not None:
			query = User.objects.get(username=request.session['username'])
			query.set_password(new_password)
			query.save()
			error = 1
			t = loader.get_template('users/account.html')
			c = RequestContext(request, {'error': error})
			return HttpResponse(t.render(c))
		else:
			error = 2
			t = loader.get_template('users/account.html')
			c = RequestContext(request, {'error': error})
			return HttpResponse(t.render(c))
			

@login_required
def change_email(request):
	error = 3
	if request.method == "POST":
		email = request.POST['email']
		query = User.objects.get(username=request.session['username'])
		query.email = email
		query.save()
		error = 4
	t = loader.get_template('users/account.html')
	c = RequestContext(request, {'error': error})
	return HttpResponse(t.render(c))

@login_required
def user_logout(request):
	del request.session['username']
	del request.session['password'] 
	logout(request)
	return HttpResponseRedirect("/judgev2/login")

@login_required
def leaderboard(request):
	users = Users.objects.order_by('score')
	return render(request, 'users/leaderboard.html', {'users': users})

@login_required
def submission(request):
	return render(request, 'users/submission.html')

@login_required
def account(request):
	return render(request, 'users/account.html')

@login_required
def problems(request):
	problems = Problems.objects.order_by('id')
	return render(request, 'problems/index.html', {'problems': problems})

@login_required
def details(request, problem_id):
    prob = get_object_or_404(Problems, id=problem_id)
    # context = RequestContext(request)
	# if request.method == 'POST':
	# 	username = request.session['username']
	# 	language = request.POST['language']
	# 	code = request.POST['code']
	# 	query = Solve.objects.create(problem_id = prob.id, username = username, solution = code, language = language)
	# 	query.save()
    return render(request, 'problems/details.html', {'prob': prob})