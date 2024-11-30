from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Game, Package, Transaction, Payment
from .forms import PackageForm, PaymentForm, RegisterForm, LoginForm

# Create your views here.
def login_view(req):
    form = LoginForm()
    if req.method == 'POST':
        form = LoginForm(req, data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=username, password=password)

            if user is not None:
                login(req, user)
                return redirect('main')

    return render(req, 'auth/login.html', {'form': form})

def register_view(req):
    form = RegisterForm()
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(req, 'auth/register.html', {'form': form})
    return render(req, 'auth/register.html', {'form': form})

@login_required
def logout_view(req):
    logout(req)
    return redirect('login')

def main_view(req):
    games = Game.objects.all()
    return render(req, 'main.html', {'games': games})

@login_required
def history_view(req):
    histories = Transaction.objects.filter(user=req.user)
    return render(req, 'history.html', {'histories': histories})

def about_view(req):
    return render(req, 'about.html')

@login_required
def package_view(req, id):
    game = get_object_or_404(Game, id=id)
    packages = Package.objects.filter(game=game)
    form = PackageForm()

    if req.method == 'POST':
        form = PackageForm(req.POST)
        form.fields['packages'].queryset = packages
        
        if form.is_valid():
            packages = form.cleaned_data['packages']
            player_id = form.cleaned_data['player_id']
            server_id = form.cleaned_data['server_id']
            transaction = Transaction.objects.create(
                user=req.user,
                package=packages,
                player_id=player_id,
                server_id=server_id,
                status='PENDING'
            )
            
            return redirect('transaction', id=transaction.id)
        else:
            print(form.errors)
    
    form.fields['packages'].queryset = packages
    return render(req, 'package.html', {'form': form})

@login_required
def transaction_view(req, id):
    transaction = get_object_or_404(Transaction, id=id, user=req.user)
    return render(req, 'transaction.html', {'transaction': transaction})

@login_required
def payment_view(req, transaction_id, status):
    form = PaymentForm()
    transaction = get_object_or_404(Transaction, id=transaction_id, user=req.user)

    if status == 'failed':
        transaction.status = "FAILED"
        transaction.save()
        return redirect('main')

    if req.method == 'POST':
        payment_method = req.POST.get('payment_method')

        payment = Payment.objects.create(
            transaction=transaction,
            user=req.user,
            method=payment_method,
            amount=transaction.package.price,
            status='PENDING'
        )

        if status == 'success':
            payment.status = 'SUCCESS'
            payment.save()

            transaction.status = "SUCCESS"
            transaction.save()
            return redirect('transaction', id=transaction.id)

    return render(req, 'payment.html', {'transaction': transaction, 'form': form})