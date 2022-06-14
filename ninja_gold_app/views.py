from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
import random

def index(request):
    if 'gold' in request.session:
        print('key exists!')
    else:
        request.session['gold'] = 0
        print("key 'key_name' does NOT exist")

    if 'activity' in request.session:
        print('key exists!')
    else:
        request.session['activity'] = []
    
    return render(request, 'index.html')

def process(request):
    location = request.POST['location']
    context = {
        "time": strftime("%B %d %Y %I:%M %p", gmtime()),
        "activities": request.session['activity'],
    }
    if (location == 'farm' or location == 'cave' or location == 'house'):
        num = int(random.randint(10, 20))
        request.session['gold'] += num
        earn_activity = f"You entered a {location} and earned {num} gold. {context['time']}"
        request.session['activity'].append(earn_activity)
        request.session.save()
    if (location == 'quest'):
        num = int(random.randint(0, 50))
        earn_take = int(random.randint(0, 1))
        if (earn_take == 0):
            request.session['gold'] += num
            earn_activity = f"You completed a {location} and earned {num} gold. {context['time']}"
            request.session['activity'].append(earn_activity)
            request.session.save()
        if (earn_take == 1):
            request.session['gold'] -= num
            faild_activity = f"You failed a {location} and lost {num} gold. Ouch. {context['time']}"
            request.session['activity'].append(faild_activity)
            request.session.save()
    return render(request, "index.html", context)

def destroy_sess(request):
    del request.session['gold']
    del request.session['activity']
    return redirect("/")