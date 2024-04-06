from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout  as logout_user
import re
from django.contrib import messages
#from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'index.html')

#functions to be perform in login page
@never_cache

def loginn(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    
    #storing values to variable by using http methods keyword post, get
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #form validation 
        if not username or not password:
            error_message = "Username and password are required."
            messages.error(request, error_message) 
        elif len(username) < 4:
            error_message = "Username must be at least 8 characters long."
            messages.error(request, error_message) 
        elif not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            error_message = "Password must contain both uppercase and lowercase letters."
            messages.error(request, error_message) 
        #validation ends
            
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['user_id']=user.id
                login(request, user)
                return redirect('homepage')
                #return HttpResponse("Hai User, Welcome!!")

            else:
                messages.error(request, 'Invalid user')
                return redirect('signup')
    return render(request, 'login.html')

#function for email vlidtion
def is_valid_email(email):
    # Regular expression for validating an email address
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

#functions to be perform in signup page
@never_cache
#@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signuppage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        #validation
        if not username or not password or not email:
            error_message = "Username, email and password are required."
            messages.error(request, error_message) 
            return redirect('signup')
        elif len(username) < 4:
            error_message = "Username must be at least 8 characters long."
            messages.error(request, error_message)
            return redirect('signup')
        if not is_valid_email(email):
            error_message = "Invalid email address."
            messages.error(request, error_message)
            return redirect('signup')
        elif not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            error_message = "Password must contain both uppercase and lowercase letters."
            messages.error(request, error_message)
            return redirect('signup')
        #validtion ends
        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.save()
            return redirect('login')
           
    else:
        return render(request, 'signup.html')



@login_required(login_url='login')
@never_cache
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.session.get('user_id', None)
    #getuser=User.objects.get(id=user_id)
    getuser = User.objects.filter(id=user_id).first()
    if not getuser:
        messages.error(request, 'User not found in session.')
        return redirect('login')
    else:
        return render(request, 'homepage.html', {'username': getuser.username}) 
    

def logout(request):

    logout_user(request)
    request.session.flush()
    return redirect('index')

def contact(request):
    return render(request,'contact.html')