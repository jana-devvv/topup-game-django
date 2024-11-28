from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Game, Package, Transaction, Payment

# Create your views here.
def register_view(req):
    if req.method == 'POST':
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(req, 'auth/register.html')

def login_view(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('main')
        else:
            return render(req, 'auth/login.html', {'error': 'Invalid credentials'})
    return render(req, 'auth/login.html')

def logout_view(req):
    logout(req)
    return redirect('login')

def main_view(req):
    games = Game.objects.all()
    return render(req, 'main.html', {'games': games})

def about_view(req):
    return render(req, 'about.html')

@login_required
def package_view(req, id):
    game = get_object_or_404(Game, id=id)
    packages = Package.objects.filter(game=game)
    if req.method == 'POST':
        package_id = req.POST['package_id']
        player_id = req.POST['player_id']
        server_id = req.POST['server_id']
        transaction = Transaction.objects.create(
            user=req.user,
            package_id=package_id,
            player_id=player_id,
            server_id=server_id,
            status='PENDING'
        )
        return redirect('transaction', id=transaction.id)
    
    return render(req, 'package.html', {'game': game, 'packages': packages})

@login_required
def transaction_view(req, id):
    transaction = get_object_or_404(Transaction, id=id, user=req.user)
    return render(req, 'transaction.html', {'transaction': transaction})

@login_required
def payment_view(req, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=req.user)

    if req.method == 'POST':
        payment_method = req.POST.get('payment_method')
        payment = Payment.objects.create(
            transaction=transaction,
            user=req.user,
            method=payment_method,
            amount=transaction.package.price,
            status='PENDING'
        )

        payment.status = 'SUCCESS'
        payment.save()

        transaction.status = "SUCCESS"
        transaction.save()

        return redirect('transaction', id=transaction.id)

    return render(req, 'payment.html', {'transaction': transaction})