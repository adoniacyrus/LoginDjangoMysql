from django.shortcuts import render, redirect
from .models import User

def login_view(request):
    # If already logged in
    if 'user_id' in request.session:
        return render(request, 'accounts/success.html', {
            'user': {'username': request.session['username']}
        })

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Empty validation
        if not username or not password:
            return render(request, 'accounts/login.html', {
                'error': 'All fields are required',
                'username': username
            })

        # Check user
        user = User.objects.filter(username=username, password=password).first()

        if user:
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return render(request, 'accounts/success.html', {'user': user})
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid credentials',
                'username': username
            })

    return render(request, 'accounts/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')