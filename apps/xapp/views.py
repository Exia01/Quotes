from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def indexlogin(request):
    # Product.objects.all().delete()
    # Sales.objects.all().delete()
    return render(request, 'xapp/login.html')

def logout(request):
    request.session.clear()
    return redirect('/')


def loginprocess(request):
    results = User.objects.loginValidator(request.POST)
    # print(results)
    if results[0]:
        request.session['id'] = results[1].id
        request.session['name'] = results[1].name
        return redirect('/dashboard')
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='login')
        return redirect('/')


def register(request):
    return render(request, 'xapp/register.html')


def createuser(request):
    print(request.POST)
    results = User.objects.regValidator(request.POST)
    print(results)
    if results[0]:
        request.session['id'] = results[1].id
        request.session['name'] = results[1].name
        return redirect('/dashboard')
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='register')
            return redirect('/register')



def dashboard(request, user_id=None):
    
    myquotes = User.objects.get(id=request.session['id']).favoritequotes.all()
    quotes = Quote.objects.exclude(booker = request.session['id'])


    context = {
        'myquotes' : myquotes,
        'quotes' : quotes
    }

    #programmer.objects.count() this would bring out the count of it. I think.

    return render(request, 'xapp/dashboard.html', context)

# def add(request, user_id=None):
#     return render(request, 'xapp/addtrip.html')


def addquote(request, user_id=None):
    results = Quote.objects.quoteValidator(request.POST, request.session['id'])
    print(results)
    if results[0]:
        return redirect('/dashboard/{}'.format(request.session['id']))
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='quoterror')
            return redirect('/dashboard/{}'.format(request.session['id']))


def addwish(request, x):
    user = User.objects.get(id=request.session['id'])
    quote = Quote.objects.get(id=x)

    user.favoritequotes.add(quote)
    
    return redirect('/dashboard')

def showposter(request, x):
    user = User.objects.get(id =x)
    count = Quote.objects.filter(poster=x).count()
    print(count)
    quotes = Quote.objects.filter(poster=x)

    context = {
        'quotes' : quotes,
        'count' : count,
        'user' : user
    }
    return render(request, 'xapp/showquotes.html', context)


def remove(request, x):
    user = User.objects.get(id=request.session['id'])
    quote = Quote.objects.get(id=x)

    user.favoritequotes.remove(quote)
    
    return redirect('/dashboard')
