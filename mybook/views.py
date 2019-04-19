from django.shortcuts import render, redirect
from mybook import forms
from django.views.decorators.csrf import csrf_exempt
import requests


@csrf_exempt
def login(request):
    if 'session' in request.session:
        return redirect('/books')
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            if form.get_user():
                r = requests.post('https://mybook.ru/api/auth/', json=form.get_user())
                if r.status_code == 200:
                    response = redirect('/books')
                    request.session['session'] = r.cookies['session']
                    request.session.set_expiry(3600)
                    return response
                else:
                    form = forms.LoginForm()
                    is_valid = False
                    return render(request, 'mybook/login.html', {'form': form, 'is_valid': is_valid})

    else:
        is_valid = True
        form = forms.LoginForm()
    return render(request, 'mybook/login.html', {'form': form, 'is_valid': is_valid})


def get_books(request):
    if 'session' in request.session:
        session = request.session['session']
        headers = {'Accept': 'application/json; version=5'}
        r = requests.get('https://mybook.ru/api/bookuserlist/', headers=headers,
                         cookies={'session': session})
        if r.status_code == 200:
            data = r.json()
            to_parse = data["objects"]
            while data['meta']['next'] is not None:
                r = requests.get('https://mybook.ru' + data['meta']['next'], cookies={'session': session})
                data = r.json()
                to_parse = to_parse + data["objects"]
            books = []
            for x in range(len(to_parse)):
                books.append([to_parse[x]['book']['name'], to_parse[x]['book']['default_cover'],
                              to_parse[x]['book']['main_author']['cover_name']])
            return render(request, 'mybook/books.html', {'books': books})
        else:
            return redirect('/')
    else:
        return redirect('/')


def logout(request):
    print(request.session.items())
    if 'session' in request.session:
        print("logout")
        request.session.flush()
        print(request.session.items())
        return redirect('/')
    return redirect('/books')
