from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import User, Comment
from django.utils import timezone
from django.core.paginator  import Paginator
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    user_list = User.objects.all().order_by('-id')
    paginator = Paginator(user_list, 5)
    page_number = request.GET.get('page')
    user_list = paginator.get_page(page_number)

    return render(request, 'users/index.html', {'page_obj': user_list})

@csrf_exempt
def search(request):
    term = request.GET.get('search', '')
    user_list = User.objects.filter(Q(user_fname__icontains=term) | Q(user_lname__icontains=term)).order_by('-id')

    paginator = Paginator(user_list, 5)
    page_number = request.GET.get('page')
    user_list = paginator.get_page(page_number)

    return render(request, 'users/index.html', {'page_obj': user_list})

@csrf_exempt
def add(request):
    return render(request, 'users/add.html')

@csrf_exempt
def processadd(request):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    position = request.POST.get('position')

    if request.FILES.get('image'):
        user_pic = request.FILES.get('image')
    else:
        user_pic = 'profile_pic/image.jpg'
    try:
        n = User.objects.get(user_email=email)
        # number already exists
        return render(request, 'users/add.html', {
            'error_message' : "Duplicated Email: " + email
        })
    except ObjectDoesNotExist:
        user = User.objects.create(user_email=email, user_fname=fname, user_lname=lname, user_position=position, user_image=user_pic)
        user.save()
        return HttpResponseRedirect('/users')
    
@csrf_exempt
@login_required(login_url='/users/login')
def detail(request, profile_id):
    try:
        user = User.objects.get(pk=profile_id)
        comments = Comment.objects.filter(user_id=profile_id)
        comments_count = Comment.objects.filter(user_id=profile_id).count()
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    return render(request, 'users/detail.html', {'users': user, 'comments': comments, 'comments_count' : comments_count })

@csrf_exempt
def delete(request, profile_id):
    User.objects.filter(id=profile_id).delete()
    return HttpResponseRedirect('/users')

@csrf_exempt
def addcomment(request):
    comment_text = request.POST.get('comment')
    user_id = request.POST.get('user_id')  
    name = request.POST.get('name')
    email = request.POST.get('email')
    comment = Comment.objects.create(user_id=user_id, body=comment_text, name=name, email=email) 
    comment.save()
    return HttpResponseRedirect(reverse('users:detail', args=(user_id,)))

@login_required(login_url='/users/login')
@permission_required('users.change_user', login_url='/users/login')
def edit (request, profile_id):
    try:
        user = User.objects.get(pk=profile_id)
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    return render(request, 'users/edit.html', {'users': user})
@csrf_exempt
def processedit(request, profile_id):
    user = get_object_or_404(User, pk=profile_id)
    profile_pic = request.FILES.get('image')
    try:
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        position = request.POST.get('position')
    except (KeyError, User.DoesNotExist):
        return render(request, 'users/detail.html', {
            'user':user,
            'error_message' : "Problem updating record",
        })
    else:
        user_profile = User.objects.get(id=profile_id)
        user_profile.user_fname = fname
        user_profile.user_lname = lname
        user_profile.user_email = email
        user_profile.user_position = position
        if profile_pic:
            user_profile.user_image = profile_pic
        user_profile.save()
        return HttpResponseRedirect(reverse('users:detail', args=(profile_id,)))
 
@csrf_exempt
def loginview(request):
    return render(request, 'users/login.html')

@csrf_exempt
def process(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:

        login(request, user)
        return HttpResponseRedirect('/users')
    else:

        return render(request, 'users/login.html', {
            'error_message' : "Log in Failed: Please check your username or password"
        })

def processlogout(request):
    logout(request)
    return HttpResponseRedirect('/users/login')


