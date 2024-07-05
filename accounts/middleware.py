from django.shortcuts import redirect
from django.urls import reverse, resolve

class PepyAuthMiddleware:
   def __init__(self, get_response):
       self.get_response = get_response

   def __call__(self, request):
       # List of paths that require authentication
       protected_paths = (
           '/',
           '/explore/',
           '/search/',
           '/search/',
           '/accounts/auth/change-password/'
       )

       # Check if the request path is in the protected paths
       if request.path in protected_paths:
           print(request.path)
           # Check if the user is authenticated
           if not request.user.is_authenticated:
               # Redirect to login page if not authenticated
               return redirect(reverse('user_login'))

       # Continue processing the request
       response = self.get_response(request)
       return response