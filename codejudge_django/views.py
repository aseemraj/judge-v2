from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from codejudge_django.models import Users, Problems, Solve
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session


# Create your views here.
@login_required
def index(request):
	return render(request, 'users/index.html')

def users_index(request):
	try:
		if request.session['username']:
			return HttpResponseRedirect("/codejudge_django")
		else:
			return render(request, 'users/login.html')
	except KeyError:
		return render(request, 'users/login.html')

def admin_index(request):
	try:
		if request.session['username'] and request.session['username']=='admin':
			return HttpResponseRedirect("admin_site/newprob/")
		else:
			return render(request, 'admin_site/index.html')
	except KeyError:
		context = RequestContext(request)
		error = False
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			if username=='admin':
				user = authenticate(username=username, password=password)
				if user != None:
					if user.is_authenticated():
						login(request, user)
						request.session['username']  = username
						request.session['password']  = password
						return HttpResponseRedirect("/codejudge_django/admin_site/newprob/")
					else:
						error = True
				else:
					error = True
			else:
				error = True
		return render(request, 'admin_site/index.html', {'error': error})

def register(request):
	context = RequestContext(request)
	registered = False

	if request.method == 'POST':
		username = request.POST['user_name']
		password = request.POST['pass_word']
		email = request.POST['email']

		user = User.objects.create_user(username, email, password)
		user.save()

		query = Users.objects.create(username = username)
		query.save()
		registered = True
		user = authenticate(username=username, password=password)
		login(request, user)
		request.session['username']  = username
		request.session['password']  = password
		return HttpResponseRedirect("/codejudge_django")

	else:
		return HttpResponse("Unsuccesful registration")

def user_login(request):
	try:
		if request.session['username']:
			return HttpResponseRedirect("/codejudge_django")
	except KeyError:
		context = RequestContext(request)
		error = False
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user != None:
				if user.is_authenticated():
					login(request, user)
					request.session['username']  = username
					request.session['password']  = password
					return HttpResponseRedirect("/codejudge_django")
				else:
					error = True
			else:
				error = True

		return render(request, 'users/login.html', {'error': error})

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
	error = True
	if request.method == "POST":
		email = request.POST['email']
		query = User.objects.get(username=request.session['username'])
		query.email = email
		query.save()
		error = False
	t = loader.get_template('users/account.html')
	c = RequestContext(request, {'error': error})
	return HttpResponse(t.render(c))

@login_required
def user_logout(request):
	del request.session['username']
	del request.session['password'] 
	logout(request)
	return HttpResponseRedirect("/codejudge_django/login")

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
