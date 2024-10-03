from core.http import render_template

from sqlalchemy.orm import Session
from app.migartions import engine
from app.models import User,Post
from sqlalchemy import select

def index(request):
    context = {'title': 'Home', 'message': 'Welcome to my jinja project'}
    return render_template('index.html', context)

# def css(request):
#     return render_css('static/css/style.min.css')

def about(request):
    context = {'title': 'About', 'message': 'This is the About Page'}
    return render_template('about.html', context)

def post(request,post_id):
    with Session(engine) as session:
        query = select(Post).where(Post.id==post_id)
        post = session.scalar(query)
    context = {'title': 'Post', 'post': post}
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
            print(user.id)
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
                    print(user.username)
                    
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
        data = request.POST
        with Session(engine) as session:
            post = Post(
                body= data['body'],
                user_id= request.user.id,
                user= request.user,
            )
            session.add(post)
            session.commit()
            print(post.id)
        return render_template('posts.html',context)


    elif request.command=="GET":
        context={}
        with Session() as session:
            posts = session.query(Post).all()
            context={'posts':posts}
        return render_template('posts.html',context)

  