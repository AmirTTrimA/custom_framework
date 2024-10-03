from core.http import render_template, render_css

from sqlalchemy.orm import Session
from app.migartions import engine
from app.models import User,Post, engine
from sqlalchemy import select

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

def index(request):
    context = {'title': 'Home', 'message': 'Welcome to my jinja project'}
    return render_template('index.html', context)

def css(request):
    return render_css('static/css/style.min.css')

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
        username = data.get('username')
        password = data.get('password')

        if username and password:
            session = Session()
            query = select(User).where(User.username == username)
            user = session.scalar(query)
            # with Session(engine) as session:
            #     # Fetch the user based on username
            #     query = select(User).where(User.username == username)
            #     user = session.scalar(query)

                # Check if user exists and password matches
            if user and user.password == password:
                print(f"User {user.username} logged in successfully.")
                # Here you might want to set a session or a cookie
                # For example: request.session['user_id'] = user.id
                # Redirect to index or posts page
                request.send_response(302)
                request.send_header('Location', '/posts')
                request.end_headers()
                return ""

            else:
                # Invalid credentials
                return render_template('login.html', {'title': 'Login', 'error': 'Invalid username or password.'})

    # Display the login form
    return render_template('login.html', {'title': 'Login'})


def posts_view(request):
    session = Session()
    posts = session.query(Post).all()
    return render_template('posts.html', {'posts': posts})

    with Session() as session:
        try:
            posts = session.query(Post).all()
            return render_template('posts.html', {'posts': posts})
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return render_template('error.html', {'error': 'Could not fetch posts.'})
