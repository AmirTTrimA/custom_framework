from core.http import render_template, render_css

from sqlalchemy.orm import Session
from app.migartions import engine
from app.models import User
from sqlalchemy import select

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
        # with Session(engine) as session:
        #     user = User(
        #         username= data['username'],
        #         password= data['password1'],
        #         email= data['email'],
        #     )
        #     session.add(user)
        #     session.commit()
        return render_template('register.html',{'message':f'user {data["username"]} is registered successfully!', 'title':'Registered'})
             
    elif request.command=="GET":
        return render_template('register.html',{'title': 'Register','message':""})
    


def login(request):
    if request.command == 'POST':
        data = request.POST
        username =  data.get('username')
        password = data.get('password')
        if username is not None and password is not None:
            with Session(engine) as session:
                query = select(User).where(User.username==username,User.password==password)
                user = session.scalar(query)
                if user:
                    pass
                    
        # بررسی اعتبارسنجی کاربر
        # if User.get(username) == password:
        #     session_id = create_session(username)  
        #     request.send_response(302)
        #     request.send_header('Set-Cookie', f'session_id={session_id}; HttpOnly')
        #     request.send_header('Location', '/')
        #     request.end_headers()
        #     return ""
        # else:
        #     # نمایش پیام خطا
        #     return render_template('login.html', {'error': 'Incorrect username or password'})
    # نمایش فرم لاگین
    # return render_template('login.html', {})
    elif request.command == 'GET':
        return render_template('login.html', {'title': 'Login'})




def posts_view(request):
    context = {}
    if request.command=="POST":
        new_post = request.POST.get('new_post')
        return render_template('posts.html',context)


    elif request.command=="GET":
        return render_template('posts.html',context)

  