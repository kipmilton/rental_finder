from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('accounts/login/', views.login_page, name='login_page'),
    path('accounts/register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('rent/', views.rent_house, name='rent_house'),
    path('contact/', views.contact, name='contact'),
    path('my_list/', views.my_list, name='my_list'),
    path('pay/', views.pay, name='payment_page'),
    path('stk/', views.stk, name='stk'),
    path('rent/', views.rent_house, name='rent_house'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_status/<int:rental_id>/<str:new_status>/', views.update_status, name='update_status'),
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

