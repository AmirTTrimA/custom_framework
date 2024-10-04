from core.http import render_template, render_css, MyHandler

from sqlalchemy.orm import Session
from app.migartions import engine
from app.models import User, Post
from sqlalchemy import select
from session.session import creat_session

def index(request):
    context = {'title': 'Home', 'message': 'Welcome to my jinja project'}
    return render_template('index.html', context)

def css(request):
    return render_css('static/css/style.min.css')

def about(request):
    context = {'title': 'About', 'message': 'This is the About Page'}
    return render_template('about.html', context)
def post(request):
    context = {'title': 'Post', 'message': '????'}
    return render_template('post.html', context)

def register(request):
    if request.command=="POST":
        data = request.POST
        with Session(engine) as session:
            user = User(
                username= data['username'],
                password= data['password1'],
                email= data['email'],
            )
            session.add(user)
            session.commit()
        return render_template('register.html',{'message':f'user {data["username"]} is registered successfully!', 'title':'Registered'})
             
    elif request.command=="GET":
        return render_template('register.html',{'title': 'Register','message':""})
    


def login(request):
    if request.command == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if username is not None and password is not None:
            with Session(engine) as session:
                query = select(User).where(User.username==username,User.password==password)
                user = session.scalar(query)
                if user == None:
                    return render_template('login.html', {'title': 'Login','message':'<div class="alert alert-danger">Invalid Credentials</div>'})
                else:
                    session_id = creat_session(user.id)  
                    request.send_response(302)
                    request.send_header('Set-Cookie', f'session_id={session_id}; HttpOnly')
                    request.send_header('Location', '/posts')
                    request.end_headers()
                    # return render_template('login.html', {'title': 'Login','message':'<div class="alert alert-success">Logged in successfully!</div>'})
    elif request.command == 'GET':
        return render_template('login.html', {'title': 'Login'})




def posts_view(request):
    context = []
    if request.command=="POST":
        
        with Session(engine) as session:
            query = select(User).where(User.id==request.get_current_user())
            user = session.scalar(query)
            new_post = Post (
                body = request.POST.get('new_post'),
                user_id = request.get_current_user(),
                user_name = user.username
            )
            session.add(new_post)
            session.commit()
            context = session.query(Post).all()
            return render_template('posts.html',{'posts' : context})


    elif request.command=="GET":
        with Session(engine) as session:
                context = session.query(Post).all()
                return render_template('posts.html', {'posts' : context})

  