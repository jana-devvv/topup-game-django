from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Main Views
    path('', views.main_view, name='main'),
    path('game/<int:id>/', views.package_view, name='package'),
    path('transaction/<int:id>/', views.transaction_view, name='transaction'),
    path('payment/<int:transaction_id>/', views.payment_view, name='payment')
]
