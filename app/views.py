from core.http import render_template

def index(request):
    context = {'title': 'Home', 'message': 'Welcome to the Home Page'}
    return render_template('index.html', context)

def about(request):
    context = {'title': 'About', 'message': 'This is the About Page'}
    return render_template('about.html', context)
