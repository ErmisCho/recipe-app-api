"""
URL mapping for the user API
"""
from django.urls import path
from user import views

app_name = 'user'  # used for the reverse mapping in the file "test_user_api.py"

urlpatterns = [
    # used for the reverse mapping in the file "test_user_api.py"
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManagerUserView.as_view(), name='me'),
]
