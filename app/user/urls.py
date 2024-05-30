"""
URL mapping for the user API
"""
from django.urls import path
from user import views

app_name = 'user'  # used for the reverse mapping in the file "test_user_api.py"

url_patterns = [
    # used for the reverse mapping in the file "test_user_api.py"
    path('create/', views.CreateUserView.as_view(), name='create')
]
