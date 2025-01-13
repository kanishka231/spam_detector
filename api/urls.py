from django.urls import path
from .views import LoginView, RegisterView, SearchByNameView, SearchByPhoneView, MarkSpamView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'), 
    path('search/name/', SearchByNameView.as_view(), name='search_name'),
    path('search/phone/', SearchByPhoneView.as_view(), name='search_phone'),
    path('mark-spam/<int:pk>/', MarkSpamView.as_view(), name='mark_spam'),
]
