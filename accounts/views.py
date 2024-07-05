from django.shortcuts import render, redirect
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
import time

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
    
        # Check if a user with the provided username exists
        # if not Profile.objects.filter(email=username).exists():
        #     # Display an error message if the username does not exist
        #     messages.error(request, 'Sorry, your email was incorrect. Please double-check your email.')
        #     return redirect('user_login')
         
        # Authenticate the user with the provided username and password
        user = authenticate(request, username=username, password=password)
         
        if user is not None:
            if user.is_active:
                # Log in the user and redirect to the home page upon successful login
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Account is inactive.')
        else:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid username or password.")
        
    return render(request, 'accounts/auth/login.html', {})

def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get('user_name_full')
        username = request.POST.get('user_name_short')
        email = request.POST.get('user_email')
        password = request.POST.get('user_password')
        password_cnf = request.POST.get('user_password_cnf')

        print("\nNew User registration", time.time())
        print("Name:", full_name)
        print("Username:", username)
        print("Email:", email, end="\n\n")

        # 1 - check if username follows the valid regex
        regex = "^[A-Za-z0-9_][A-Za-z0-9_.]{3,28}[A-Za-z0-9_]$"
        if not re.match(regex, username):
            messages.error(request, 'Username can only contains alphabets, underscore or dots, and must have alteast 4 characters.')
            return redirect('user_register')
        
        # 2 - check if password is not empty and is valid password
        elif not password or not password_cnf or (password != password_cnf) or (len(password) < 7):
            messages.error(request, 'Sorry, Choose a strong password.')
            return redirect('user_register')
        
        # 3 - Check if the username with the provided email exists
        elif Profile.objects.filter(email=email).exists():
            # Display an error message if the email exists
            messages.error(request, 'Email already exists, try logging in.')
            return redirect('user_register')
        
        # 4 - Check if the username with the provided username exists
        elif Profile.objects.filter(username=username).exists():
            # Display an error message if the username exists
            messages.error(request, 'Username already exists, try logging in.')
            return redirect('user_register')
        
        user = Profile.objects.create_user(email=email, username=username, full_name=full_name)
        user.set_password(password)
        user.save()
        login(request, user)
        update_session_auth_hash(request, user)  # Important to keep the user logged in
        messages.success(request, 'Profile successfully created!')
        return redirect('home')
        
    return render(request, 'accounts/auth/register.html', {})

def check_username(request):
    if request.method == "POST":
        username = request.POST.get('user_name_short')

        regex = "^[A-Za-z0-9_][A-Za-z0-9_.]{3,28}[A-Za-z0-9_]$"
        if (not username) or (not re.match(regex, username)):
            # messages.error(request, 'Invalid username')
            return JsonResponse({'success': False,'message': 'Invalid username'}, status=405)

        # Check if a user with the provided username exists
        if Profile.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            # messages.error(request, 'Username already exists')
            return JsonResponse({'success': False,'message': 'Username not available!'}, status=406)
        return JsonResponse({'success': True,'message': 'Username available!'}, status=200)
    return redirect('user_register')

def user_forget(request):
    return render(request, 'accounts/auth/forgot.html', {})

@login_required
def user_logout(request):
    logout(request)
    return redirect("user_login")

# from rest_framework.response import Response
# from rest_framework.request import Request
# from feed.serializers import ProfileBasicSerializer
# from rest_framework.decorators import api_view

# @api_view(('GET','POST',))   
# def profile_followers(request, username):
#     if request.method == 'POST' and request.user.is_authenticated:
#         try:
#             get_user = Profile.objects.get(username = username)
#             user_followers = Profile.objects.filter(following=get_user)
#             serializer = ProfileBasicSerializer(user_followers, many=True)
#             return Response(serializer.data)
#         except Profile.DoesNotExist:
#             return render(request, '404.html', {}, status=404)
#     else:
#         return redirect(f"/{username}/")
    
# @api_view(('GET','POST',))   
# def profile_following(request, username):
#     try:
#         get_user = Profile.objects.get(username = username)
#         if request.method == 'POST' and request.user.is_authenticated:
#             user_following = get_user.following.all()
#             serializer = ProfileBasicSerializer(user_following, many=True)
#             return Response(serializer.data)
#         else:
#             return redirect(f"/{get_user.username}/")
#     except Profile.DoesNotExist:
#         return render(request, '404.html', {}, status=404)

@csrf_exempt
def user_follow(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            userprofile = Profile.objects.get(username=username)
            if request.user.following.filter(username=username).exists():
                request.user.following.remove(userprofile)
                return JsonResponse({'success': True, 'message': 'Profile Unfollowed!'}, status=200)
            else:
                request.user.following.add(userprofile)
                return JsonResponse({'success': True, 'message': 'Profile Followed!'}, status=200)
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Profile does not exist!'}, status=404)
    return redirect('home')