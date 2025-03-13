# Create your views here.
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
#restrict users to login
from django.contrib.auth.decorators import login_required
# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

from myapp.credentials import LipanaMpesaPpassword, MpesaAccessToken
from myapp.models import Rental
from .forms import RentalForm
from requests.auth import HTTPBasicAuth



# Create your views here.
def home_page(request):
    context = {}
    return render(request, "index.html", context)

def book(request):
    return render(request, 'book.html')

def contact(request):
    return render(request, 'contact.html')

def login_page(request):
    """Display the appointment page"""
    return render(request, "accounts/login.html")



def logout_user(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    return redirect('myapp:login_page')  # Redirect user after logout

def login_page(request):
    """Login view"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('myapp:rent_house')  # Redirect to the homepage
        else:
            messages.error(request, "Invalid login credentials")
    
    return render(request, 'accounts/login.html')


def register(request):
    """Registration view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Account created successfully.")
                return redirect('myapp:login_page')  # Redirect to the login page after successful registration
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'accounts/register.html')



@login_required
def my_list(request):
    user_rentals = Rental.objects.filter(user=request.user)  # Filter bookings for the logged-in user
    return render(request, 'my_list.html', {'rentals': user_rentals})  


@login_required
def rent_house(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user  
            rental.save()
            messages.success(request, "House booking submitted successfully!")
            return redirect('myapp:payment_page')  # Redirect to payment page
        else:
            messages.error(request, "Invalid form submission. Please check your inputs.")
    else:
        form = RentalForm()
    
    return render(request, 'rent.html', {'form': form})


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required  # Restricts access to admin users
def admin_dashboard(request):
    rentals = Rental.objects.all()  # Fetch all rental applications
    return render(request, 'admin_dashboard.html', {'rentals': rentals})

# @staff_member_required
# def update_status(request, rental_id, status):
#     rental = Rental.objects.get(id=rental_id)
#     rental.status = status
#     rental.save()
#     messages.success(request, f"Application status updated to {status}.")
#     return redirect('admin_dashboard')  # Redirect to admin dashboard


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Rental

def update_status(request, rental_id, new_status):
    rental = get_object_or_404(Rental, id=rental_id)

    if new_status in ['Accepted', 'Rejected', 'Pending']:  # Only valid status updates
        rental.status = new_status
        rental.save()
        messages.success(request, f"Status updated to {new_status}!")
    else:
        messages.error(request, "Invalid status update.")

    return redirect('myapp:admin_dashboard')

# Adding the mpesa functions

def pay(request):
    """ Renders the form to pay """
    storage = messages.get_messages(request)
    for _ in storage: 
        pass
    return render(request, 'pay.html')



# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'EJwbmTGr391sTpntpVLLRZzv52oxwVSxXfa8qeaGKL4XxzLw'
    consumer_secret = 'UBIqynIJbG1tete0bDtMFnbhOAh0RUnfwqRFGfQIzl1ya7BqB21dWMFAQb2PzkKM'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth = HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


from django.shortcuts import render


def stk(request):
    """ Sends the stk push prompt """
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        stk_request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://yourdomain.com/callback-url/",
            "AccountReference": "KURentals",
            "TransactionDesc": "Pay for IT"
        }

        try:
            response = requests.post(api_url, json=stk_request, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and "ResponseCode" in response_data:
                messages.success(request, "Payment request sent successfully! Please check your phone.")
                return redirect("myapp:pay")
            else:
                error_message = response_data.get("errorMessage", "An error occurred.")
                messages.error(request, f"Payment failed: {error_message}")
                return redirect("myapp:pay")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect("myapp:pay")
    return redirect("myapp:pay")
