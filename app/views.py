import sys
import os
sys.path.append(os.path.abspath('C:\\Users\\BEROOZDG\\OneDrive\\Desktop\\مکتب\\project\\framework'))
from core.httpss import render_template
from sqlalchemy.orm import Session
from app.migrathons import engine
from app.models import User,Post
from app.session.session import create_session,get_session
from datetime import datetime
import sqlite3

def index(request):
    context = {'title': 'Home', 'message': 'Welcome to the Home Page'}
    return render_template('index.html', context)

def about(request):
    context = {'title': 'About', 'message': 'This is the About Page'}
    return render_template('about.html', context)

def register (request):
    if request.command=='POST':
        data = request.POST
        if data['password1']!=data['password2']:
            return render_template(
                    "register.html",
                    {"message": 'password error!!!'})
        else:
            with Session(engine) as session:
                user = session.query(User).filter_by(username=data["username"]).first()

                if  user:
                    return render_template(
                        "register.html",
                        {"message": f'user {data["username"]} already exists!'})
                else:
                    user = User(
                        username=data["username"],
                        password=data["password1"],
                        email=data["email"],
                    )
                session.add(user)
                session.commit()
        return render_template(
            "register.html",
            {"message": f'user {data["username"]} is registered successfully!'}
        )
    elif request.command=='GET':
        return render_template('register.html',{})

def posts_view(request):
     # name hameye textbox ha new_post bashe...va ye halghe for lazeme too front ke sakhtare post ha ro dorost neshon bede
     #name post ha items
     #ye message ham darim to safhe
     if request.command=='GET':
        #as sqlite3 ham estefade kardam
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Post")  
        data = cursor.fetchall()  
        connection.close()
        return render_template('posts.html',{'items':data,'message':'welcom!'})
     elif request.command=='POST':
         my_user_data=request.get_current_user()
         if my_user_data:
            #chon type body table session  str bood braye biron keshidane user_id yekam kod kasif shod
            user_id_1=str(my_user_data).split(':')
            user_id_2=user_id_1[1].split('}')
            user_id=int(user_id_2[0])
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT username FROM User_account WHERE id = {user_id};")  
            username =cursor.fetchone()  
            connection.close()
            data = request.POST
            now=datetime.now()
            new_post=request.POST.get('new_post')
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Post")  
            data = cursor.fetchall()  
            connection.close()
            if new_post is None:
                return render_template('posts.html',{'items':data,'message':'welcom!'})
            with Session(engine) as session:
                user = Post(
                    author=str(username[0]),
                    title='message',
                    body=new_post,
                    created_at=now)
                session.add(user)
                session.commit()
                return render_template(
                        "posts.html",
                        {'items':data,"message": "Your message has been saved successfully"})
         else:
             return render_template(
                        "posts.html",
                        {"message": "You are not logged in!!"})
     
def post_view(request):
    if request.command=='GET':
        my_user_data=request.get_current_user()
        if my_user_data:
            user_id_1=str(my_user_data).split(':')
            user_id_2=user_id_1[1].split('}')
            user_id=int(user_id_2[0])
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT username FROM User_account WHERE id = {user_id};")  
            username =cursor.fetchone()  
            connection.close()
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            my_username=username[0]
            cursor.execute(f"SELECT * FROM Post WHERE author = '{my_username}';")  
            post_au = cursor.fetchall()  
            connection.close()
            return render_template('post.html',{'items':post_au,'message':'welcom!'})
        else:
             return render_template(
                        "post.html",
                        {"message": "You are not logged in!!"})
    elif request.command=='POST':
         my_user_data=request.get_current_user()
         if my_user_data:
            user_id_1=str(my_user_data).split(':')
            user_id_2=user_id_1[1].split('}')
            user_id=int(user_id_2[0])
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT username FROM User_account WHERE id = {user_id};")  
            username =cursor.fetchone()  
            connection.close()
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            my_username=username[0]
            cursor.execute(f"SELECT * FROM Post WHERE author = '{my_username}';")  
            post_au = cursor.fetchall()
            data = request.POST
            now=datetime.now()
            new_post=data.get('new_post')
            if new_post is None:
                return render_template('post.html',{'items':post_au,'message':'welcom!'})
            with Session(engine) as session:
                user = Post(
                    author=str(username[0]),
                    title='message',
                    body=new_post,
                    created_at=now)
                session.add(user)
                session.commit()
                return render_template(
                        "post.html",
                        {'items':post_au,"message": "Your message has been saved successfully"})
         else:
             return render_template(
                        "post.html",
                        {"message": "You are not logged in!!"})
     
def login (request):
    if request.command=='GET':
        contex={}
        return render_template('login.html',contex)
    if request.command=='POST':
        data=request.POST
        username_1 = data["username"]
        password_1 = data["password"]
        if username_1 is not None and password_1 is not None:
            with Session(engine) as session:
                user = session.query(User).filter_by(username=username_1,password=password_1).first()
            if user :
                session_id = create_session(user.id)
                request.send_response(302)
                request.set_cookie('session_id', session_id)
                request.send_header('Location', '/')
                request.end_headers()
                with Session(engine) as session:
                    user = session.query(User).filter_by(username=data["username"]).first()
                    user.last_login=str(datetime.now())
                    session.commit()
                context ={'message':'You have successfully logged in'}
            else:
                context ={'message':'user not exist'}
            return render_template('login.html',context)





  
